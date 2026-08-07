# Similaridade Top 5 ↔ ligas satélite (offline)

Compara meio-campistas das **6 ligas satélite** (Bélgica, Croácia, Eredivisie, Grécia, Portugal, Turquia) com as **Top 5 europeias** (Premier League, Bundesliga, Ligue 1, La Liga, Serie A).

## Métodos

| Método | Descrição | Melhor para |
|---|---|---|
| **seven_pillars** | 7 notas de scout (Volume, Efficiency, Build-up, Chance creation, Productivity, Precision, Lethality) | Alinhar com a UI do Pass Scout / relatórios |
| **alt_metrics** | Perfil de estilo (longos, progressivos, xPV, COE) | Encontrar jogadores com *jeito de jogo* parecido |
| **hybrid** | 65% alt_metrics + 35% seven_pillars | Equilíbrio entre estilo e nota de scout |

- Pool satélite elegível (7 pilares): **251**
- Pool Top 5 elegível (7 pilares): **251**

---

## A) Top 5 → satélite

Referência de elite → alternativas mais baratas nas 6 ligas.

### Rodri (Manchester City · Premier League)
- MV: **€55.00M** · xP pass: 0.8212
- Pilares: Volume 9.0 · Efficiency 8.3 · Build-up 9.0 · Chance creation 8.1 · Productivity 8.9 · Precision 8.7 · Lethality 8.5

#### Seven pillars (scout display scores)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 95.3% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 95.0% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |
| 94.1% | Josip Mišić | GNK Dinamo Zagreb | Croatian League | — | 0.8114 |
| 93.7% | Adem Zorgane | Royale Union Saint-Gilloise | Belgian Pro League | — | 0.816 |
| 92.4% | Jordan Holsgrove | Estoril Praia | Liga Portugal | — | 0.8269 |
| 92.2% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |
| 91.8% | Orkun Kökçü | Beşiktaş JK | Süper Lig | — | 0.8301 |
| 91.6% | Giannis Kosti | APO Levadiakos | Greek Super League | — | 0.8038 |

#### Alt metrics (style / rate profile)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 81.9% | Jordan Holsgrove | Estoril Praia | Liga Portugal | — | 0.8269 |
| 76.9% | Enzo Barrenechea | Benfica | Liga Portugal | — | 0.8204 |
| 76.5% | João Moutinho | Sporting Braga | Liga Portugal | — | 0.8315 |
| 71.0% | Giannis Kosti | APO Levadiakos | Greek Super League | — | 0.8038 |
| 70.8% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 70.8% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |
| 70.0% | Lucas Torreira | Galatasaray | Süper Lig | — | 0.8139 |
| 69.9% | Morten Hjulmand | Sporting CP | Liga Portugal | — | 0.8095 |

#### Hybrid (65% alt + 35% pillars)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 100.0% | Jordan Holsgrove | Estoril Praia | Liga Portugal | — | 0.8269 |
| 99.6% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |
| 99.2% | Giannis Kosti | APO Levadiakos | Greek Super League | — | 0.8038 |
| 98.8% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 98.4% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 98.0% | João Moutinho | Sporting Braga | Liga Portugal | — | 0.8315 |
| 97.6% | Josip Mišić | GNK Dinamo Zagreb | Croatian League | — | 0.8114 |
| 97.2% | Lucas Torreira | Galatasaray | Süper Lig | — | 0.8139 |

#### Alternativas ≤35% do MV (seven_pillars)

| Sim | Jogador | Clube | Liga | MV |
|---:|---|---|---|---:|
| 95.3% | Bryan Heynen | KRC Genk | — | — |
| 95.0% | Mattéo Guendouzi | Fenerbahçe | — | — |
| 94.1% | Josip Mišić | GNK Dinamo Zagreb | — | — |
| 93.7% | Adem Zorgane | Royale Union Saint-Gilloise | — | — |
| 92.4% | Jordan Holsgrove | Estoril Praia | — | — |

### Vitinha (Paris Saint-Germain · Ligue 1)
- MV: **€140.00M** · xP pass: 0.8319
- Pilares: Volume 9.0 · Efficiency 8.8 · Build-up 8.8 · Chance creation 8.5 · Productivity 9.0 · Precision 9.0 · Lethality 8.7

