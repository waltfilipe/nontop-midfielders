#!/usr/bin/env python3
"""Generate top-N player reports per age category for frontend/lib/playerReports.ts.

Uses the precomputed API pool cache plus cached profile ages. Run from backend/:

    python scripts/generate_age_group_reports.py
    python scripts/generate_age_group_reports.py --top 15 --write
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import player_profiles as pp

API_POOL_PATH = ROOT / "data" / "api_pool_midfielders.json"

TOP_N_DEFAULT = 15
RANK_KEY = "xp_pass_rating"

REPORT_BANDS: tuple[tuple[str, int | None, int | None], ...] = (
    ("u23-breakout", None, 23),
    ("blue-collar-24-30", 24, 30),
    ("experience-30-plus", 31, None),
)

CATEGORY_META: dict[str, dict[str, str]] = {
    "u23-breakout": {
        "title": "U23 — Breakout Promises",
        "subtitle": "Emerging profiles under 23",
        "description": "Young midfielders with standout pass profiles and room to scale impact.",
        "accent": "#a78bfa",
    },
    "blue-collar-24-30": {
        "title": "24–30 — Blue Collar Prospects",
        "subtitle": "Prime-age engine room",
        "description": "Reliable progression and pass-value profiles in the peak development window.",
        "accent": "#38bdf8",
    },
    "experience-30-plus": {
        "title": "30+ — Standout Experience",
        "subtitle": "Veteran control & leadership",
        "description": "Experienced midfield profiles with elite game management and passing authority.",
        "accent": "#fbbf24",
    },
}


def _player_age(player: dict[str, Any]) -> int | None:
    age = player.get("age")
    if age is not None:
        try:
            return int(age)
        except (TypeError, ValueError):
            pass
    pid = str(player.get("player_id", ""))
    if not pid:
        return None
    return pp.read_cached_age(pid)


def _in_age_band(age: int, age_min: int | None, age_max: int | None) -> bool:
    if age_min is not None and age < age_min:
        return False
    if age_max is not None and age > age_max:
        return False
    return True


def _rank_value(player: dict[str, Any]) -> float:
    value = player.get(RANK_KEY)
    if value is None:
        return float("-inf")
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("-inf")


def load_midfielder_pool() -> list[dict[str, Any]]:
    path = API_POOL_PATH
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    players = payload.get("players", [])
    if not isinstance(players, list):
        raise ValueError(f"Invalid pool cache: {path}")
    return players


def select_top_by_age_band(
    players: list[dict[str, Any]],
    *,
    top_n: int,
) -> dict[str, list[dict[str, Any]]]:
    eligible = [p for p in players if p.get("eligible_for_rating")]
    results: dict[str, list[dict[str, Any]]] = {}

    for category_id, age_min, age_max in REPORT_BANDS:
        pool: list[dict[str, Any]] = []
        for player in eligible:
            age = _player_age(player)
            if age is None:
                continue
            if not _in_age_band(age, age_min, age_max):
                continue
            pool.append(player)

        pool.sort(
            key=lambda p: (
                -_rank_value(p),
                str(p.get("player_name", "")).lower(),
            )
        )
        results[category_id] = pool[:top_n]

    return results


def _ts_player_ref(player: dict[str, Any]) -> str:
    pid = str(player["player_id"])
    name = str(player.get("player_name", "—"))
    team = str(player.get("team", "—"))
    rating = player.get(RANK_KEY)
    age = _player_age(player)
    rating_text = f"{float(rating):.2f}" if rating is not None else "—"
    age_text = str(age) if age is not None else "?"
    note = f"{name} ({team}) · age {age_text} · pass {rating_text}"
    escaped_note = note.replace("\\", "\\\\").replace('"', '\\"')
    return (
        f'      {{ playerId: "{pid}", positionFamily: "midfielders", note: "{escaped_note}" }},'
    )


def render_player_reports_ts(selection: dict[str, list[dict[str, Any]]]) -> str:
    lines: list[str] = [
        'export type ReportPlayerRef = {',
        "  playerId: string;",
        "  positionFamily?: string;",
        "  note?: string;",
        "};",
        "",
        "export type ReportPlayerGroup = {",
        "  label?: string;",
        "  players: ReportPlayerRef[];",
        "};",
        "",
        "export type PlayerReportCategory = {",
        "  id: string;",
        "  title: string;",
        "  subtitle: string;",
        "  description: string;",
        "  accent: string;",
        "  groups: ReportPlayerGroup[];",
        "};",
        "",
        "export const PLAYER_REPORT_CATEGORIES: PlayerReportCategory[] = [",
    ]

    for category_id, _age_min, _age_max in REPORT_BANDS:
        meta = CATEGORY_META[category_id]
        players = selection.get(category_id, [])
        lines.extend([
            "  {",
            f'    id: "{category_id}",',
            f'    title: "{meta["title"]}",',
            f'    subtitle: "{meta["subtitle"]}",',
            f'    description: "{meta["description"]}",',
            f'    accent: "{meta["accent"]}",',
            "    groups: [{",
            "      players: [",
        ])
        if players:
            lines.extend(_ts_player_ref(player) for player in players)
        lines.extend([
            "      ],",
            "    }],",
            "  },",
        ])

    lines.extend([
        "];",
        "",
        "export function allReportPlayerRefs(): ReportPlayerRef[] {",
        "  const seen = new Set<string>();",
        "  const out: ReportPlayerRef[] = [];",
        "  for (const category of PLAYER_REPORT_CATEGORIES) {",
        "    for (const group of category.groups) {",
        "      for (const player of group.players) {",
        "        if (seen.has(player.playerId)) continue;",
        "        seen.add(player.playerId);",
        "        out.push(player);",
        "      }",
        "    }",
        "  }",
        "  return out;",
        "}",
        "",
        "export function totalReportCount(): number {",
        "  return allReportPlayerRefs().length;",
        "}",
        "",
        "export type EnrichedReportPlayer = ReportPlayerRef & {",
        "  category: PlayerReportCategory;",
        "  groupLabel?: string;",
        "  /** 1-based index within the age category. */",
        "  categoryIndex: number;",
        "};",
        "",
        "export function enrichedReportPlayers(): EnrichedReportPlayer[] {",
        "  const out: EnrichedReportPlayer[] = [];",
        "  for (const category of PLAYER_REPORT_CATEGORIES) {",
        "    let categoryIndex = 0;",
        "    for (const group of category.groups) {",
        "      for (const player of group.players) {",
        "        categoryIndex += 1;",
        "        out.push({",
        "          ...player,",
        "          category,",
        "          groupLabel: group.label,",
        "          categoryIndex,",
        "        });",
        "      }",
        "    }",
        "  }",
        "  return out;",
        "}",
        "",
    ])
    return "\n".join(lines)


def print_summary(selection: dict[str, list[dict[str, Any]]]) -> None:
    for category_id, _age_min, _age_max in REPORT_BANDS:
        meta = CATEGORY_META[category_id]
        players = selection.get(category_id, [])
        print(f"\n{meta['title']} ({len(players)} players)", flush=True)
        for idx, player in enumerate(players, start=1):
            age = _player_age(player)
            rating = player.get(RANK_KEY)
            rating_text = f"{float(rating):.2f}" if rating is not None else "—"
            print(
                f"  {idx:>2}. {player.get('player_name')} ({player.get('team')}) "
                f"age={age} pass={rating_text}",
                flush=True,
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate top player reports per age group.")
    parser.add_argument("--top", type=int, default=TOP_N_DEFAULT, help="Players per age band")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write frontend/lib/playerReports.ts",
    )
    args = parser.parse_args()

    players = load_midfielder_pool()
    selection = select_top_by_age_band(players, top_n=args.top)
    print_summary(selection)

    out_path = REPO_ROOT / "frontend" / "lib" / "playerReports.ts"
    content = render_player_reports_ts(selection)
    if args.write:
        out_path.write_text(content, encoding="utf-8")
        print(f"\nWrote {out_path}", flush=True)
    else:
        print("\nDry run — pass --write to update frontend/lib/playerReports.ts", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
