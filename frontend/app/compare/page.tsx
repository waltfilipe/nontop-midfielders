"use client";

import { Suspense, useCallback, useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { CompareCenter } from "@/components/CompareCenter";
import { ComparePlayerCard } from "@/components/ComparePlayerCard";
import { LoadingState } from "@/components/LoadingState";
import { PageHero } from "@/components/PageHero";
import { SimilarPlayersPanel } from "@/components/SimilarPlayersPanel";
import {
  getCompare,
  getSimilarMeta,
  getSimilarOptions,
  getSimilarPlayers,
  type ComparePayload,
  type PlayerOption,
  type SimilarPlayersPayload,
} from "@/lib/api";

const DEFAULT_REFERENCE_POOL = "top5";
const DEFAULT_CANDIDATE_POOL = "satellite";

export default function ComparePage() {
  return (
    <Suspense fallback={<LoadingState message="Carregando compare…" />}>
      <CompareContent />
    </Suspense>
  );
}

function CompareContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [poolLabels, setPoolLabels] = useState<Record<string, string>>({
    satellite: "Ligas satélite (6)",
    top5: "Top 5 europeias",
    all: "Todas",
  });
  const [referencePool, setReferencePool] = useState(DEFAULT_REFERENCE_POOL);
  const [candidatePool, setCandidatePool] = useState(DEFAULT_CANDIDATE_POOL);
  const [referenceOptions, setReferenceOptions] = useState<PlayerOption[]>([]);
  const [compareOptions, setCompareOptions] = useState<PlayerOption[]>([]);
  const [referencePlayerId, setReferencePlayerId] = useState("");
  const [playerA, setPlayerA] = useState(searchParams.get("a") ?? "");
  const [playerB, setPlayerB] = useState(searchParams.get("b") ?? "");
  const [affordableOnly, setAffordableOnly] = useState(false);
  const [similarData, setSimilarData] = useState<SimilarPlayersPayload | null>(null);
  const [compareData, setCompareData] = useState<ComparePayload | null>(null);
  const [similarLoading, setSimilarLoading] = useState(false);
  const [compareLoading, setCompareLoading] = useState(false);
  const [similarError, setSimilarError] = useState<string | null>(null);
  const [compareError, setCompareError] = useState<string | null>(null);

  const syncUrl = useCallback((a: string, b: string) => {
    const params = new URLSearchParams();
    if (a) params.set("a", a);
    if (b) params.set("b", b);
    const qs = params.toString();
    router.replace(qs ? `/compare?${qs}` : "/compare", { scroll: false });
  }, [router]);

  useEffect(() => {
    getSimilarMeta()
      .then((meta) => {
        const labels: Record<string, string> = {};
        for (const pool of meta.pools) {
          const count = meta.pool_counts[pool.key];
          labels[pool.key] = count != null ? `${pool.label} (${count})` : pool.label;
        }
        setPoolLabels(labels);
      })
      .catch(() => { /* defaults */ });
  }, []);

  useEffect(() => {
    getSimilarOptions(referencePool)
      .then((res) => {
        setReferenceOptions(res.options);
        const fromUrl = searchParams.get("ref");
        const initial = fromUrl && res.options.some((o) => o.player_id === fromUrl)
          ? fromUrl
          : res.options[0]?.player_id ?? "";
        setReferencePlayerId((prev) => prev || initial);
        if (!playerA && initial) setPlayerA(initial);
      })
      .catch(() => setSimilarError("Não foi possível carregar jogadores de referência."));
  }, [referencePool, searchParams, playerA]);

  useEffect(() => {
    getSimilarOptions("all")
      .then((res) => setCompareOptions(res.options))
      .catch(() => setCompareError("Backend indisponível"));
  }, []);

  useEffect(() => {
    if (!referencePlayerId) return;
    setSimilarLoading(true);
    setSimilarError(null);
    getSimilarPlayers(referencePlayerId, {
      candidate_pool: candidatePool,
      reference_pool: referencePool,
      top_k: 12,
      max_market_value_pct: affordableOnly ? 0.35 : undefined,
    })
      .then(setSimilarData)
      .catch((e) => setSimilarError(e instanceof Error ? e.message : "Erro ao buscar similares"))
      .finally(() => setSimilarLoading(false));
  }, [referencePlayerId, candidatePool, referencePool, affordableOnly]);

  useEffect(() => {
    if (!playerA || !playerB || playerA === playerB) {
      setCompareData(null);
      return;
    }
    setCompareLoading(true);
    setCompareError(null);
    getCompare(playerA, playerB)
      .then(setCompareData)
      .catch((e) => setCompareError(e instanceof Error ? e.message : "Erro na comparação"))
      .finally(() => setCompareLoading(false));
    syncUrl(playerA, playerB);
  }, [playerA, playerB, syncUrl]);

  const compareSelectOptions = useMemo(() => {
    const seen = new Set<string>();
    const merged: PlayerOption[] = [];
    for (const list of [compareOptions, referenceOptions]) {
      for (const opt of list) {
        if (seen.has(opt.player_id)) continue;
        seen.add(opt.player_id);
        merged.push(opt);
      }
    }
    return merged;
  }, [compareOptions, referenceOptions]);

  const handleCompareFromSimilar = (candidateId: string) => {
    setPlayerA(referencePlayerId);
    setPlayerB(candidateId);
    const el = document.getElementById("compare-head-to-head");
    el?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <div className="container">
      <PageHero
        title="Compare"
        subtitle="Encontre jogadores similares com Seven Pillars e compare dois perfis lado a lado — satélite ↔ Top 5."
        icon="fa-scale-balanced"
      />

      <SimilarPlayersPanel
        referenceOptions={referenceOptions}
        referencePlayerId={referencePlayerId}
        referencePool={referencePool}
        candidatePool={candidatePool}
        affordableOnly={affordableOnly}
        loading={similarLoading}
        data={similarData}
        error={similarError}
        poolLabels={poolLabels}
        onReferencePoolChange={setReferencePool}
        onCandidatePoolChange={setCandidatePool}
        onReferenceChange={setReferencePlayerId}
        onAffordableToggle={setAffordableOnly}
        onCompare={handleCompareFromSimilar}
      />

      <section id="compare-head-to-head" className="player-card">
        <h2 className="section-label" style={{ marginBottom: "0.75rem" }}>
          <i className="fa-solid fa-chart-radar" aria-hidden="true" /> Comparação direta
        </h2>
        <div className="filters compare-selectors" style={{ marginBottom: 0 }}>
          <label className="filter-field compare-player-select">
            <span className="filter-label">Jogador A</span>
            <select value={playerA} onChange={(e) => setPlayerA(e.target.value)}>
              {compareSelectOptions.map((o) => (
                <option key={o.player_id} value={o.player_id}>{o.label}</option>
              ))}
            </select>
          </label>
          <span className="compare-vs muted">vs</span>
          <label className="filter-field compare-player-select">
            <span className="filter-label">Jogador B</span>
            <select value={playerB} onChange={(e) => setPlayerB(e.target.value)}>
              {compareSelectOptions
                .filter((o) => o.player_id !== playerA)
                .map((o) => (
                  <option key={o.player_id} value={o.player_id}>{o.label}</option>
                ))}
            </select>
          </label>
        </div>
      </section>

      {compareLoading && <LoadingState message="Carregando comparação…" />}
      {compareError && <div className="error-box">{compareError}</div>}

      {compareData && !compareLoading && (
        <div className="compare-layout">
          <ComparePlayerCard
            side="a"
            player={compareData.player_a}
            heatmap={compareData.heatmap_a_b64}
          />
          <div className="player-card" style={{ padding: "1rem" }}>
            <CompareCenter pillars={compareData.pillars} passGrid={compareData.pass_grid} />
          </div>
          <ComparePlayerCard
            side="b"
            player={compareData.player_b}
            heatmap={compareData.heatmap_b_b64}
          />
        </div>
      )}
    </div>
  );
}