#### Seven pillars (scout display scores)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 97.3% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 95.6% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 95.4% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |
| 94.2% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |
| 92.1% | Josip Mišić | GNK Dinamo Zagreb | Croatian League | — | 0.8114 |
| 92.0% | Alexandru Maxim | Gaziantep FK | Süper Lig | — | 0.8005 |
| 92.0% | Orkun Kökçü | Beşiktaş JK | Süper Lig | — | 0.8301 |
| 91.6% | Adem Zorgane | Royale Union Saint-Gilloise | Belgian Pro League | — | 0.816 |

#### Alt metrics (style / rate profile)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 64.1% | Jordan Holsgrove | Estoril Praia | Liga Portugal | — | 0.8269 |
| 63.6% | João Moutinho | Sporting Braga | Liga Portugal | — | 0.8315 |
| 62.2% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 61.7% | Enzo Barrenechea | Benfica | Liga Portugal | — | 0.8204 |
| 58.9% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |
| 57.8% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 57.1% | Lucas Torreira | Galatasaray | Süper Lig | — | 0.8139 |
| 56.0% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |

#### Hybrid (65% alt + 35% pillars)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 100.0% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 99.6% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 99.2% | Jordan Holsgrove | Estoril Praia | Liga Portugal | — | 0.8269 |
| 98.8% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |
| 98.4% | João Moutinho | Sporting Braga | Liga Portugal | — | 0.8315 |
| 98.0% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |
| 97.6% | Josip Mišić | GNK Dinamo Zagreb | Croatian League | — | 0.8114 |
| 97.2% | Giannis Kosti | APO Levadiakos | Greek Super League | — | 0.8038 |

#### Alternativas ≤35% do MV (seven_pillars)

| Sim | Jogador | Clube | Liga | MV |
|---:|---|---|---|---:|
| 97.3% | Bryan Heynen | KRC Genk | — | — |
| 95.6% | Hans Vanaken | Club Brugge KV | — | — |
| 95.4% | Joey Veerman | PSV Eindhoven | — | — |
| 94.2% | Mattéo Guendouzi | Fenerbahçe | — | — |
| 92.1% | Josip Mišić | GNK Dinamo Zagreb | — | — |

### Joshua Kimmich (FC Bayern München · Bundesliga)
- MV: **€35.00M** · xP pass: 0.832
- Pilares: Volume 9.0 · Efficiency 8.8 · Build-up 9.0 · Chance creation 9.0 · Productivity 9.0 · Precision 9.0 · Lethality 8.9

#### Seven pillars (scout display scores)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 98.4% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |
| 97.8% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 96.0% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 93.2% | Orkun Kökçü | Beşiktaş JK | Süper Lig | — | 0.8301 |
| 91.9% | Alexandru Maxim | Gaziantep FK | Süper Lig | — | 0.8005 |
| 91.3% | Adem Zorgane | Royale Union Saint-Gilloise | Belgian Pro League | — | 0.816 |
| 90.8% | Fredrik Aursnes | Benfica | Liga Portugal | — | 0.8018 |
| 90.7% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |

#### Alt metrics (style / rate profile)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 69.4% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 66.3% | João Moutinho | Sporting Braga | Liga Portugal | — | 0.8315 |
| 65.3% | Jordan Holsgrove | Estoril Praia | Liga Portugal | — | 0.8269 |
| 64.4% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 64.1% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |
| 63.0% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |
| 61.0% | Enzo Barrenechea | Benfica | Liga Portugal | — | 0.8204 |
| 57.5% | Giannis Kosti | APO Levadiakos | Greek Super League | — | 0.8038 |

#### Hybrid (65% alt + 35% pillars)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 100.0% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 99.6% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 99.2% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |
| 98.8% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |
| 98.4% | Jordan Holsgrove | Estoril Praia | Liga Portugal | — | 0.8269 |
| 98.0% | João Moutinho | Sporting Braga | Liga Portugal | — | 0.8315 |
| 97.6% | Josip Mišić | GNK Dinamo Zagreb | Croatian League | — | 0.8114 |
| 97.2% | Giannis Kosti | APO Levadiakos | Greek Super League | — | 0.8038 |

#### Alternativas ≤35% do MV (seven_pillars)

