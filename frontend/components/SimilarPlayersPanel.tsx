"use client";

import type { PlayerOption, SimilarPlayersPayload } from "@/lib/api";

type Props = {
  referenceOptions: PlayerOption[];
  referencePlayerId: string;
  referencePool: string;
  candidatePool: string;
  affordableOnly: boolean;
  loading: boolean;
  data: SimilarPlayersPayload | null;
  error: string | null;
  poolLabels: Record<string, string>;
  onReferencePoolChange: (pool: string) => void;
  onCandidatePoolChange: (pool: string) => void;
  onReferenceChange: (playerId: string) => void;
  onAffordableToggle: (value: boolean) => void;
  onCompare: (playerId: string) => void;
};

function topDeltas(row: SimilarPlayersPayload["similar"][number]): string {
  const deltas = row.pillar_delta ?? {};
  const sorted = Object.entries(deltas).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]));
  return sorted
    .slice(0, 3)
    .map(([label, value]) => `${label} ${value > 0 ? "+" : ""}${value.toFixed(1)}`)
    .join(" · ");
}

export function SimilarPlayersPanel({
  referenceOptions,
  referencePlayerId,
  referencePool,
  candidatePool,
  affordableOnly,
  loading,
  data,
  error,
  poolLabels,
  onReferencePoolChange,
  onCandidatePoolChange,
  onReferenceChange,
  onAffordableToggle,
  onCompare,
}: Props) {
  return (
    <section className="player-card" style={{ marginBottom: "1.25rem" }}>
      <div className="section-label-row">
        <h2 className="section-label">
          <i className="fa-solid fa-people-arrows" aria-hidden="true" /> Similaridade — Seven Pillars
        </h2>
        <span className="muted" style={{ fontSize: "0.85rem" }}>
          Volume · Efficiency · Build-up · Chance creation · Productivity · Precision · Lethality
        </span>
      </div>

      <div className="filters compare-selectors" style={{ marginTop: "0.75rem" }}>
        <label className="filter-field">
          <span className="filter-label">Referência</span>
          <select value={referencePool} onChange={(e) => onReferencePoolChange(e.target.value)}>
            {Object.entries(poolLabels).map(([key, label]) => (
              <option key={key} value={key}>{label}</option>
            ))}
          </select>
        </label>
        <label className="filter-field compare-player-select">
          <span className="filter-label">Jogador de referência</span>
          <select value={referencePlayerId} onChange={(e) => onReferenceChange(e.target.value)}>
            {referenceOptions.map((o) => (
              <option key={o.player_id} value={o.player_id}>{o.label}</option>
            ))}
          </select>
        </label>
        <label className="filter-field">
          <span className="filter-label">Buscar similares em</span>
          <select value={candidatePool} onChange={(e) => onCandidatePoolChange(e.target.value)}>
            {Object.entries(poolLabels).map(([key, label]) => (
              <option key={key} value={key}>{label}</option>
            ))}
          </select>
        </label>
        <label className="filter-field" style={{ alignSelf: "end" }}>
          <span className="filter-label">&nbsp;</span>
          <label className="checkbox-inline">
            <input
              type="checkbox"
              checked={affordableOnly}
              onChange={(e) => onAffordableToggle(e.target.checked)}
            />
            {" "}≤35% do valor de mercado
          </label>
        </label>
      </div>

      {loading && <p className="muted" style={{ marginTop: "0.75rem" }}>Buscando jogadores similares…</p>}
      {error && <div className="error-box" style={{ marginTop: "0.75rem" }}>{error}</div>}

      {data && !loading && (
        <div style={{ marginTop: "1rem" }}>
          <p className="muted" style={{ marginBottom: "0.75rem" }}>
            Referência: <strong>{data.target.player_name}</strong> ({data.target.team} · {data.target.league})
            {data.target.market_value_display ? ` · MV ${data.target.market_value_display}` : ""}
          </p>
          {data.similar.length === 0 ? (
            <p className="muted">Nenhum jogador similar encontrado com os filtros atuais.</p>
          ) : (
            <div className="table-wrap">
              <table className="compare-radar-table">
                <thead>
                  <tr>
                    <th>Sim</th>
                    <th>Jogador</th>
                    <th>Clube</th>
                    <th>Liga</th>
                    <th>MV</th>
                    <th>xP pass</th>
                    <th>Principais deltas</th>
                    <th />
                  </tr>
                </thead>
                <tbody>
                  {data.similar.map((row) => (
                    <tr key={row.player_id}>
                      <td className="tabular"><strong>{row.similarity_pct}%</strong></td>
                      <td>{row.player_name}</td>
                      <td>{row.team}</td>
                      <td>{row.league ?? "—"}</td>
                      <td className="tabular">{row.market_value_display ?? "—"}</td>
                      <td className="tabular">
                        {row.xp_pass_rating != null ? Number(row.xp_pass_rating).toFixed(2) : "—"}
                      </td>
                      <td className="muted" style={{ fontSize: "0.82rem" }}>{topDeltas(row)}</td>
                      <td>
                        <button type="button" className="btn btn-secondary btn-sm" onClick={() => onCompare(row.player_id)}>
                          Comparar
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
