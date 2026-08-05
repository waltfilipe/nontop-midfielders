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

export const PLAYER_REPORT_CATEGORIES: PlayerReportCategory[] = [
  {
    id: "u23-breakout",
    title: "U23 — Breakout Promises",
    subtitle: "Emerging profiles under 23",
    description: "Young midfielders with standout pass profiles and room to scale impact.",
    accent: "#a78bfa",
    groups: [{ players: [] }],
  },
  {
    id: "blue-collar-24-30",
    title: "24–30 — Blue Collar Prospects",
    subtitle: "Prime-age engine room",
    description: "Reliable progression and pass-value profiles in the peak development window.",
    accent: "#38bdf8",
    groups: [{ players: [] }],
  },
  {
    id: "experience-30-plus",
    title: "30+ — Standout Experience",
    subtitle: "Veteran control & leadership",
    description: "Experienced midfield profiles with elite game management and passing authority.",
    accent: "#fbbf24",
    groups: [{ players: [] }],
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
  /** 1-based index within the age category. */
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