| Sim | Jogador | Clube | Liga | MV |
|---:|---|---|---|---:|
| 98.4% | Joey Veerman | PSV Eindhoven | — | — |
| 97.8% | Hans Vanaken | Club Brugge KV | — | — |
| 96.0% | Bryan Heynen | KRC Genk | — | — |
| 93.2% | Orkun Kökçü | Beşiktaş JK | — | — |
| 91.9% | Alexandru Maxim | Gaziantep FK | — | — |

### Bruno Fernandes (Manchester United · Premier League)
- MV: **€35.00M** · xP pass: 0.8005
- Pilares: Volume 9.0 · Efficiency 8.3 · Build-up 9.0 · Chance creation 9.0 · Productivity 8.5 · Precision 6.9 · Lethality 9.0

#### Seven pillars (scout display scores)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 94.4% | Ryotaro Ito | Sint-Truidense VV | Belgian Pro League | — | 0.7953 |
| 93.5% | Joris van Overeem | SC Heerenveen | Eredivisie | — | 0.8236 |
| 90.1% | Orkun Kökçü | Beşiktaş JK | Süper Lig | — | 0.8301 |
| 89.9% | Tiago Dantas | HNK Rijeka | Croatian League | — | 0.7844 |
| 89.0% | Luciano Valente | Feyenoord | Eredivisie | — | 0.7748 |
| 88.7% | Adem Zorgane | Royale Union Saint-Gilloise | Belgian Pro League | — | 0.816 |
| 88.7% | Yassine Titraoui | RC Sporting Charleroi | Belgian Pro League | — | 0.7822 |
| 88.3% | Alexandru Maxim | Gaziantep FK | Süper Lig | — | 0.8005 |

#### Alt metrics (style / rate profile)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 84.2% | Joris van Overeem | SC Heerenveen | Eredivisie | — | 0.8236 |
| 80.4% | Orkun Kökçü | Beşiktaş JK | Süper Lig | — | 0.8301 |
| 77.8% | Ryotaro Ito | Sint-Truidense VV | Belgian Pro League | — | 0.7953 |
| 77.7% | Josip Mišić | GNK Dinamo Zagreb | Croatian League | — | 0.8114 |
| 77.6% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 77.1% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |
| 77.1% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 77.1% | Alexandru Maxim | Gaziantep FK | Süper Lig | — | 0.8005 |

#### Hybrid (65% alt + 35% pillars)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 100.0% | Joris van Overeem | SC Heerenveen | Eredivisie | — | 0.8236 |
| 99.6% | Ryotaro Ito | Sint-Truidense VV | Belgian Pro League | — | 0.7953 |
| 99.2% | Orkun Kökçü | Beşiktaş JK | Süper Lig | — | 0.8301 |
| 98.8% | Josip Mišić | GNK Dinamo Zagreb | Croatian League | — | 0.8114 |
| 98.4% | Alexandru Maxim | Gaziantep FK | Süper Lig | — | 0.8005 |
| 98.0% | Adem Zorgane | Royale Union Saint-Gilloise | Belgian Pro League | — | 0.816 |
| 97.6% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 97.2% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |

#### Alternativas ≤35% do MV (seven_pillars)

| Sim | Jogador | Clube | Liga | MV |
|---:|---|---|---|---:|
| 94.4% | Ryotaro Ito | Sint-Truidense VV | — | — |
| 93.5% | Joris van Overeem | SC Heerenveen | — | — |
| 90.1% | Orkun Kökçü | Beşiktaş JK | — | — |
| 89.9% | Tiago Dantas | HNK Rijeka | — | — |
| 89.0% | Luciano Valente | Feyenoord | — | — |

### Pedri (FC Barcelona · La Liga)
- MV: **€150.00M** · xP pass: 0.8309
- Pilares: Volume 9.0 · Efficiency 8.8 · Build-up 9.0 · Chance creation 9.0 · Productivity 8.9 · Precision 8.9 · Lethality 8.9

