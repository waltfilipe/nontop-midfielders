#!/usr/bin/env python3
"""Prefetch Transfermarkt profile metadata for the curated 45-player site pool."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import transfermarkt_profiles as tm

SITE_DATA = REPO_ROOT / "data"
PLAYER_IDS_FILE = SITE_DATA / "player-ids.json"
PLAYERS_FILE = SITE_DATA / "players.json"


def _load_targets() -> list[dict[str, str]]:
    player_ids = json.loads(PLAYER_IDS_FILE.read_text(encoding="utf-8"))
    players = {
        str(row["player_id"]): row
        for row in json.loads(PLAYERS_FILE.read_text(encoding="utf-8")).get("players", [])
    }
    targets: list[dict[str, str]] = []
    for pid in player_ids:
        row = players.get(str(pid), {})
        targets.append({
            "player_id": str(pid),
            "player_name": str(row.get("player_name") or ""),
            "team": str(row.get("team") or ""),
        })
    return targets


def main() -> None:
    parser = argparse.ArgumentParser(description="Prefetch Transfermarkt profiles for curated 45.")
    parser.add_argument("--force", action="store_true", help="Re-fetch even when cache looks fresh.")
    parser.add_argument("--sleep", type=float, default=0.4, help="Delay between players in seconds.")
    parser.add_argument("--limit", type=int, default=0, help="Optional cap on players to fetch.")
    args = parser.parse_args()

    targets = _load_targets()
    if args.limit > 0:
        targets = targets[: args.limit]

    print(f"Prefetching Transfermarkt profiles for {len(targets)} curated players…", flush=True)
    resolved = 0
    errors = 0
    for index, player in enumerate(targets, start=1):
        pid = player["player_id"]
        name = player["player_name"]
        team = player["team"]
        try:
            profile = tm.prefetch_transfermarkt_for_player(
                pid,
                name,
                team,
                force=args.force,
            )
        except Exception as exc:  # noqa: BLE001
            errors += 1
            print(f"  ERROR {index}/{len(targets)} · {name}: {exc}", flush=True)
            if args.sleep > 0:
                time.sleep(args.sleep)
            continue

        if profile.get("transfermarkt_fetch_status") == "ok":
            resolved += 1
        print(
            f"  {index}/{len(targets)} · {name}: "
            f"age={profile.get('age')} · nat={profile.get('nationality')} · "
            f"mv={profile.get('market_value_display')} · foot={profile.get('dominant_foot')}",
            flush=True,
        )
        if args.sleep > 0:
            time.sleep(args.sleep)

    print(f"Done. Profiles resolved: {resolved}/{len(targets)} · errors: {errors}", flush=True)


if __name__ == "__main__":
    main()
