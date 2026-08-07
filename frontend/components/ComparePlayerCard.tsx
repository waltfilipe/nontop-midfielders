"use client";

import Image from "next/image";
import { PassLengthMix } from "@/components/PassLengthMix";
import { XpProfileBars } from "@/components/XpProfileBars";

type Props = {
  side: "a" | "b";
  player: Record<string, unknown>;
  heatmap?: string | null;
};

export function ComparePlayerCard({ side, player, heatmap }: Props) {
  const bars = (player.xp_bars as { key: string; label: string; value?: number }[]) ?? [];

  return (
    <div className={`player-card compare-side compare-side-${side}`}>
      <div className="identity-header">
        {player.photo_url ? (
          <div className="identity-photo-wrap">
            <Image src={String(player.photo_url)} alt="" width={58} height={58} className="identity-photo" unoptimized />
          </div>
        ) : (
          <div className="identity-photo-wrap">
            <div className="identity-photo-placeholder">{String(player.player_name ?? "?").charAt(0)}</div>
          </div>
        )}
        <div className="identity-head-text">
          <h3 className="identity-title" style={{ fontSize: "1rem" }}>{String(player.player_name)}</h3>
          <p className="identity-meta">{String(player.team)} · {String(player.position)}</p>
        </div>
      </div>
      <div className="metric-lines" style={{ marginTop: "0.5rem" }}>
        <div className="metric-line"><span>Valor</span><span className="stat-val">{String(player.market_value ?? "—")}</span></div>
        <div className="metric-line"><span>Idade</span><span className="stat-val">{String(player.age ?? "—")}</span></div>
        <div className="metric-line"><span>Minutos</span><span className="stat-val">{String(player.minutes ?? "—")}</span></div>
      </div>
      {heatmap && <img src={`data:image/png;base64,${heatmap}`} alt="Heatmap" className="heatmap-img" />}
      <div style={{ marginTop: "0.75rem" }}>
        <XpProfileBars bars={bars} />
      </div>
      <PassLengthMix data={{
        long_pass_share_pct: player.long_pass_share_pct as number | null | undefined,
        long_pass_share_ref_avg_pct: player.long_pass_share_ref_avg_pct as number | null | undefined,
        long_pass_share_pctile: player.long_pass_share_pctile as number | null | undefined,
      }} />
    </div>
  );
}