#### Seven pillars (scout display scores)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 98.5% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |
| 97.3% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 96.3% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 94.1% | Orkun Kökçü | Beşiktaş JK | Süper Lig | — | 0.8301 |
| 92.6% | Alexandru Maxim | Gaziantep FK | Süper Lig | — | 0.8005 |
| 91.9% | Adem Zorgane | Royale Union Saint-Gilloise | Belgian Pro League | — | 0.816 |
| 91.3% | Fredrik Aursnes | Benfica | Liga Portugal | — | 0.8018 |
| 90.8% | Răzvan Marin | AEK Athens | Greek Super League | — | 0.798 |

#### Alt metrics (style / rate profile)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 80.3% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 75.6% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |
| 74.9% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 73.8% | Jordan Holsgrove | Estoril Praia | Liga Portugal | — | 0.8269 |
| 73.8% | João Moutinho | Sporting Braga | Liga Portugal | — | 0.8315 |
| 73.4% | Enzo Barrenechea | Benfica | Liga Portugal | — | 0.8204 |
| 70.2% | Lucas Torreira | Galatasaray | Süper Lig | — | 0.8139 |
| 68.7% | Giannis Kosti | APO Levadiakos | Greek Super League | — | 0.8038 |

#### Hybrid (65% alt + 35% pillars)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 100.0% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 99.6% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 99.2% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |
| 98.8% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |
| 98.4% | Jordan Holsgrove | Estoril Praia | Liga Portugal | — | 0.8269 |
| 98.0% | João Moutinho | Sporting Braga | Liga Portugal | — | 0.8315 |
| 97.6% | Josip Mišić | GNK Dinamo Zagreb | Croatian League | — | 0.8114 |
| 97.2% | Giannis Kosti | APO Levadiakos | Greek Super League | — | 0.8038 |

#### Alternativas ≤35% do MV (seven_pillars)

| Sim | Jogador | Clube | Liga | MV |
|---:|---|---|---|---:|
| 98.5% | Joey Veerman | PSV Eindhoven | — | — |
| 97.3% | Hans Vanaken | Club Brugge KV | — | — |
| 96.3% | Bryan Heynen | KRC Genk | — | — |
| 94.1% | Orkun Kökçü | Beşiktaş JK | — | — |
| 92.6% | Alexandru Maxim | Gaziantep FK | — | — |

### Manuel Locatelli (Juventus · Serie A)
- MV: **€25.00M** · xP pass: 0.832
- Pilares: Volume 9.0 · Efficiency 8.8 · Build-up 9.0 · Chance creation 8.8 · Productivity 8.9 · Precision 8.9 · Lethality 9.0

#### Seven pillars (scout display scores)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 98.3% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |
| 97.2% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 96.5% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 93.9% | Orkun Kökçü | Beşiktaş JK | Süper Lig | — | 0.8301 |
| 92.3% | Adem Zorgane | Royale Union Saint-Gilloise | Belgian Pro League | — | 0.816 |
| 92.3% | Alexandru Maxim | Gaziantep FK | Süper Lig | — | 0.8005 |
| 91.3% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |
| 91.1% | Fredrik Aursnes | Benfica | Liga Portugal | — | 0.8018 |

#### Alt metrics (style / rate profile)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 79.5% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |
| 70.6% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 68.6% | Orkun Kökçü | Beşiktaş JK | Süper Lig | — | 0.8301 |
| 68.6% | Joris van Overeem | SC Heerenveen | Eredivisie | — | 0.8236 |
| 67.9% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 63.1% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |
| 61.2% | Adem Zorgane | Royale Union Saint-Gilloise | Belgian Pro League | — | 0.816 |
| 61.1% | Ljuban Crepulja | NK Slaven Belupo | Croatian League | — | 0.8182 |

#### Hybrid (65% alt + 35% pillars)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 100.0% | Joey Veerman | PSV Eindhoven | Eredivisie | — | 0.8317 |
| 99.6% | Hans Vanaken | Club Brugge KV | Belgian Pro League | — | 0.8317 |
| 99.2% | Orkun Kökçü | Beşiktaş JK | Süper Lig | — | 0.8301 |
| 98.8% | Bryan Heynen | KRC Genk | Belgian Pro League | — | 0.8311 |
| 98.4% | Adem Zorgane | Royale Union Saint-Gilloise | Belgian Pro League | — | 0.816 |
| 98.0% | Mattéo Guendouzi | Fenerbahçe | Süper Lig | — | 0.8305 |
| 97.6% | Joris van Overeem | SC Heerenveen | Eredivisie | — | 0.8236 |
| 97.2% | Josip Mišić | GNK Dinamo Zagreb | Croatian League | — | 0.8114 |

