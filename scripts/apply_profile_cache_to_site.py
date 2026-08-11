#!/usr/bin/env python3
"""Merge backend player_profiles_cache.json into static site data for curated players."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from player_profiles import format_contract_until_display, read_cached_profile  # noqa: E402
import transfermarkt_profiles as tm  # noqa: E402

DATA_DIR = ROOT / "data"
CACHE_PATH = BACKEND / "data" / "player_profiles_cache.json"
PLAYER_IDS_FILE = DATA_DIR / "player-ids.json"
PLAYERS_FILE = DATA_DIR / "players.json"
PROFILES_DIR = DATA_DIR / "profiles"


PROFILE_FIELDS = (
    "photo_url",
    "age",
    "height",
    "nationality",
    "dominant_foot",
    "market_value",
    "market_value_eur",
    "contract_until",
)


def _site_fields(pid: str) -> dict:
    cached = read_cached_profile(pid)
    if not cached:
        return {}

    photo = cached.get("photo_url") or cached.get("transfermarkt_photo_url")
    market_value = cached.get("market_value_display") or tm.read_cached_market_value(pid)
    contract_raw = cached.get("contract_until")
    contract_until = format_contract_until_display(str(contract_raw) if contract_raw else None)
    height = cached.get("height")

    out = {
        "photo_url": photo,
        "age": cached.get("age"),
        "height": height,
        "nationality": cached.get("nationality"),
        "dominant_foot": cached.get("dominant_foot"),
        "market_value": market_value,
        "market_value_eur": cached.get("market_value_eur"),
        "contract_until": contract_until or contract_raw,
    }
    return {key: value for key, value in out.items() if value is not None}


def main() -> None:
    if not CACHE_PATH.exists():
        raise SystemExit(f"Missing cache file: {CACHE_PATH}")

    player_ids = json.loads(PLAYER_IDS_FILE.read_text(encoding="utf-8"))
    players_payload = json.loads(PLAYERS_FILE.read_text(encoding="utf-8"))
    players = players_payload.get("players", [])
    by_id = {str(row["player_id"]): row for row in players}

    updated_players = 0
    updated_profiles = 0
    for pid in player_ids:
        pid = str(pid)
        fields = _site_fields(pid)
        if not fields:
            continue

        row = by_id.get(pid)
        if row:
            row.update(fields)
            updated_players += 1

        profile_path = PROFILES_DIR / f"{pid}.json"
        if profile_path.exists():
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            player = profile.setdefault("player", {})
            player.update(fields)
            profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
            updated_profiles += 1

    players_payload["players"] = list(by_id.values())
    PLAYERS_FILE.write_text(json.dumps(players_payload, ensure_ascii=False), encoding="utf-8")
    print(f"Updated players.json rows: {updated_players}/{len(player_ids)}")
    print(f"Updated profile files: {updated_profiles}/{len(player_ids)}")


if __name__ == "__main__":
    main()
