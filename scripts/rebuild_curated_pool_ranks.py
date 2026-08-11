#!/usr/bin/env python3
"""Recalculate rank pools for the curated 45-player site against itself."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PROFILES_DIR = DATA_DIR / "profiles"
PLAYER_IDS = [str(pid) for pid in json.loads((DATA_DIR / "player-ids.json").read_text(encoding="utf-8"))]

RANK_SPECS: tuple[tuple[str, Callable[[dict[str, Any]], str]], ...] = (
    ("_rank_in_group", lambda row: str(row.get("position_group") or row.get("midfield_origin_profile") or "unknown")),
    ("_rank_pool_in_group", lambda row: str(row.get("position_group") or row.get("midfield_origin_profile") or "unknown")),
    ("_rank_in_league", lambda row: str(row.get("league_source") or "unknown")),
    ("_rank_pool_in_league", lambda row: str(row.get("league_source") or "unknown")),
)


def _rank_desc(values: list[tuple[str, float]]) -> dict[str, tuple[int, int]]:
    ordered = sorted(values, key=lambda item: item[1], reverse=True)
    pool_size = len(ordered)
    return {pid: (index + 1, pool_size) for index, (pid, _) in enumerate(ordered)}


def _discover_metric_bases(xp_rows: dict[str, dict[str, Any]]) -> set[str]:
    bases: set[str] = set()
    suffixes = tuple(spec[0] for spec in RANK_SPECS)
    for xp in xp_rows.values():
        for key in xp:
            for suffix in suffixes:
                if key.endswith(suffix):
                    bases.add(key[: -len(suffix)])
                    break
    return bases


def _apply_rank_fields(rows: dict[str, dict[str, Any]], xp_rows: dict[str, dict[str, Any]]) -> None:
    bases = _discover_metric_bases(xp_rows)
    for suffix, group_fn in RANK_SPECS:
        for base in bases:
            rank_key = f"{base}{suffix}"
            grouped: dict[str, list[tuple[str, float]]] = defaultdict(list)
            for pid, row in rows.items():
                xp = xp_rows[pid]
                value = xp.get(base)
                if value is None:
                    continue
                try:
                    numeric = float(value)
                except (TypeError, ValueError):
                    continue
                if not (numeric == numeric):  # NaN guard
                    continue
                grouped[group_fn(row)].append((pid, numeric))

            for values in grouped.values():
                ranks = _rank_desc(values)
                for pid, (rank, pool) in ranks.items():
                    if suffix.startswith("_rank_pool"):
                        xp_rows[pid][rank_key] = pool
                    else:
                        xp_rows[pid][rank_key] = rank


def _merge_xp_into_player(player: dict[str, Any], xp: dict[str, Any]) -> dict[str, Any]:
    """Merge xp metrics into player without wiping identity fields with null xp values."""
    merged = dict(player)
    for key, value in xp.items():
        if value is not None:
            merged[key] = value
    return merged


def _rebuild_profile_sections(profile: dict[str, Any]) -> None:
    sys_path = ROOT / "backend"
    if str(sys_path) not in __import__("sys").path:
        __import__("sys").path.insert(0, str(sys_path))
    from services.profile_service import build_pass_score_sections, build_xp_profile_bars

    xp = profile.get("xp") or {}
    if xp:
        profile["pass_scores"] = build_pass_score_sections(xp)
        profile["xp_bars"] = build_xp_profile_bars(xp)


def main() -> None:
    rows: dict[str, dict[str, Any]] = {}
    xp_rows: dict[str, dict[str, Any]] = {}
    profiles: dict[str, dict[str, Any]] = {}

    for pid in PLAYER_IDS:
        profile_path = PROFILES_DIR / f"{pid}.json"
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        player = dict(profile.get("player") or {})
        xp = dict(profile.get("xp") or {})
        rows[pid] = player
        xp_rows[pid] = xp
        profiles[pid] = profile

    _apply_rank_fields(rows, xp_rows)

    for pid, profile in profiles.items():
        xp = xp_rows[pid]
        profile["xp"] = xp
        if profile.get("player"):
            profile["player"] = _merge_xp_into_player(profile["player"], xp)
        _rebuild_profile_sections(profile)
        (PROFILES_DIR / f"{pid}.json").write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")

    pool_metrics_path = DATA_DIR / "pool-metrics.json"
    pool_metrics = json.loads(pool_metrics_path.read_text(encoding="utf-8"))
    pool_by_id = {str(row.get("player_id")): row for row in pool_metrics}
    for pid in PLAYER_IDS:
        if pid not in pool_by_id:
            continue
        pool_by_id[pid].update(xp_rows[pid])
        pool_by_id[pid].update({k: v for k, v in rows[pid].items() if k in pool_by_id[pid]})
    pool_metrics_path.write_text(
        json.dumps([pool_by_id[pid] for pid in PLAYER_IDS if pid in pool_by_id], ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Rebuilt curated rank pools for {len(PLAYER_IDS)} players.")


if __name__ == "__main__":
    main()
