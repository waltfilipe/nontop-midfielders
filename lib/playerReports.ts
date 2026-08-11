export type ReportPlayerRef = {
  playerId: string;
  positionFamily?: string;
  note?: string;
};

export type ReportPlayerGroup = {
  label?: string;
  players: ReportPlayerRef[];
};

export type PlayerReportCategory = {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  accent: string;
  groups: ReportPlayerGroup[];
};

const mid = "midfielders" as const;

function p(playerId: string, note?: string): ReportPlayerRef {
  return { playerId, positionFamily: mid, note };
}

export const PROFILE_ALL_GROUP = {
  id: "all",
  title: "All Players",
  subtitle: "Full curated pool",
  description: "All 42 midfielders ranked across five satellite European leagues.",
  accent: "#cbd5e1",
} as const;

export const PLAYER_REPORT_CATEGORIES: PlayerReportCategory[] = [
  {
    id: "u23-breakout",
    title: "U23 — Breakout Promises",
    subtitle: "Emerging profiles under 23",
    description: "Young midfielders with standout pass profiles across Eredivisie, Belgium, Turkey, Greece and Portugal.",
    accent: "#a78bfa",
    groups: [
      {
        label: "Top 10",
        players: [
          p("1405756"),
          p("1094538"),
          p("1888002"),
          p("1121400"),
          p("1184054"),
          p("1002007"),
          p("997165"),
          p("1441117"),
          p("1153957"),
          p("1859920"),
        ],
      },
      {
        label: "Extended watchlist",
        players: [
          p("997022"),
          p("1002146"),
          p("1188173"),
          p("1191892"),
        ],
      },
    ],
  },
  {
    id: "blue-collar-24-30",
    title: "24–30 — Blue Collar Prospects",
    subtitle: "Prime-age engine room",
    description: "Reliable progression and pass-value profiles in the peak development window.",
    accent: "#38bdf8",
    groups: [
      {
        label: "Top 10",
        players: [
          p("850816"),
          p("801025"),
          p("920684"),
          p("907461"),
          p("1000472"),
          p("1087316"),
          p("754794"),
          p("859917"),
          p("799216"),
          p("840412"),
        ],
      },
      {
        label: "Extended watchlist",
        players: [
          p("228364"),
          p("831697"),
          p("850404"),
          p("279563"),
          p("989882"),
        ],
      },
    ],
  },
  {
    id: "experience-30-plus",
    title: "30+ — Standout Experience",
    subtitle: "Veteran control & leadership",
    description: "Experienced midfield profiles with elite game management and passing authority.",
    accent: "#fbbf24",
    groups: [
      {
        label: "Top 10",
        players: [
          p("118085"),
          p("6562"),
          p("138842"),
          p("180511"),
          p("211116"),
          p("45853"),
          p("80465"),
          p("926560"),
        ],
      },
      {
        label: "Extended watchlist",
        players: [
          p("905455"),
          p("307284"),
          p("94290"),
          p("243623"),
          p("772685"),
        ],
      },
    ],
  },
];

export function allReportPlayerRefs(): ReportPlayerRef[] {
  const seen = new Set<string>();
  const out: ReportPlayerRef[] = [];
  for (const category of PLAYER_REPORT_CATEGORIES) {
    for (const group of category.groups) {
      for (const player of group.players) {
        if (seen.has(player.playerId)) continue;
        seen.add(player.playerId);
        out.push(player);
      }
    }
  }
  return out;
}

export function totalReportCount(): number {
  return allReportPlayerRefs().length;
}

export type EnrichedReportPlayer = ReportPlayerRef & {
  category: PlayerReportCategory;
  groupLabel?: string;
  /** 1-based index within the age category (1–15). */
  categoryIndex: number;
};

export function enrichedReportPlayers(): EnrichedReportPlayer[] {
  const out: EnrichedReportPlayer[] = [];
  for (const category of PLAYER_REPORT_CATEGORIES) {
    let categoryIndex = 0;
    for (const group of category.groups) {
      for (const player of group.players) {
        categoryIndex += 1;
        out.push({
          ...player,
          category,
          groupLabel: group.label,
          categoryIndex,
        });
      }
    }
  }
  return out;
}

export function playerIdsForProfileGroup(groupId: string): Set<string> {
  const category = PLAYER_REPORT_CATEGORIES.find((cat) => cat.id === groupId);
  if (!category) return new Set();
  const ids = new Set<string>();
  for (const group of category.groups) {
    for (const player of group.players) {
      ids.add(player.playerId);
    }
  }
  return ids;
}

export function profileGroupCounts(
  players: { player_id?: string | number | null }[],
): Record<string, number> {
  const available = new Set(players.map((p) => String(p.player_id)));
  const counts: Record<string, number> = {
    [PROFILE_ALL_GROUP.id]: players.length,
  };
  for (const category of PLAYER_REPORT_CATEGORIES) {
    const ids = playerIdsForProfileGroup(category.id);
    counts[category.id] = [...ids].filter((id) => available.has(id)).length;
  }
  return counts;
}
