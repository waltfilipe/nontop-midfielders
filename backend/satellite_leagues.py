"""Satellite European leagues included in nontop-midfielders analysis."""

from __future__ import annotations

EXCLUDED_LEAGUE_SOURCES = frozenset({"croatian_league"})

SATELLITE_LEAGUE_OPTIONS: tuple[tuple[str, str], ...] = (
    ("belgian_pro_league", "Belgian Pro League"),
    ("eredivisie", "Eredivisie"),
    ("greek_super_league", "Greek Super League"),
    ("liga_portugal", "Liga Portugal"),
    ("super_lig", "Süper Lig"),
)

SATELLITE_LEAGUE_DESCRIPTION = (
    "Belgian Pro League, Eredivisie, Greece, Portugal and Turkey"
)

SITE_LEAGUE_LIST_EN = "Eredivisie, Belgium, Turkey, Greece and Portugal"
SITE_LEAGUE_LIST_PT = "Eredivisie, Bélgica, Turquia, Grécia e Portugal"

CURATED_PLAYER_COUNT = 42

CROATIAN_CURATED_PLAYER_IDS = frozenset({"1065258", "89346", "243713"})


def league_is_active(league_source: str | None) -> bool:
    return bool(league_source) and league_source not in EXCLUDED_LEAGUE_SOURCES
