#!/usr/bin/env python3
"""Remove excluded satellite leagues (e.g. Croatia) from the backend API pool."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from satellite_leagues import EXCLUDED_LEAGUE_SOURCES, league_is_active  # noqa: E402

POOL_PATH = ROOT / "data" / "api_pool_midfielders.json"


def main() -> None:
    payload = json.loads(POOL_PATH.read_text(encoding="utf-8"))
    before = len(payload.get("players", []))
    players = [p for p in payload.get("players", []) if league_is_active(p.get("league_source"))]
    payload["players"] = players
    payload["player_count"] = len(players)
    POOL_PATH.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    removed = before - len(players)
    print(
        f"Filtered {POOL_PATH.name}: kept {len(players)} players, "
        f"removed {removed} from {sorted(EXCLUDED_LEAGUE_SOURCES)}"
    )


if __name__ == "__main__":
    main()