#### Alternativas ≤35% do MV (seven_pillars)

| Sim | Jogador | Clube | Liga | MV |
|---:|---|---|---|---:|
| 98.3% | Joey Veerman | PSV Eindhoven | — | — |
| 97.2% | Bryan Heynen | KRC Genk | — | — |
| 96.5% | Hans Vanaken | Club Brugge KV | — | — |
| 93.9% | Orkun Kökçü | Beşiktaş JK | — | — |
| 92.3% | Adem Zorgane | Royale Union Saint-Gilloise | — | — |

### João Neves (Paris Saint-Germain · Ligue 1)
- MV: **€140.00M** · xP pass: 0.7409
- Pilares: Volume 8.1 · Efficiency 7.9 · Build-up 7.1 · Chance creation 8.0 · Productivity 7.5 · Precision 8.2 · Lethality 5.8

#### Seven pillars (scout display scores)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 88.2% | İlkay Gündoğan | Galatasaray | Süper Lig | — | 0.7886 |
| 87.7% | Antoine Makoumbou | Samsunspor | Süper Lig | — | 0.7704 |
| 85.3% | Iker Pozo | HNK Gorica | Croatian League | — | 0.7493 |
| 83.1% | Nicolas Janvier | Alanyaspor | Süper Lig | — | 0.7191 |
| 82.7% | Aleksandar Stanković | Club Brugge KV | Belgian Pro League | — | 0.7548 |
| 81.4% | Ismaël Bennacer | GNK Dinamo Zagreb | Croatian League | — | 0.7641 |
| 78.6% | Lincoln | FC Alverca | Liga Portugal | — | 0.6927 |
| 77.2% | Paul Wanner | PSV Eindhoven | Eredivisie | — | 0.7346 |

#### Alt metrics (style / rate profile)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 80.4% | İlkay Gündoğan | Galatasaray | Süper Lig | — | 0.7886 |
| 79.3% | Florian Grillitsch | Sporting Braga | Liga Portugal | — | 0.7061 |
| 76.2% | Adriano Firmino | Santa Clara | Liga Portugal | — | 0.7022 |
| 75.3% | Beni Mukendi | Vitória SC | Liga Portugal | — | 0.7055 |
| 73.5% | Soualiho Meïté | PAOK | Greek Super League | — | 0.6949 |
| 73.1% | Tim Jabol-Folcarelli | Trabzonspor | Süper Lig | — | 0.7318 |
| 72.1% | Adam Gnezda Čerin | Panathinaikos FC | Greek Super League | — | 0.7382 |
| 70.7% | Maestro | Alanyaspor | Süper Lig | — | 0.7186 |

#### Hybrid (65% alt + 35% pillars)

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 100.0% | İlkay Gündoğan | Galatasaray | Süper Lig | — | 0.7886 |
| 99.6% | Adriano Firmino | Santa Clara | Liga Portugal | — | 0.7022 |
| 99.2% | Tim Jabol-Folcarelli | Trabzonspor | Süper Lig | — | 0.7318 |
| 98.8% | Adam Gnezda Čerin | Panathinaikos FC | Greek Super League | — | 0.7382 |
| 98.4% | Morten Hjulmand | Sporting CP | Liga Portugal | — | 0.8095 |
| 98.0% | Florian Grillitsch | Sporting Braga | Liga Portugal | — | 0.7061 |
| 97.6% | Beni Mukendi | Vitória SC | Liga Portugal | — | 0.7055 |
| 97.2% | Antoine Makoumbou | Samsunspor | Süper Lig | — | 0.7704 |

#### Alternativas ≤35% do MV (seven_pillars)

| Sim | Jogador | Clube | Liga | MV |
|---:|---|---|---|---:|
| 88.2% | İlkay Gündoğan | Galatasaray | — | — |
| 87.7% | Antoine Makoumbou | Samsunspor | — | — |
| 85.3% | Iker Pozo | HNK Gorica | — | — |
| 83.1% | Nicolas Janvier | Alanyaspor | — | — |
| 82.7% | Aleksandar Stanković | Club Brugge KV | — | — |

