#!/usr/bin/env python3
"""Rebuild round-grade consistency series for the curated 45-player site pool."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("PASS_SCOUT_MODE", "local")

from services.profile_service import build_round_grade_series  # noqa: E402

DATA_DIR = REPO_ROOT / "data"
PROFILES_DIR = DATA_DIR / "profiles"
PLAYER_IDS = json.loads((DATA_DIR / "player-ids.json").read_text(encoding="utf-8"))


def main() -> None:
    updated = 0
    skipped = 0
    for pid in PLAYER_IDS:
        profile_path = PROFILES_DIR / f"{pid}.json"
        if not profile_path.is_file():
            print(f"  WARNING: missing profile {pid}")
            skipped += 1
            continue

        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        xp = profile.get("xp") or {}
        # Use precomputed xp_round_series / xp_game_grades from the profile xp blob.
        round_grades = build_round_grade_series(xp, None)
        if len(round_grades) < 2:
            print(f"  WARNING: insufficient round grades for {pid} ({len(round_grades)})")
            skipped += 1
            continue

        profile["xp_round_grades"] = round_grades
        profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
        updated += 1
        print(f"  updated {pid}: {len(round_grades)} rounds")

    print(f"Done. Updated {updated}/{len(PLAYER_IDS)} profiles ({skipped} skipped).")


if __name__ == "__main__":
    main()
