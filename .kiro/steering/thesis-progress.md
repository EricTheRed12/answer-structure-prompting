---
inclusion: auto
---

# Thesis Progress

## Current Status

**Currently working on:** Section 2 — Literature Review (subsection by subsection)

## Section Order (Lit Review)

1. [x] Large Language Models (§2.1) — claims finalized and written
2. [x] Scale and Structure (§2.2) — claims finalized, quick-pass edits done
3. [x] Unconstrained Prediction (§2.3) — claims finalized, citations first-passed
4. [ ] Small Language Models (§2.4)
5. [ ] Fine-Tuning and Parameter-Efficient Adaptation (§2.5)
6. [ ] Prompt Engineering and In-Context Learning (§2.6)
7. [ ] Retrieval-Augmented Generation (§2.7)
8. [ ] Question Classification in QA (§2.8)
9. [ ] Answer Structure Types: A Taxonomy Hypothesis (§2.9)

## Completed Work (All Sessions)

### Introduction
- [x] Problem Statement (§1.2) — 20 claims, full citation coverage, all reviewed
- [x] Purpose of the Paper (§1.4) — first pass done (claims reviewed/revised, citations logged)

### Literature Review
- [x] §2.1 Large Language Models — 5 claims finalized and written to main.tex
  - Structure (transformers, attention, parameters, training)
  - Function (probabilistic token prediction, stochastic)
  - Architecture split (encoder vs decoder, pre-training objectives)
  - Autoregressive decoding (sequential, committed, limited self-correction)
  - Key implication (probability engine — anything improving quality shapes the distribution)
- [x] §2.2 Scale and Structure — claims reviewed, quick-pass edits applied
  - Stripped "this paper" framing from final bullet
  - Merged "Existing techniques demonstrate this principle" into CoT bullet
  - Added architectural equivalence claim (small models = same system, lower resolution) with REVISIT note
  - Self-correction language updated to match §2.3
- [x] §2.3 Unconstrained Prediction (renamed from "Reframing Model Errors") — 7 claims finalized
  - Define hallucination → reframe as unconstrained prediction (no separate failure mode)
  - Parameters set baseline distribution; small models approximate at lower resolution (Godey et al.)
  - Approximation compounds during generation (LPSR 2026 + exposure bias)
  - "We argue" scope reduced by narrowing output space (empirical: brevity constraints)
  - Existing approaches reduce via parameters or context
  - Answer structure reduces by providing output form (model populates content)
  - Citations first-passed; hallucination_unified2024 flagged for full-text review

### Structural Decisions Made
- Merged old §2.3 (Generalization at Scale) + §2.4 (Problem with Scale) → §2.2 (Scale and Structure)
- Renamed §2.3 to "Unconstrained Prediction" (from "Reframing Model Errors")
- Stripped "this paper" / "Connection to this paper" framing from all reviewed lit review sections (§2.1, §2.2, §2.3). Remaining sections still need this treatment.
- Created lit-review-section-map.md steering doc (maps each section's job, core ideas, scope boundaries)
- Created new §2.4 (Small Language Models) — dedicated SLM section
- Created new §2.5 (Fine-Tuning and Parameter-Efficient Adaptation)
- Expanded Prompt Engineering to include ICL as first-class topic
- Folded MoE into Prompt Engineering as routing-analogy paragraph
- Created new §2.8 (Question Classification in QA) — separates prior art from our contribution
- Moved Answer Structure Taxonomy Hypothesis to final position (§2.9 — section payoff)
- Removed instruction tuning from Prompt Engineering (now in §2.5)

### Bib Entries Added (Unreviewed)
- `llama3_2024` — Meta, "The Llama 3 Herd of Models" (confirms autoregressive decoder for open models)
- `exposure_bias_ilp2022` — Arora et al., "An Imitation Learning Perspective of Error Accumulation" (exposure bias → error propagation)
- `godey2024softmax` — Godey et al., "Why Do Small Language Models Underperform? Softmax Bottleneck" (dimensional bottleneck in small models)
- `lpsr2026` — Gupta et al., "Latent Phase-Shift Rollback" (inference-time error compounding in autoregressive models)

## Still TODO (Non-Lit-Review)

- [ ] Hook (§1.1) — needs rewrite after Problem Statement/Purpose finalized (see rewrite plan in session notes)
- [ ] Abstract — write from scratch
- [ ] Architecture (§3) — write from scratch
- [ ] Methodology (§4) — write from scratch
- [ ] Results (§5) — after experiments
- [ ] Discussion (§6) — after experiments
- [ ] Limitations (§7) — after results
- [ ] Conclusion (§8) — after everything

## Hook Rewrite Plan (§1.1)

Goal: Hook does ONLY the "why care" job (broad stakes). Strip everything that belongs to Problem Statement or Purpose.

Target Hook (~4 light claims):
1. LLMs are transformative, reshaping how we work with information
2. But the most capable are large, closed, expensive — concentrating access/control
3. Small open models are accessible to anyone but underperform on general tasks
4. One forward-pointing sentence — "narrowing that gap without scale is the challenge this paper takes on" — WITHOUT revealing taxonomy/classifier

## Open Decisions (Parked)

- [ ] Gap-vs-larger-models comparison — where does it live? (Purpose vs Methodology vs Discussion)
- [ ] Core-mechanism claim citation — verify `costofdownscaling2023` actually shows fragment retention under downscaling
- [ ] §4 Methodology — labeling mechanism: training labels assigned by LLM offline. Must state this clearly.
- [ ] Define "answer structure" crisply in §2.8/§3 (formal, load-bearing definition)
- [ ] §1.3 — add explicit Contributions subsection? Or let Purpose absorb that role?
