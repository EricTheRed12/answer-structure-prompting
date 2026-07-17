---
inclusion: manual
---

# Citation Verification Tracker

Pull this file into context when reviewing or verifying citations for a section.

## ⭐ DEFERRED MILESTONE: Full-text verification (after ALL claims are done)

Once every section's claims are finalized, do a dedicated pass to verify EVERY cited paper against its FULL TEXT — not just the abstract/snippet.

Why: Abstracts can support a claim that the full paper actually qualifies, contradicts, or scopes narrowly.

Priorities flagged:
- `costofdownscaling2023` (confirm fact-recall-vs-ICL split holds as worded)
- `nonfactoid_taxonomy2022` (confirm non-factoid scope doesn't undercut general use)
- `xie2022icl` (confirm "uncertainty collapses with few examples" framing)
- Many bib entries have `author = "various"` placeholders — fix real author lists during this pass

---

## Hook Section (§1.1)

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `kaplan2020scaling` | Large models superior but resource-constrained | HIGH | arXiv (2700+ citations) | Unverified |
| `strubell2019energy` | Resource constraints | HIGH | ACL 2019 | Unverified |
| `patterson2021carbon` | Resource constraints | HIGH | arXiv (Google) | Unverified |
| `smalllmsready2024` | Small models compete with large | MEDIUM | arXiv | Unverified |
| `modelsizematters2024` | Small models compete with large | MEDIUM | arXiv | Unverified |
| `wei2022cot` | CoT can improve small model performance | HIGH | arXiv (highly cited) | Unverified |
| `cot_limitations2025` | CoT has shortcomings | MEDIUM | arXiv | Unverified |
| `cot_mirage2025` | CoT has shortcomings | MEDIUM | arXiv | Unverified |
| `lewis2020rag` | RAG can improve small models | HIGH | NeurIPS 2020 | Unverified |
| `rag_survey2023` | RAG has shortcomings | MEDIUM | arXiv | Unverified |
| `devlin2019bert` | Small models comprehend language | HIGH | NAACL 2019 | Unverified |
| `liu2019roberta` | Small models comprehend language | HIGH | arXiv | Unverified |
| `costofdownscaling2023` | Comprehension survives downscaling | MEDIUM | arXiv | Unverified |
| `liroth2002questions` | Finite question type classification | HIGH | COLING 2002 | Unverified |
| `nonfactoid_taxonomy2022` | Finite answer structures exist | HIGH | SIGIR 2022 | Unverified |

## Problem Statement (§1.2)

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `eloundou2023gpts` | LLMs are transformative (labor market impact) | MEDIUM | arXiv / Science 2024 | Unverified |
| `llm_critical_societal2024` | LLMs are transformative (healthcare, finance, law) | MEDIUM | arXiv | Unverified |
| `llmoverview2023` | LLMs are transformative (general survey) | MEDIUM | arXiv | Unverified |
| `liesenfeld2024closed` | Most capable are closed/proprietary | HIGH | Nature 2024 | Unverified |
| `kapoor2024societal` | Concentrated control limits contributions | MEDIUM | arXiv / ICML 2024 | Unverified |
| `bommasani2023fmti` | No external input on training; can't be audited | HIGH | arXiv (Stanford) | Unverified |
| `liesenfeld2024openwashing` | "Open-source" models aren't truly open | HIGH | ACM FAccT 2024 | Unverified |
| `strubell2019energy` | Environmental cost | HIGH | ACL 2019 | Unverified |
| `patterson2021carbon` | Environmental cost | HIGH | arXiv (Google) | Unverified |
| `modelsizematters2024` | Small models underperform | MEDIUM | arXiv | Unverified |
| `kaplan2020scaling` | Limited parametric capacity; hard cap | HIGH | arXiv (2700+ citations) | Unverified |
| `costofdownscaling2023` | Can't encode everything; brittleness | MEDIUM | arXiv | Unverified |
| `linguistic_competence_scale2025` | Linguistic competence survives scaling | MEDIUM | arXiv | Unverified |
| `emergent_reducedscale2024` | Emergent abilities in small models | MEDIUM | NAACL 2024 | Unverified |
| `slm_survey2024` | Small models accessible; domain training | MEDIUM | arXiv (Penn State) | Unverified |
| `domain_expert_smalllm2024` | Small models match domain experts | MEDIUM | arXiv | Unverified |
| `catastrophic_forgetting2023` | Specialization costs generality | MEDIUM | arXiv | Unverified |

## Purpose of the Paper (§1.4) — reviewed via web search

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `devlin2019bert` | Encoder classifier maps question → structure type | HIGH | NAACL 2019 | ✅ Verified (canonical fit) |
| `costofdownscaling2023` | Core mechanism: in-context ability survives down-scaling | MEDIUM | ICLR 2024 / arXiv | ✅ Verified; claim REWORDED to match |
| `xie2022icl` | Scaffold narrows probability space | HIGH | ICLR 2022 | ✅ NEW — direct fit |
| `liroth2002questions` | Answer structure inferable from question text | HIGH | COLING 2002 | ✅ Verified (canonical fit) |
| `nonfactoid_taxonomy2022` | Finite set of answer structure types exists | HIGH | SIGIR 2022 (Best Paper) | ✅ VERIFIED — direct hit |
| `smalllmsready2024` | Generator can be any small model | MEDIUM | arXiv | ✅ Keep |
| `slm_survey2024` | Generator can be any small model | MEDIUM | arXiv (Penn State) | ✅ NEW here |

## Lit Review §2.3 — Unconstrained Prediction

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `ji2023hallucination` | Definition of hallucination | HIGH | ACM Computing Surveys 2023 | Unverified |
| `hallucination_unified2024` | Definition of hallucination | MEDIUM | ICML 2026 | **RISK — their definition (inaccurate world modeling) may conflict with our simpler definition (output ≠ expected). Review full text before relying on it.** |
| `brown2020gpt3` | Autoregressive mechanism; no separate failure mode (supports premise, conclusion is ours) | HIGH | NeurIPS 2020 | Unverified |
| `godey2024softmax` | Small models cannot fully express target probability distribution due to dimensional bottleneck | HIGH | arXiv 2024 (Inria) | Unverified |
| `lpsr2026` | Inference-time error compounding: "once a wrong step is taken, subsequent tokens compound the mistake" | HIGH | arXiv 2026 (under review) | Unverified |
| `exposure_bias_ilp2022` | Error propagation in autoregressive generation (training-side cause) | MEDIUM | arXiv | Unverified — supports the vulnerability but is about training-time exposure bias, not inference-time compounding directly. Keep as secondary support alongside lpsr2026. |
| `costofdownscaling2023` | What degrades with scale (fact recall before ICL) — belongs on claim 3, not claim 4 | MEDIUM | ICLR 2024 / arXiv | Unverified |
| `hallucination_survey2024` | Hallucination scales inversely with model size | MEDIUM | arXiv | Unverified — supports existence of problem, not "narrowing reduces scope" specifically |
| `zhang2023hallucination` | Hallucination scales inversely with model size | MEDIUM | arXiv | Unverified — same concern as above |
| `brevity_constraints2025` | Constraining output form improves performance empirically | MEDIUM | arXiv (unreviewed) | Unverified — empirical backing for claim 5's "narrowing reduces scope" principle |
| `llmreasoning_stochastic2024` | LLMs as stochastic pattern-matchers (ambient support for claim 7) | MEDIUM | arXiv | Unverified |

### Claim 1 — Alternative papers to review (hallucination definition)

The following papers could replace or supplement `hallucination_unified2024` if its "world model" definition conflicts:
- `ji2023hallucination` — ACM Computing Surveys, comprehensive, uses simpler output-mismatch framing. Likely sufficient alone.
- `zhang2023hallucination` — Siren's Song survey. Documents hallucination broadly. May have a compatible definition.
- `whyllmshallucinate2024` — "Why Language Models Hallucinate." Mechanistic focus. May fit better with claim 2 than claim 1.
- `hallucination_survey2024` — another broad survey. Check its definition section.

**Decision needed after full-text review:** Does `hallucination_unified2024`'s "world model" framing conflict with our simpler "output ≠ expected" definition? If yes, drop it from claim 1 and use `ji2023hallucination` alone.

## Lit Review §2.2 — Scale and Structure

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `kaplan2020scaling` | Scale is dominant performance predictor; capacity explanation | HIGH | arXiv (2700+ citations) | Unverified |
| `hoffmann2022chinchilla` | Compute-optimal scaling; model+data should scale equally | HIGH | NeurIPS 2022 (DeepMind) | Unverified |
| `brown2020gpt3` | GPT-3 vs GPT-2 jump demonstrates capacity gap | HIGH | NeurIPS 2020 | Unverified |
| `llmoverview2023` | More parameters → more connections encoded | MEDIUM | arXiv | Unverified |
| `smalllmsready2024` | Small models match large on specific tasks (gap is conditional) | MEDIUM | arXiv | Unverified |
| `modelsizematters2024` | Small models match large on specific tasks (gap is conditional) | MEDIUM | arXiv | Unverified |
| `costofdownscaling2023` | External context can close gap; scale ≠ completeness | MEDIUM | ICLR 2024 / arXiv | Unverified for §2.2 use |
| `math_reasoning_limits2024` | Large models still fail on multi-step/structured tasks | MEDIUM | arXiv | Unverified |
| `lrm_complexity2025` | Reasoning models collapse beyond certain complexity | MEDIUM | NeurIPS 2025 (Apple) | Unverified |
| `wei2022cot` | CoT imposes structure → improves reasoning | HIGH | arXiv (highly cited) | Unverified |
| `brevity_constraints2025` | Output form constraints invert large-vs-small rankings | MEDIUM | arXiv (unreviewed) | Unverified |
| `prompt_control_theory2023` | Prompts steer output probability distributions | MEDIUM | arXiv (unreviewed) | Unverified |
| `llmreasoning_stochastic2024` | LLM output is pattern-based, not genuine reasoning | MEDIUM | arXiv | Unverified |
| `liesenfeld2024closed` | Closed-source internals unverifiable (footnote) | HIGH | Nature 2024 | Unverified |

## Lit Review §2.1 — Large Language Models

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `vaswani2017attention` | Transformer architecture; self-attention | HIGH | NeurIPS 2017 | Unverified |
| `llmoverview2023` | LLM definition and overview | MEDIUM | arXiv | Unverified |
| `brown2020gpt3` | Token prediction; decoder pre-training; autoregressive decoding | HIGH | NeurIPS 2020 | Unverified |
| `devlin2019bert` | Encoder pre-training (masked LM) | HIGH | NAACL 2019 | Unverified |
| `exposure_bias_ilp2022` | Error propagation in autoregressive generation | MEDIUM | arXiv | Unverified |
| `llama3_2024` | Confirms autoregressive decoder for open models | HIGH | arXiv (Meta) | Unverified |
| `liesenfeld2024closed` | Closed models don't disclose internals (footnote) | HIGH | Nature 2024 | Unverified |
| `llmreasoning_stochastic2024` | LLMs as probability engines; stochastic nature | MEDIUM | arXiv | Unverified |

## §1.4 Applied Changes (from previous sessions)

- Generator claim: dropped `modelsizematters2024` (wrong support), added `slm_survey2024`
- Core-mechanism claim: kept `costofdownscaling2023`, REWORDED to credit surviving ICL ability
- Probability-space claim: replaced `llmreasoning_stochastic2024` with `xie2022icl` for §1.4 specifically
- Metadata bug FIXED: `llmreasoning_stochastic2024` bib year corrected 2024 → 2025

## Legacy Review Items

- [ ] Consider enhancing Hook Claim 3 to strengthen "comprehension survives scale" argument
- [ ] Verify `nonfactoid_taxonomy2022` defines answer types (not just question types)
- [ ] Verify `liroth2002questions` finite question type classification with learned classifier
