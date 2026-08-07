import { PassLengthMix } from "@/components/PassLengthMix";
import { ConsistencyAccordion } from "@/components/ConsistencyAccordion";
import { ImpactAccordion } from "@/components/ImpactAccordion";
import { XpProfileBars } from "@/components/XpProfileBars";
import type { PlayerProfile } from "@/lib/api";
import { Tooltip } from "@/components/ui/Tooltip";
import { XP_INDEX_TIER_LABELS, xpIndexTierClass } from "@/lib/gradeColors";
import { INDEX_TOOLTIPS } from "@/lib/tooltips";

type Props = {
  profile: PlayerProfile;
  accent?: string;
  expandAll?: boolean;
};

export function ReportXpPanel({ profile, accent = "#a78bfa", expandAll = false }: Props) {
  const indices = (profile.xp_indices ?? []).filter((i) => i.tier);
  const consistency = indices.find((i) => i.key === "consistency");
  const impact = indices.find((i) => i.key === "impact");
  const other = indices.filter((i) => i.key !== "consistency" && i.key !== "impact");

  return (
    <div className="player-card xp-profile-card report-xp-card">
      <h3 className="section-label">xP Profile</h3>
      <XpProfileBars bars={profile.xp_bars} />

      {indices.length > 0 && (
        <div className="xp-indices-panel">
          <h4 className="section-label-sm">xP Indices</h4>
          <div className="xp-indices-list">
            {consistency && (
              <ConsistencyAccordion
                label={consistency.label}
                tier={consistency.tier}
                tierKey={consistency.tier_key ?? consistency.label}
                icon={consistency.icon ?? "fa-wave-square"}
                points={profile.xp_round_grades ?? []}
                accent={accent}
                expandAll={expandAll}
              />
            )}
            {impact && impact.components && impact.components.length > 0 && (
              <ImpactAccordion
                label={impact.label}
                tier={impact.tier}
                tierKey={impact.tier_key ?? impact.label}
                icon={impact.icon ?? "fa-crosshairs"}
                components={impact.components}
                expandAll={expandAll}
              />
            )}
            {impact && (!impact.components || impact.components.length === 0) && (
              <Tooltip content={INDEX_TOOLTIPS[impact.tier_key ?? impact.label] ?? ""} block>
                <div className={`xp-index-row ${xpIndexTierClass(impact.tier)}`}>
                  <span className="xp-index-row-icon">
                    <i className={`fa-solid ${impact.icon ?? "fa-crosshairs"}`} />
                  </span>
                  <span className="xp-index-row-name">{impact.label}</span>
                  <span className="xp-index-row-sep" aria-hidden="true" />
                  <span className="xp-index-row-val">{XP_INDEX_TIER_LABELS[impact.tier ?? "mid"] ?? impact.tier}</span>
                </div>
              </Tooltip>
            )}
            {other.map((item) => {
              const tip = INDEX_TOOLTIPS[item.tier_key ?? item.label] ?? INDEX_TOOLTIPS[item.label] ?? "";
              return (
                <Tooltip key={item.key} content={tip} block>
                  <div className={`xp-index-row ${xpIndexTierClass(item.tier)}`}>
                    <span className="xp-index-row-icon">
                      <i className={`fa-solid ${item.icon ?? "fa-circle"}`} />
                    </span>
                    <span className="xp-index-row-name">{item.label}</span>
                    <span className="xp-index-row-sep" aria-hidden="true" />
                    <span className="xp-index-row-val">{XP_INDEX_TIER_LABELS[item.tier ?? "mid"] ?? item.tier}</span>
                  </div>
                </Tooltip>
              );
            })}
          </div>
        </div>
      )}

      <PassLengthMix data={profile} />
    </div>
  );
}
