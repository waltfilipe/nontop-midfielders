"""Lightweight per-family player pool — precomputed JSON for Render free tier."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from position_families import DEFAULT_POSITION_FAMILY, normalize_position_family
from services.serialization import sanitize_for_json

import player_profiles as pp
import transfermarkt_profiles as tm

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
POOL_CACHE_VERSION = 1


def api_pool_path(position_family: str) -> Path:
    family = normalize_position_family(position_family)
    return DATA_DIR / f"api_pool_{family}.json"


def pool_cache_available(position_family: str) -> bool:
    return api_pool_path(position_family).is_file()


@lru_cache(maxsize=1)
def _load_pool_file(position_family: str) -> dict[str, Any]:
    """Load one family JSON; LRU maxsize=1 evicts the previous family from memory."""
    path = api_pool_path(position_family)
    if not path.is_file():
        raise FileNotFoundError(f"No API pool cache for {position_family!r}: {path}")
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict) or not isinstance(payload.get("players"), list):
        raise ValueError(f"Invalid API pool cache: {path}")
    return payload


def clear_pool_cache() -> None:
    _load_pool_file.cache_clear()


def enrich_player_profile_fields(player: dict[str, Any]) -> dict[str, Any]:
    """Merge cached profile / Transfermarkt metadata into a pool player record."""
    pid = str(player.get("player_id", ""))
    if not pid:
        return player
    out = dict(player)
    out["age"] = pp.read_cached_age(pid)
    out["height"] = pp.read_cached_height_display(pid)
    out["nationality"] = pp.read_cached_nationality(pid)
    out["dominant_foot"] = pp.read_cached_dominant_foot(pid)
    out["photo_url"] = pp.read_cached_photo_url(pid)
    out["market_value"] = tm.read_cached_market_value(pid)
    out["market_value_eur"] = tm.read_cached_market_value_eur(pid)
    out["contract_until"] = pp.read_cached_contract_until(pid)
    return out


def get_pool_parts(position_family: str = DEFAULT_POSITION_FAMILY) -> dict[str, Any]:
    """Return pool dicts compatible with legacy _bundle_parts (no pass DataFrames)."""
    family = normalize_position_family(position_family)
    payload = _load_pool_file(family)
    players: list[dict[str, Any]] = payload["players"]

    players_by_id: dict[str, dict[str, Any]] = {}
    progression_by_id: dict[str, dict[str, Any]] = {}
    xp_by_id: dict[str, dict[str, Any]] = {}

    for raw in players:
        if not isinstance(raw, dict):
            continue
        player = enrich_player_profile_fields(dict(raw))
        pid = str(player.get("player_id", ""))
        if not pid:
            continue
        players_by_id[pid] = player
        progression_by_id[pid] = player
        xp_by_id[pid] = player

    return {
        "position_family": family,
        "analysis_players": players,
        "passes_by_player": {},
        "progression_by_id": progression_by_id,
        "players_by_id": players_by_id,
        "xp_by_id": xp_by_id,
    }


def build_pool_record(
    *,
    rated: dict[str, Any],
    progression: dict[str, Any],
    xp: dict[str, Any],
    position_family: str,
) -> dict[str, Any]:
    """Merge rated + progression + xP into one JSON-safe player record."""
    pid = str(rated.get("player_id") or progression.get("player_id") or xp.get("player_id"))
    merged: dict[str, Any] = {}
    for source in (rated, progression, xp):
        if source:
            merged.update(source)
    merged["player_id"] = pid
    merged["position_family"] = position_family
    for key in ("league", "league_source"):
        for source in (rated, progression, xp):
            value = source.get(key) if source else None
            if value:
                merged[key] = value
                break
    return sanitize_for_json(merged)
