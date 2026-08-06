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
    groups: [{
      players: [
      { playerId: "1405756", positionFamily: "midfielders", note: "Kees Smit (AZ Alkmaar) · age 20 · pass 0.81" },
      { playerId: "1888002", positionFamily: "midfielders", note: "Christ Inao Oulaï (Trabzonspor) · age 20 · pass 0.79" },
      { playerId: "1121400", positionFamily: "midfielders", note: "Luciano Valente (Feyenoord) · age 22 · pass 0.78" },
      { playerId: "1002007", positionFamily: "midfielders", note: "Giannis Konstantelias (PAOK) · age 23 · pass 0.77" },
      { playerId: "1124749", positionFamily: "midfielders", note: "Mathias Delorge (KAA Gent) · age 22 · pass 0.77" },
      { playerId: "1184054", positionFamily: "midfielders", note: "Kodai Sano (NEC Nijmegen) · age 22 · pass 0.77" },
      { playerId: "997165", positionFamily: "midfielders", note: "Bartuğ Elmaz (Fatih Karagümrük) · age 23 · pass 0.76" },
      { playerId: "1441117", positionFamily: "midfielders", note: "Tygo Land (FC Groningen) · age 20 · pass 0.76" },
      { playerId: "1153957", positionFamily: "midfielders", note: "Aleksandar Stanković (Club Brugge KV) · age 21 · pass 0.76" },
      { playerId: "1859920", positionFamily: "midfielders", note: "Sean Steur (AFC Ajax) · age 18 · pass 0.75" },
      { playerId: "1146018", positionFamily: "midfielders", note: "Paul Wanner (PSV Eindhoven) · age 20 · pass 0.73" },
      { playerId: "1065258", positionFamily: "midfielders", note: "Adrion Pajaziti (HNK Hajduk Split) · age 23 · pass 0.73" },
      { playerId: "1090328", positionFamily: "midfielders", note: "Stije Resink (FC Groningen) · age 23 · pass 0.72" },
      { playerId: "997022", positionFamily: "midfielders", note: "Diogo Nascimento (Olympiacos FC) · age 23 · pass 0.72" },
      { playerId: "1002146", positionFamily: "midfielders", note: "Maestro (Alanyaspor) · age 23 · pass 0.72" },
      ],
    }],
  },
  {
    id: "blue-collar-24-30",
    title: "24–30 — Blue Collar Prospects",
    subtitle: "Prime-age engine room",
    description: "Reliable progression and pass-value profiles in the peak development window.",
    accent: "#38bdf8",
    groups: [{
      players: [
      { playerId: "850816", positionFamily: "midfielders", note: "Joey Veerman (PSV Eindhoven) · age 27 · pass 0.83" },
      { playerId: "801025", positionFamily: "midfielders", note: "Bryan Heynen (KRC Genk) · age 29 · pass 0.83" },
      { playerId: "920684", positionFamily: "midfielders", note: "Jordan Holsgrove (Estoril Praia) · age 26 · pass 0.83" },
      { playerId: "907461", positionFamily: "midfielders", note: "Orkun Kökçü (Beşiktaş JK) · age 25 · pass 0.83" },
      { playerId: "1087316", positionFamily: "midfielders", note: "Enzo Barrenechea (Benfica) · age 25 · pass 0.82" },
      { playerId: "1000472", positionFamily: "midfielders", note: "Adem Zorgane (Royale Union Saint-Gilloise) · age 26 · pass 0.82" },
      { playerId: "754794", positionFamily: "midfielders", note: "Lucas Torreira (Galatasaray) · age 30 · pass 0.81" },
      { playerId: "859917", positionFamily: "midfielders", note: "Morten Hjulmand (Sporting CP) · age 27 · pass 0.81" },
      { playerId: "228364", positionFamily: "midfielders", note: "Fredrik Aursnes (Benfica) · age 30 · pass 0.81" },
      { playerId: "799216", positionFamily: "midfielders", note: "Pedro Chirivella (Panathinaikos FC) · age 29 · pass 0.80" },
      { playerId: "831697", positionFamily: "midfielders", note: "Ryotaro Ito (Sint-Truidense VV) · age 28 · pass 0.80" },
      { playerId: "840412", positionFamily: "midfielders", note: "Giannis Kosti (APO Levadiakos) · age 26 · pass 0.80" },
      { playerId: "989882", positionFamily: "midfielders", note: "Ramiz Zerrouki (FC Twente) · age 28 · pass 0.80" },
      { playerId: "279563", positionFamily: "midfielders", note: "Răzvan Marin (AEK Athens) · age 30 · pass 0.80" },
      { playerId: "830431", positionFamily: "midfielders", note: "Francisco Trincão (Sporting CP) · age 26 · pass 0.79" },
      ],
    }],
  },
  {
    id: "experience-30-plus",
    title: "30+ — Standout Experience",
    subtitle: "Veteran control & leadership",
    description: "Experienced midfield profiles with elite game management and passing authority.",
    accent: "#fbbf24",
    groups: [{
      players: [
      { playerId: "118085", positionFamily: "midfielders", note: "Hans Vanaken (Club Brugge KV) · age 33 · pass 0.83" },
      { playerId: "6562", positionFamily: "midfielders", note: "João Moutinho (Sporting Braga) · age 39 · pass 0.83" },
      { playerId: "138842", positionFamily: "midfielders", note: "Joris van Overeem (SC Heerenveen) · age 32 · pass 0.82" },
      { playerId: "89346", positionFamily: "midfielders", note: "Ljuban Crepulja (NK Slaven Belupo) · age 32 · pass 0.82" },
      { playerId: "243713", positionFamily: "midfielders", note: "Josip Mišić (GNK Dinamo Zagreb) · age 32 · pass 0.81" },
      { playerId: "180511", positionFamily: "midfielders", note: "Alexandru Maxim (Gaziantep FK) · age 36 · pass 0.80" },
      { playerId: "45853", positionFamily: "midfielders", note: "İlkay Gündoğan (Galatasaray) · age 35 · pass 0.79" },
      { playerId: "211116", positionFamily: "midfielders", note: "Andreas Bouchalakis (GFS Panetolikos) · age 33 · pass 0.78" },
      { playerId: "926560", positionFamily: "midfielders", note: "Hidemasa Morita (Sporting CP) · age 31 · pass 0.77" },
      { playerId: "243623", positionFamily: "midfielders", note: "Fred (Fenerbahçe) · age 33 · pass 0.75" },
      { playerId: "94290", positionFamily: "midfielders", note: "Hannes Van Der Bruggen (Cercle Brugge) · age 33 · pass 0.75" },
      { playerId: "307284", positionFamily: "midfielders", note: "Mario Lemina (Galatasaray) · age 32 · pass 0.74" },
      { playerId: "772685", positionFamily: "midfielders", note: "Juanpi Añor (NPS Volos) · age 32 · pass 0.73" },
      { playerId: "48243", positionFamily: "midfielders", note: "Genki Haraguchi (K. Beerschot V.A.) · age 36 · pass 0.73" },
      { playerId: "792155", positionFamily: "midfielders", note: "Jorge Pombo (AE Kifisia) · age 32 · pass 0.73" },
      ],
    }],
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