---

## B) Satélite → Top 5

Jogador das 6 ligas → comps de referência na elite europeia.

### Kees Smit (AZ Alkmaar · Eredivisie)
- MV: **—** · xP pass: 0.8079

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 93.7% | Exequiel Palacios | Bayer 04 Leverkusen | Bundesliga | €25.00M | 0.8189 |
| 92.9% | Federico Valverde | Real Madrid | La Liga | €90.00M | 0.7963 |
| 91.1% | Pablo Fornals | Real Betis | La Liga | €8.00M | 0.7768 |
| 90.5% | Pierre-Emile Højbjerg | Olympique de Marseille | Ligue 1 | €15.00M | 0.81 |
| 90.1% | Frenkie de Jong | FC Barcelona | La Liga | €35.00M | 0.8241 |
| 90.0% | Fabián Ruiz | Paris Saint-Germain | Ligue 1 | €30.00M | 0.8157 |
| 89.8% | Nicolò Fagioli | Fiorentina | Serie A | €16.00M | 0.7837 |
| 89.6% | Valentin Rongier | Stade Rennais | Ligue 1 | €8.00M | 0.7978 |

### Christ Inao Oulaï (Trabzonspor · Süper Lig)
- MV: **—** · xP pass: 0.7871

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 93.1% | Máximo Perrone | Como | Serie A | €35.00M | 0.7917 |
| 92.4% | Hakan Çalhanoğlu | Inter | Serie A | €16.00M | 0.7939 |
| 92.3% | Lucas Da Cunha | Como | Serie A | €20.00M | 0.7678 |
| 91.3% | Dominik Szoboszlai | Liverpool FC | Premier League | €100.00M | 0.795 |
| 90.9% | Tyler Morton | Olympique Lyonnais | Ligue 1 | €30.00M | 0.7501 |
| 90.9% | Federico Valverde | Real Madrid | La Liga | €90.00M | 0.7963 |
| 90.8% | Maxime López | Paris FC | Ligue 1 | €5.00M | 0.8117 |
| 90.4% | Koke | Atlético Madrid | La Liga | €5.00M | 0.8042 |

### Luciano Valente (Feyenoord · Eredivisie)
- MV: **—** · xP pass: 0.7748

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 93.6% | Nicolò Barella | Inter | Serie A | €50.00M | 0.7818 |
| 92.4% | Bruno Guimarães | Newcastle United | Premier League | €70.00M | 0.7897 |
| 91.8% | Pablo Fornals | Real Betis | La Liga | €8.00M | 0.7768 |
| 91.6% | Nadiem Amiri | 1. FSV Mainz 05 | Bundesliga | €17.00M | 0.7576 |
| 91.0% | Pablo Barrios | Atlético Madrid | La Liga | €55.00M | 0.7484 |
| 89.7% | Arda Güler | Real Madrid | La Liga | €90.00M | 0.7618 |
| 89.3% | Granit Xhaka | Sunderland | Premier League | €8.00M | 0.7609 |
| 88.7% | Mario Pašalić | Atalanta | Serie A | €6.00M | 0.7561 |

### Giannis Konstantelias (PAOK · Greek Super League)
- MV: **—** · xP pass: 0.7661

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 77.6% | Giovani Lo Celso | Real Betis | La Liga | €8.00M | 0.7358 |
| 77.6% | Rayan Cherki | Manchester City | Premier League | €90.00M | 0.7588 |
| 72.1% | Dani Olmo | FC Barcelona | La Liga | €60.00M | 0.6836 |
| 72.0% | Henrikh Mkhitaryan | Inter | Serie A | €3.00M | 0.7161 |
| 71.4% | Petar Sučić | Inter | Serie A | €45.00M | 0.702 |
| 70.5% | Azzedine Ounahi | Girona FC | La Liga | €18.00M | 0.7384 |
| 70.1% | Moi Gómez | Osasuna | La Liga | €1.50M | 0.7441 |
| 69.5% | Carlos Soler | Real Sociedad | La Liga | €7.00M | 0.698 |

