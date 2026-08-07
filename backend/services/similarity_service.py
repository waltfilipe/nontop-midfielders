"""Seven-pillars player similarity for API (satellite ↔ Top 5)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

import player_profiles as pp
import transfermarkt_profiles as tm
from passes_engine import SATELLITE_LEAGUE_SOURCES, TOP5_LEAGUE_SOURCES

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TOP5_CACHE_PATH = DATA_DIR / "top5_midfielders_scored.json"

SIMILARITY_PILLARS: tuple[tuple[str, str], ...] = (
    ("pass_volume_display", "Volume"),
    ("pass_efficiency_display", "Efficiency"),
    ("pass_buildup_display", "Build-up"),
    ("pass_chance_creation_display", "Chance creation"),
    ("xp_activity_display", "Productivity"),
    ("xp_efficiency_display", "Precision"),
    ("xp_edge_display", "Lethality"),
)
PILLAR_KEYS: tuple[str, ...] = tuple(key for key, _ in SIMILARITY_PILLARS)

POOL_SATELLITE = "satellite"
POOL_TOP5 = "top5"
POOL_ALL = "all"
POOL_CHOICES = frozenset({POOL_SATELLITE, POOL_TOP5, POOL_ALL})


def _merge_player_xp(player: dict, xp: dict) -> dict:
    row = {**player, **xp}
    row["league_source"] = player.get("league_source") or xp.get("league_source")
    row["league"] = player.get("league") or xp.get("league")
    row["team"] = player.get("team") or xp.get("team")
    return row


def _eligible_seven_pillars(players: list[dict]) -> list[dict]:
    return [
        p
        for p in players
        if p.get("xp_profile_bars_eligible")
        and all(p.get(key) is not None for key in PILLAR_KEYS)
    ]


def _load_satellite_midfielders() -> list[dict]:
    from services.player_pool_service import enrich_player_profile_fields, get_pool_parts

    parts = get_pool_parts("midfielders")
    merged: list[dict] = []
    for raw in parts.get("analysis_players", []):
        if not isinstance(raw, dict):
            continue
        row = enrich_player_profile_fields(dict(raw))
        pid = str(row.get("player_id", ""))
        if not pid:
            continue
        row["market_value_eur"] = row.get("market_value_eur") or tm.read_cached_market_value_eur(pid)
        row["market_value_display"] = row.get("market_value") or tm.read_cached_market_value(pid)
        row["photo_url"] = row.get("photo_url") or pp.read_cached_photo_url(pid)
        merged.append(row)
    return merged


def _load_top5_midfielders() -> list[dict]:
    if not TOP5_CACHE_PATH.is_file():
        return []
    payload = json.loads(TOP5_CACHE_PATH.read_text(encoding="utf-8"))
    players = payload.get("players", [])
    if not isinstance(players, list):
        return []
    return [dict(p) for p in players if isinstance(p, dict)]


@lru_cache(maxsize=1)
def _cached_pools() -> tuple[list[dict], list[dict], list[dict]]:
    satellite_raw = _load_satellite_midfielders()
    top5_raw = _load_top5_midfielders()
    satellite = _eligible_seven_pillars(
        [p for p in satellite_raw if str(p.get("league_source", "")) in SATELLITE_LEAGUE_SOURCES]
    )
    top5 = _eligible_seven_pillars(
        [p for p in top5_raw if str(p.get("league_source", "")) in TOP5_LEAGUE_SOURCES]
    )
    by_id: dict[str, dict] = {}
    for player in satellite + top5:
        by_id[str(player["player_id"])] = player
    all_players = list(by_id.values())
    return satellite, top5, all_players


def clear_similarity_cache() -> None:
    _cached_pools.cache_clear()


def pool_counts() -> dict[str, int]:
    satellite, top5, all_players = _cached_pools()
    return {
        POOL_SATELLITE: len(satellite),
        POOL_TOP5: len(top5),
        POOL_ALL: len(all_players),
    }


def _normalize_pool(pool: str) -> str:
    key = (pool or POOL_ALL).strip().lower()
    if key not in POOL_CHOICES:
        return POOL_ALL
    return key


def players_for_pool(pool: str) -> list[dict]:
    satellite, top5, all_players = _cached_pools()
    key = _normalize_pool(pool)
    if key == POOL_SATELLITE:
        return satellite
    if key == POOL_TOP5:
        return top5
    return all_players


def _pillar_vector(player: dict) -> np.ndarray:
    return np.array([float(player[key]) for key in PILLAR_KEYS], dtype=float)


def _similarity_pct(distance: float, scale: float) -> float:
    if scale <= 0:
        return 100.0 if distance == 0 else 0.0
    return float(np.clip(100.0 * (1.0 - distance / scale), 0.0, 100.0))


def find_similar_players(
    target_player_id: str,
    *,
    candidate_pool: str = POOL_SATELLITE,
    reference_pool: str | None = None,
    top_k: int = 10,
    max_market_value_eur: float | None = None,
) -> dict[str, Any] | None:
    target_id = str(target_player_id).strip()
    if not target_id:
        return None

    ref_pool_key = _normalize_pool(reference_pool or POOL_ALL)
    cand_pool_key = _normalize_pool(candidate_pool)

    ref_players = players_for_pool(ref_pool_key)
    cand_players = players_for_pool(cand_pool_key)

    target = next((p for p in ref_players if str(p["player_id"]) == target_id), None)
    if target is None:
        _, _, all_players = _cached_pools()
        target = next((p for p in all_players if str(p["player_id"]) == target_id), None)
    if target is None:
        return None

    candidates = [
        p
        for p in cand_players
        if str(p["player_id"]) != target_id
        and (
            max_market_value_eur is None
            or p.get("market_value_eur") is None
            or float(p["market_value_eur"]) <= max_market_value_eur
        )
    ]
    if not candidates:
        return _serialize_target(target, similar=[], candidate_pool=cand_pool_key)

    raw = np.vstack([_pillar_vector(p) for p in candidates])
    mean = raw.mean(axis=0)
    std = raw.std(axis=0)
    std[std == 0] = 1.0
    z_pool = (raw - mean) / std
    z_target = (_pillar_vector(target) - mean) / std
    dists = np.sqrt(((z_pool - z_target) ** 2).sum(axis=1))
    scale = float(dists.max()) if len(dists) else 1.0
    if scale <= 0:
        scale = 1.0

    rows: list[dict[str, Any]] = []
    for dist, cand in zip(dists, candidates):
        pillar_delta = {
            label: round(float(cand[key]) - float(target[key]), 1)
            for key, label in SIMILARITY_PILLARS
        }
        rows.append({
            "player_id": cand["player_id"],
            "player_name": cand.get("player_name"),
            "team": cand.get("team"),
            "league": cand.get("league"),
            "league_source": cand.get("league_source"),
            "similarity_pct": round(_similarity_pct(float(dist), scale), 1),
            "distance": round(float(dist), 3),
            "market_value_display": cand.get("market_value_display") or "—",
            "market_value_eur": cand.get("market_value_eur"),
            "xp_pass_rating": cand.get("xp_pass_rating"),
            "pillars": {
                label: round(float(cand[key]), 1)
                for key, label in SIMILARITY_PILLARS
            },
            "pillar_delta": pillar_delta,
        })

    rows.sort(key=lambda r: (-r["similarity_pct"], r["distance"]))
    return _serialize_target(target, similar=rows[:top_k], candidate_pool=cand_pool_key)


def _serialize_target(
    target: dict,
    *,
    similar: list[dict[str, Any]],
    candidate_pool: str,
) -> dict[str, Any]:
    return {
        "target": {
            "player_id": target.get("player_id"),
            "player_name": target.get("player_name"),
            "team": target.get("team"),
            "league": target.get("league"),
            "league_source": target.get("league_source"),
            "market_value_display": target.get("market_value_display") or "—",
            "market_value_eur": target.get("market_value_eur"),
            "xp_pass_rating": target.get("xp_pass_rating"),
            "pillars": {
                label: round(float(target[key]), 1)
                for key, label in SIMILARITY_PILLARS
                if target.get(key) is not None
            },
        },
        "method": "seven_pillars",
        "pillar_labels": [label for _, label in SIMILARITY_PILLARS],
        "candidate_pool": candidate_pool,
        "similar": similar,
    }


def player_options_for_pool(pool: str, *, limit: int = 500) -> list[dict[str, str]]:
    players = players_for_pool(pool)
    players.sort(
        key=lambda p: (
            -float(p.get("xp_pass_rating") or 0),
            str(p.get("player_name", "")).lower(),
        )
    )
    options: list[dict[str, str]] = []
    for idx, player in enumerate(players[:limit], start=1):
        pid = str(player["player_id"])
        name = str(player.get("player_name", "—"))
        team = str(player.get("team", "—"))
        league = str(player.get("league", "—"))
        rating = player.get("xp_pass_rating")
        suffix = f" · Pass {float(rating):.2f}" if rating is not None else ""
        options.append({
            "player_id": pid,
            "player_name": name,
            "team": team,
            "league": league,
            "label": f"#{idx} {name} ({team}) · {league}{suffix}",
        })
    return options


def merged_compare_parts(base_parts: dict[str, Any]) -> dict[str, Any]:
    """Merge Top 5 scored players into pool dicts for head-to-head compare."""
    _, _, all_players = _cached_pools()
    parts = dict(base_parts)
    players_by_id = dict(parts.get("players_by_id") or {})
    progression_by_id = dict(parts.get("progression_by_id") or {})
    xp_by_id = dict(parts.get("xp_by_id") or {})
    for player in all_players:
        pid = str(player["player_id"])
        if pid not in xp_by_id:
            players_by_id[pid] = player
            progression_by_id[pid] = player
            xp_by_id[pid] = player
    parts["players_by_id"] = players_by_id
    parts["progression_by_id"] = progression_by_id
    parts["xp_by_id"] = xp_by_id
    return parts
