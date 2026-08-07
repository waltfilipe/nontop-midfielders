#!/usr/bin/env python3
"""Cross-league midfielder similarity: Top 5 Europe ↔ six satellite leagues.

Offline report generator. Scores both pools with the same xP / pass pillar pipeline,
then runs k-NN similarity in both directions:

  top5-to-satellite  — find affordable comps in Belgium, Portugal, etc. for a Top 5 star
  satellite-to-top5  — find elite-league comps for a satellite-league player

Methods compared in the report:
  1. seven_pillars  — scout display scores (Volume, Efficiency, Build-up, …)
  2. alt_metrics    — style/rate metrics (long pass share, xPV, COE, …)
  3. hybrid         — 65% alt_metrics + 35% seven_pillars rank blend

Examples:
    python scripts/study_top5_satellite_similarity.py
    python scripts/study_top5_satellite_similarity.py --rebuild-top5
    python scripts/study_top5_satellite_similarity.py --top-k 10
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ROOT.parent
SCRIPTS = ROOT / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import midfield_origin as mo
import passes_engine as pe
import transfermarkt_profiles as tm
import xp_engine as xe
from european_similarity_engine import ALT_KEYS, attach_derived_rates, knn_alt_metrics_similarity
from passes_engine import SATELLITE_LEAGUE_SOURCES, TOP5_LEAGUE_SOURCES, compute_pass_ratings
import study_player_similarity_seven_pillars as pillars

PILLAR_KEYS = pillars.PILLAR_KEYS
SIMILARITY_PILLARS = pillars.SIMILARITY_PILLARS
find_similar_seven_pillars = pillars.find_similar
REPORT_PATH = ROOT / "docs" / "top5_satellite_similarity.md"
JSON_PATH = ROOT / "docs" / "top5_satellite_similarity.json"
TOP5_CACHE_PATH = ROOT / "data" / "top5_midfielders_scored.json"
REPORT_PLAYERS_TS = REPO_ROOT / "frontend" / "lib" / "playerReports.ts"

DEFAULT_TOP5_TARGETS: tuple[str, ...] = (
    "Rodri",
    "Vitinha",
    "Joshua Kimmich",
    "Bruno Fernandes",
    "Pedri",
    "Manuel Locatelli",
    "João Neves",
)

METHODS: tuple[tuple[str, str], ...] = (
    ("seven_pillars", "Seven pillars (scout display scores)"),
    ("alt_metrics", "Alt metrics (style / rate profile)"),
    ("hybrid", "Hybrid (65% alt + 35% pillars)"),
)


def _merge_player_xp(player: dict, xp: dict) -> dict:
    row = {**player, **xp}
    row["league_source"] = player.get("league_source") or xp.get("league_source")
    row["league"] = player.get("league") or xp.get("league")
    row["team"] = player.get("team") or xp.get("team")
    return row


def _score_midfielders_from_frame(frame: pd.DataFrame) -> list[dict]:
    """Score midfielders from a raw pass frame using the same pipeline as the app."""
    import xp_stats_engine as xstats

    family = "midfielders"
    filtered = pe._filter_pass_frame_by_position_family(frame, family)
    if filtered.empty:
        return []

    season = xe._build_season_passes_from_frame(
        filtered,
        blend_league_reference=True,
    )
    if season.empty:
        return []

    minutes_info = pe._minutes_from_passes_frame(season)
    league_by_player: dict[str, str] = {}
    if "league_source" in filtered.columns:
        league_by_player = (
            filtered.groupby("player_id", sort=False)["league_source"]
            .agg(lambda s: s.mode().iloc[0] if not s.mode().empty else s.iloc[0])
            .astype(str)
            .to_dict()
        )
    elif "league_source" in season.columns:
        league_by_player = (
            season.groupby("player_id", sort=False)["league_source"]
            .agg(lambda s: s.mode().iloc[0] if not s.mode().empty else s.iloc[0])
            .astype(str)
            .to_dict()
        )

    registry = pe.build_player_registry(season)
    registry_by_id = {str(p["code"]): p for p in registry}
    ti_v2_progress_cutoffs = xstats.test_impact_v2_attempt_progress_cutoffs(season)

    xp_rows: list[dict] = []
    for pid, grp in season.groupby("player_id", sort=False):
        pid = str(pid)
        player = registry_by_id.get(pid)
        if player is None:
            continue
        completed = int((grp["is_won"] & grp["has_end"]).sum())
        if completed < 100:
            continue
        mins = minutes_info.get(pid, {})
        metrics = xstats.compute_extended_xp_stats(
            grp,
            test_impact_v2_progress_cutoffs=ti_v2_progress_cutoffs,
        )
        if not metrics:
            continue
        minutes = mins.get("minutes")
        player_raw = filtered[filtered["player_id"].astype(str) == pid]
        xstats.attach_regular_pass_stats(metrics, player_raw, minutes)
        xstats.apply_per90_metrics(metrics, minutes)
        league_source = str(league_by_player.get(pid, ""))
        xp_rows.append({
            "player_id": pid,
            "player_name": player["name"],
            "position": player.get("position", "—"),
            "position_group": pe.rating_position_group(player.get("position")),
            "position_family": family,
            "team": mins.get("team", "—"),
            "minutes": mins.get("minutes"),
            "minutes_pct": mins.get("minutes_pct"),
            "league": pe._league_label(league_source),
            "league_source": league_source,
            "passes_completed": completed,
            **metrics,
        })

    import xpass_engine as xpass_mod

    xpass_mod.attach_xpass_metrics_to_players(xp_rows, season=season)
    xstats.attach_distance_indices(xp_rows)
    xstats.attach_pass_length_profile(xp_rows)
    xstats.attach_regular_pass_scores(xp_rows)
    xstats.attach_composite_indices(xp_rows)
    xstats.attach_xp_pass_ratings(xp_rows)
    xstats.attach_all_stats_ranks(xp_rows)
    xe.attach_xp_metric_ranks(xp_rows)
    xp_by_id = {str(p["player_id"]): p for p in xp_rows}

    passes = pe._enrich_passes(filtered)
    players = pe._build_midfielders_from_enriched_frame(filtered, passes)
    passes_by_player = {str(pid): grp for pid, grp in passes.groupby("player_id", sort=False)}
    players = mo.apply_midfield_position_groups(players, passes_by_player, {})
    _, players_by_id, _ = compute_pass_ratings(players)
    xe.refresh_xp_midfield_origin_rankings(xp_rows)

    merged: list[dict] = []
    for player in players:
        pid = str(player["player_id"])
        xp = xp_by_id.get(pid)
        if not xp:
            continue
        row = _merge_player_xp(player, xp)
        row["pass_rating"] = players_by_id.get(pid, {}).get("pass_rating")
        row["market_value_eur"] = tm.read_cached_market_value_eur(pid)
        row["market_value_display"] = tm.read_cached_market_value(pid)
        attach_derived_rates(row)
        merged.append(row)
    return merged


def _eligible_seven_pillars(players: list[dict]) -> list[dict]:
    return [
        p
        for p in players
        if p.get("xp_profile_bars_eligible")
        and all(p.get(key) is not None for key in PILLAR_KEYS)
    ]


def _eligible_alt_metrics(players: list[dict]) -> list[dict]:
    return [
        p
        for p in players
        if p.get("xp_profile_bars_eligible")
        and all(p.get(key) is not None for key in ALT_KEYS)
    ]


def _filter_leagues(players: list[dict], sources: frozenset[str]) -> list[dict]:
    return [p for p in players if str(p.get("league_source", "")) in sources]


def _player_by_name(pool: list[dict], name: str) -> dict | None:
    name_l = name.strip().lower()
    matches = [p for p in pool if str(p.get("player_name", "")).strip().lower() == name_l]
    if not matches:
        return None
    return max(matches, key=lambda p: float(p.get("minutes") or 0))


def _hybrid_similar(
    target: dict,
    pool: list[dict],
    *,
    top_k: int,
    max_market_value_eur: float | None = None,
) -> list[dict[str, Any]]:
    pillar_rows = find_similar_seven_pillars(
        target,
        pool,
        top_k=max(top_k * 3, 20),
        max_market_value_eur=max_market_value_eur,
    )
    alt_rows = knn_alt_metrics_similarity(
        target,
        pool,
        top_k=max(top_k * 3, 20),
    )
    pillar_rank = {str(r["player_id"]): i for i, r in enumerate(pillar_rows)}
    alt_rank = {str(r["player_id"]): i for i, r in enumerate(alt_rows)}
    candidates = {str(p["player_id"]) for p in pool if str(p["player_id"]) != str(target["player_id"])}
    scored: list[tuple[float, dict]] = []
    for pid in candidates:
        pr = pillar_rank.get(pid, len(pillar_rows) + 10)
        ar = alt_rank.get(pid, len(alt_rows) + 10)
        blend = 0.35 * pr + 0.65 * ar
        player = next(p for p in pool if str(p["player_id"]) == pid)
        if max_market_value_eur is not None:
            mv = player.get("market_value_eur")
            if mv is not None and float(mv) > max_market_value_eur:
                continue
        scored.append((blend, player))
    scored.sort(key=lambda item: item[0])
    out: list[dict[str, Any]] = []
    max_rank = max(len(scored), 1)
    for rank, (_blend, player) in enumerate(scored[:top_k]):
        sim_pct = round(100.0 * (1.0 - rank / max_rank), 1)
        out.append({
            "player_id": player["player_id"],
            "player_name": player.get("player_name"),
            "team": player.get("team"),
            "league": player.get("league"),
            "league_source": player.get("league_source"),
            "similarity_pct": sim_pct,
            "market_value_display": player.get("market_value_display") or "—",
            "xp_pass_rating": player.get("xp_pass_rating"),
        })
    return out


def _similar_for_method(
    method: str,
    target: dict,
    pool: list[dict],
    *,
    top_k: int,
    max_market_value_eur: float | None = None,
) -> list[dict[str, Any]]:
    if method == "seven_pillars":
        return find_similar_seven_pillars(
            target,
            pool,
            top_k=top_k,
            max_market_value_eur=max_market_value_eur,
        )
    if method == "alt_metrics":
        return knn_alt_metrics_similarity(target, pool, top_k=top_k)
    return _hybrid_similar(
        target,
        pool,
        top_k=top_k,
        max_market_value_eur=max_market_value_eur,
    )


def _load_satellite_pool() -> list[dict]:
    print("Loading satellite pool from European analytics…", flush=True)
    players = pe.build_european_league_midfielders()
    passes_by_player = pe.load_european_league_passes_grouped()
    players = mo.apply_midfield_position_groups(players, passes_by_player, {})
    _, players_by_id, _ = compute_pass_ratings(players)
    _, xp_players = xe.build_european_league_xp_analytics()
    xp_by_id = {str(p["player_id"]): p for p in xp_players}

    merged: list[dict] = []
    for player in players:
        pid = str(player["player_id"])
        xp = xp_by_id.get(pid, {})
        if not xp:
            continue
        row = _merge_player_xp(player, xp)
        row["pass_rating"] = players_by_id.get(pid, {}).get("pass_rating")
        row["market_value_eur"] = tm.read_cached_market_value_eur(pid)
        row["market_value_display"] = tm.read_cached_market_value(pid)
        attach_derived_rates(row)
        merged.append(row)
    return merged


def _load_top5_pool(*, rebuild: bool = False) -> list[dict]:
    if TOP5_CACHE_PATH.is_file() and not rebuild:
        payload = json.loads(TOP5_CACHE_PATH.read_text(encoding="utf-8"))
        players = payload.get("players", [])
        if players:
            print(f"Loaded Top 5 cache ({len(players)} players).", flush=True)
            return players

    print("Scoring Top 5 leagues (this may take several minutes)…", flush=True)
    frame = pe._load_top5_league_pass_frame()
    players = _score_midfielders_from_frame(frame)
    TOP5_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOP5_CACHE_PATH.write_text(
        json.dumps(
            {
                "player_count": len(players),
                "leagues": list(TOP5_LEAGUE_SOURCES),
                "players": players,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {TOP5_CACHE_PATH} ({len(players)} players).", flush=True)
    return players


def _report_player_names() -> list[str]:
    if not REPORT_PLAYERS_TS.is_file():
        return []
    text = REPORT_PLAYERS_TS.read_text(encoding="utf-8")
    notes = re.findall(r'note: "([^"]+)"', text)
    names: list[str] = []
    for note in notes:
        name = note.split(" (")[0].strip()
        if name and name not in names:
            names.append(name)
    return names


def _target_block(
    target: dict,
    pool: list[dict],
    *,
    top_k: int,
    direction: str,
    alt_pool: list[dict] | None = None,
) -> dict[str, Any]:
    cheaper: dict[str, list[dict[str, Any]]] = {}
    methods_out: dict[str, list[dict[str, Any]]] = {}
    alt_candidates = alt_pool if alt_pool is not None else pool
    for method_key, _label in METHODS:
        candidate_pool = alt_candidates if method_key in {"alt_metrics", "hybrid"} else pool
        rows = _similar_for_method(method_key, target, candidate_pool, top_k=top_k)
        for row in rows:
            row["league"] = row.get("league") or next(
                (p.get("league") for p in pool if str(p["player_id"]) == str(row["player_id"])),
                "—",
            )
        methods_out[method_key] = rows

    target_mv = target.get("market_value_eur")
    if direction == "top5-to-satellite" and target_mv is not None and float(target_mv) > 0:
        cap = float(target_mv) * 0.35
        cheaper["seven_pillars"] = find_similar_seven_pillars(
            target,
            pool,
            top_k=5,
            max_market_value_eur=cap,
        )

    return {
        "player_id": target.get("player_id"),
        "player_name": target.get("player_name"),
        "team": target.get("team"),
        "league": target.get("league"),
        "league_source": target.get("league_source"),
        "market_value_display": target.get("market_value_display") or "—",
        "xp_pass_rating": target.get("xp_pass_rating"),
        "pillars": {
            label: round(float(target[key]), 1)
            for key, label in SIMILARITY_PILLARS
            if target.get(key) is not None
        },
        "methods": methods_out,
        "cheaper_similar_max_35pct_mv": cheaper,
    }


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Similaridade Top 5 ↔ ligas satélite (offline)",
        "",
        "Compara meio-campistas das **6 ligas satélite** (Bélgica, Croácia, Eredivisie, Grécia, Portugal, Turquia) "
        "com as **Top 5 europeias** (Premier League, Bundesliga, Ligue 1, La Liga, Serie A).",
        "",
        "## Métodos",
        "",
        "| Método | Descrição | Melhor para |",
        "|---|---|---|",
        "| **seven_pillars** | 7 notas de scout (Volume, Efficiency, Build-up, Chance creation, Productivity, Precision, Lethality) | Alinhar com a UI do Pass Scout / relatórios |",
        "| **alt_metrics** | Perfil de estilo (longos, progressivos, xPV, COE) | Encontrar jogadores com *jeito de jogo* parecido |",
        "| **hybrid** | 65% alt_metrics + 35% seven_pillars | Equilíbrio entre estilo e nota de scout |",
        "",
        f"- Pool satélite elegível (7 pilares): **{payload['n_satellite_eligible']}**",
        f"- Pool Top 5 elegível (7 pilares): **{payload['n_top5_eligible']}**",
        "",
        "---",
        "",
        "## A) Top 5 → satélite",
        "",
        "Referência de elite → alternativas mais baratas nas 6 ligas.",
        "",
    ]

    for name, block in payload["top5_to_satellite"]["examples"].items():
        if block.get("error"):
            lines.append(f"### {name}\n\nNão encontrado no pool Top 5.\n")
            continue
        lines.append(f"### {name} ({block.get('team', '—')} · {block.get('league', '—')})")
        lines.append(f"- MV: **{block.get('market_value_display', '—')}** · xP pass: {block.get('xp_pass_rating', '—')}")
        if block.get("pillars"):
            lines.append(
                "- Pilares: "
                + " · ".join(f"{k} {v}" for k, v in block["pillars"].items())
            )
        lines.append("")
        for method_key, method_label in METHODS:
            rows = block["methods"].get(method_key, [])
            lines.append(f"#### {method_label}")
            lines.append("")
            lines.append("| Sim | Jogador | Clube | Liga | MV | xP pass |")
            lines.append("|---:|---|---|---|---:|---:|")
            for row in rows:
                lines.append(
                    f"| {row['similarity_pct']}% | {row['player_name']} | {row['team']} | "
                    f"{row.get('league', '—')} | {row['market_value_display']} | {row.get('xp_pass_rating', '—')} |"
                )
            lines.append("")
        cheaper = block.get("cheaper_similar_max_35pct_mv", {}).get("seven_pillars", [])
        if cheaper:
            lines.append("#### Alternativas ≤35% do MV (seven_pillars)")
            lines.append("")
            lines.append("| Sim | Jogador | Clube | Liga | MV |")
            lines.append("|---:|---|---|---|---:|")
            for row in cheaper:
                lines.append(
                    f"| {row['similarity_pct']}% | {row['player_name']} | {row['team']} | "
                    f"{row.get('league', '—')} | {row['market_value_display']} |"
                )
            lines.append("")

    lines.extend([
        "---",
        "",
        "## B) Satélite → Top 5",
        "",
        "Jogador das 6 ligas → comps de referência na elite europeia.",
        "",
    ])

    for name, block in payload["satellite_to_top5"]["examples"].items():
        if block.get("error"):
            lines.append(f"### {name}\n\nNão encontrado no pool satélite.\n")
            continue
        lines.append(f"### {name} ({block.get('team', '—')} · {block.get('league', '—')})")
        lines.append(f"- MV: **{block.get('market_value_display', '—')}** · xP pass: {block.get('xp_pass_rating', '—')}")
        lines.append("")
        rows = block["methods"].get("seven_pillars", [])
        lines.append("| Sim | Jogador | Clube | Liga | MV | xP pass |")
        lines.append("|---:|---|---|---|---:|---:|")
        for row in rows:
            lines.append(
                f"| {row['similarity_pct']}% | {row['player_name']} | {row['team']} | "
                f"{row.get('league', '—')} | {row['market_value_display']} | {row.get('xp_pass_rating', '—')} |"
            )
        lines.append("")

    lines.extend([
        "",
        "## Alternativas consideradas",
        "",
        "| Abordagem | Prós | Contras |",
        "|---|---|---|",
        "| **Seven pillars (recomendado)** | Mesma linguagem dos relatórios; fácil de explicar | Ignora zona de origem dos passes |",
        "| **Alt metrics** | Captura estilo (longos, xPV, COE) | Menos intuitivo para scouts |",
        "| **Heatmap / origem** | Muito bom para *onde* o jogador atua no campo | Pesado; precisa de passes por jogador em memória |",
        "| **Archetypes (5 pilares)** | Bom para rótulo tático | Não é busca por vizinho; é classificação |",
        "| **Compare API (head-to-head)** | Já existe no app | Só 1v1 manual, não ranqueia o pool |",
        "",
        "Para scouting de valor, use **top5-to-satellite** com filtro de MV ≤35%. "
        "Para projetar um satélite na elite, use **satellite-to-top5**.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Top 5 ↔ satellite league similarity report.")
    parser.add_argument("--top-k", type=int, default=8, help="Similar players per method")
    parser.add_argument("--rebuild-top5", action="store_true", help="Re-score Top 5 cache")
    parser.add_argument(
        "--skip-satellite-rescore",
        action="store_true",
        help="Load satellite pool from existing European analytics (slower path uses live score)",
    )
    args = parser.parse_args()

    satellite_all = _load_satellite_pool()
    top5_all = _load_top5_pool(rebuild=args.rebuild_top5)

    satellite_pool = _eligible_seven_pillars(_filter_leagues(satellite_all, SATELLITE_LEAGUE_SOURCES))
    satellite_alt_pool = _eligible_alt_metrics(_filter_leagues(satellite_all, SATELLITE_LEAGUE_SOURCES))
    top5_pool = _eligible_seven_pillars(_filter_leagues(top5_all, TOP5_LEAGUE_SOURCES))
    top5_alt_pool = _eligible_alt_metrics(_filter_leagues(top5_all, TOP5_LEAGUE_SOURCES))

    payload: dict[str, Any] = {
        "n_satellite_eligible": len(satellite_pool),
        "n_satellite_alt_eligible": len(satellite_alt_pool),
        "n_top5_eligible": len(top5_pool),
        "n_top5_alt_eligible": len(top5_alt_pool),
        "methods": [{"key": k, "label": v} for k, v in METHODS],
        "top5_to_satellite": {"examples": {}},
        "satellite_to_top5": {"examples": {}},
    }

    for name in DEFAULT_TOP5_TARGETS:
        target = _player_by_name(top5_pool, name)
        if target is None:
            payload["top5_to_satellite"]["examples"][name] = {"error": "not in top5 eligible pool"}
            continue
        payload["top5_to_satellite"]["examples"][name] = _target_block(
            target,
            satellite_pool,
            top_k=args.top_k,
            direction="top5-to-satellite",
            alt_pool=satellite_alt_pool,
        )

    satellite_targets = _report_player_names()[:12]
    for name in satellite_targets:
        target = _player_by_name(satellite_pool, name)
        if target is None:
            payload["satellite_to_top5"]["examples"][name] = {"error": "not in satellite eligible pool"}
            continue
        payload["satellite_to_top5"]["examples"][name] = _target_block(
            target,
            top5_pool,
            top_k=args.top_k,
            direction="satellite-to-top5",
            alt_pool=top5_alt_pool,
        )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(_render_markdown(payload), encoding="utf-8")
    JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {JSON_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