### Mathias Delorge (KAA Gent · Belgian Pro League)
- MV: **—** · xP pass: 0.7713

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 84.8% | Senne Lynen | SV Werder Bremen | Bundesliga | €8.00M | 0.7659 |
| 82.9% | Nikola Moro | Bologna | Serie A | €7.00M | 0.7545 |
| 82.0% | Laurent Abergel | Lorient | Ligue 1 | €1.80M | 0.7744 |
| 81.8% | Nemanja Matić | Sassuolo | Serie A | €1.60M | 0.7416 |
| 80.0% | Billy Gilmour | SSC Napoli | Serie A | €20.00M | 0.753 |
| 79.8% | Hugo Sotelo | Celta Vigo | La Liga | €5.00M | 0.7887 |
| 77.9% | Leon Avdullahu | TSG Hoffenheim | Bundesliga | €30.00M | 0.8077 |
| 77.4% | Aurélien Tchouaméni | Real Madrid | La Liga | €70.00M | 0.8025 |

### Kodai Sano (NEC Nijmegen · Eredivisie)
- MV: **—** · xP pass: 0.7675

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 91.0% | Enzo Fernández | Chelsea | Premier League | €100.00M | 0.763 |
| 89.0% | Declan Rice | Arsenal | Premier League | €120.00M | 0.7647 |
| 88.7% | Granit Xhaka | Sunderland | Premier League | €8.00M | 0.7609 |
| 85.7% | Elliot Anderson | Nottingham Forest | Premier League | €110.00M | 0.7828 |
| 84.4% | Nadiem Amiri | 1. FSV Mainz 05 | Bundesliga | €17.00M | 0.7576 |
| 84.3% | Bruno Guimarães | Newcastle United | Premier League | €70.00M | 0.7897 |
| 84.0% | Nicolò Barella | Inter | Serie A | €50.00M | 0.7818 |
| 83.6% | Lamine Camara | AS Monaco | Ligue 1 | €40.00M | 0.7239 |

### Bartuğ Elmaz (Fatih Karagümrük · Süper Lig)
- MV: **—** · xP pass: 0.7634

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 83.0% | Sofyan Amrabat | Real Betis | La Liga | €10.00M | 0.7332 |
| 81.7% | Laurent Abergel | Lorient | Ligue 1 | €1.80M | 0.7744 |
| 81.6% | Nemanja Matić | Sassuolo | Serie A | €1.60M | 0.7416 |
| 80.0% | Pathé Ismaël Ciss | Rayo Vallecano | La Liga | €1.80M | 0.7146 |
| 77.9% | Nico González | Manchester City | Premier League | €40.00M | 0.7705 |
| 76.7% | Hugo Sotelo | Celta Vigo | La Liga | €5.00M | 0.7887 |
| 76.6% | Nabil Bentaleb | Lille | Ligue 1 | €4.50M | 0.6956 |
| 76.0% | Moisés Caicedo | Chelsea | Premier League | €100.00M | 0.7859 |

### Tygo Land (FC Groningen · Eredivisie)
- MV: **—** · xP pass: 0.7569

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 76.5% | Giovani Lo Celso | Real Betis | La Liga | €8.00M | 0.7358 |
| 76.3% | Petar Sučić | Inter | Serie A | €45.00M | 0.702 |
| 73.5% | Pol Lozano | Espanyol | La Liga | €6.00M | 0.6729 |
| 71.6% | Henrikh Mkhitaryan | Inter | Serie A | €3.00M | 0.7161 |
| 70.5% | Vitaly Janelt | Brentford | Premier League | €16.00M | 0.6679 |
| 69.7% | Moi Gómez | Osasuna | La Liga | €1.50M | 0.7441 |
| 69.2% | Fermín López | FC Barcelona | La Liga | €100.00M | 0.6548 |
| 68.6% | Ismael Koné | Sassuolo | Serie A | €25.00M | 0.6911 |

### Aleksandar Stanković (Club Brugge KV · Belgian Pro League)
- MV: **—** · xP pass: 0.7548

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 89.4% | Tyler Morton | Olympique Lyonnais | Ligue 1 | €30.00M | 0.7501 |
| 89.0% | Lucas Da Cunha | Como | Serie A | €20.00M | 0.7678 |
| 88.3% | Éderson | Atalanta | Serie A | €45.00M | 0.737 |
| 87.7% | Bernardo Silva | Manchester City | Premier League | €22.00M | 0.7552 |
| 87.2% | Gauthier Hein | Metz | Ligue 1 | €5.00M | 0.7014 |
| 87.0% | James Garner | Everton | Premier League | €45.00M | 0.7375 |
| 86.6% | Stanislav Lobotka | SSC Napoli | Serie A | €10.00M | 0.7798 |
| 86.6% | Ryan Gravenberch | Liverpool FC | Premier League | €80.00M | 0.7537 |

### Sean Steur (AFC Ajax · Eredivisie)
- MV: **—** · xP pass: 0.7512

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 89.3% | Giovani Lo Celso | Real Betis | La Liga | €8.00M | 0.7358 |
| 88.5% | Moi Gómez | Osasuna | La Liga | €1.50M | 0.7441 |
| 84.7% | Carlos Soler | Real Sociedad | La Liga | €7.00M | 0.698 |
| 84.4% | Petar Sučić | Inter | Serie A | €45.00M | 0.702 |
| 84.2% | Piotr Zieliński | Inter | Serie A | €0.00 | 0.776 |
| 82.5% | Rayan Cherki | Manchester City | Premier League | €90.00M | 0.7588 |
| 82.0% | Manu Koné | AS Roma | Serie A | €50.00M | 0.7687 |
| 81.2% | Mario Pašalić | Atalanta | Serie A | €6.00M | 0.7561 |

### Paul Wanner (PSV Eindhoven · Eredivisie)
- MV: **—** · xP pass: 0.7346

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 83.3% | Giovani Lo Celso | Real Betis | La Liga | €8.00M | 0.7358 |
| 82.9% | Petar Sučić | Inter | Serie A | €45.00M | 0.702 |
| 77.7% | Carlos Soler | Real Sociedad | La Liga | €7.00M | 0.698 |
| 77.0% | Mateus Fernandes | West Ham United | Premier League | €50.00M | 0.7348 |
| 76.9% | Piotr Zieliński | Inter | Serie A | €0.00 | 0.776 |
| 76.7% | João Neves | Paris Saint-Germain | Ligue 1 | €140.00M | 0.7409 |
| 76.6% | Manu Koné | AS Roma | Serie A | €50.00M | 0.7687 |
| 75.0% | Curtis Jones | Liverpool FC | Premier League | €35.00M | 0.7847 |

### Adrion Pajaziti (HNK Hajduk Split · Croatian League)
- MV: **—** · xP pass: 0.7289

| Sim | Jogador | Clube | Liga | MV | xP pass |
|---:|---|---|---|---:|---:|
| 91.0% | Sander Berge | Fulham | Premier League | €25.00M | 0.7066 |
| 86.6% | Sofyan Amrabat | Real Betis | La Liga | €10.00M | 0.7332 |
| 84.2% | Nicolas Seiwald | RB Leipzig | Bundesliga | €25.00M | 0.7152 |
| 83.6% | Remo Freuler | Bologna | Serie A | €3.00M | 0.6928 |
| 81.8% | Noah Cadiou | Lorient | Ligue 1 | €3.00M | 0.67 |
| 80.2% | Antonio Blanco | Deportivo Alavés | La Liga | €10.00M | 0.6808 |
| 78.6% | Samir El Mourabet | RC Strasbourg | Ligue 1 | €22.00M | 0.6945 |
| 78.1% | Pepelu | Valencia | La Liga | €8.00M | 0.7111 |


## Alternativas consideradas

| Abordagem | Prós | Contras |
|---|---|---|
| **Seven pillars (recomendado)** | Mesma linguagem dos relatórios; fácil de explicar | Ignora zona de origem dos passes |
| **Alt metrics** | Captura estilo (longos, xPV, COE) | Menos intuitivo para scouts |
| **Heatmap / origem** | Muito bom para *onde* o jogador atua no campo | Pesado; precisa de passes por jogador em memória |
| **Archetypes (5 pilares)** | Bom para rótulo tático | Não é busca por vizinho; é classificação |
| **Compare API (head-to-head)** | Já existe no app | Só 1v1 manual, não ranqueia o pool |

Para scouting de valor, use **top5-to-satellite** com filtro de MV ≤35%. Para projetar um satélite na elite, use **satellite-to-top5**.
