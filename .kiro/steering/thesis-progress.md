---
inclusion: auto
---

# Thesis Progress

## Current Status

**Currently working on:** Section 2 — Literature Review (subsection by subsection)

**⚠️ IMPORTANT: All sections written as bullet-point claims are DRAFTS.** Claims can be written/reviewed with Kiro but the final prose must be written by the author. No section is truly "done" until it has been rewritten in the author's voice as flowing paragraphs. "Initially reviewed" means claims are structured and reviewed — NOT that the section is publication-ready.

## Section Order (Lit Review)

1. [x] Large Language Models (§2.1) — initially reviewed
2. [x] Scale and Structure (§2.2) — initially reviewed
3. [x] Fine-Tuning and Parameter-Efficient Adaptation (§2.3) — initially reviewed
4. [x] Prompt Engineering and In-Context Learning (§2.4) — initially reviewed
5. [x] Retrieval-Augmented Generation (§2.5) — initially reviewed
6. [x] Unconstrained Prediction (§2.6) — reviewed and finalized
7. [ ] Question Classification in QA (§2.7) — unreviewed
8. [ ] Answer Structure Types: A Taxonomy Hypothesis (§2.8) — unreviewed

## Re-Review Notes

- **§2.2 (end):** The roadmap sentence at the end of §2.2 describes what §2.3–§2.6 will do. Needs re-review against the new flow (§2.3 = rules out fine-tuning, §2.4 = structure helps, §2.5 = specificity matters, §2.6 = constraining the problem space). Current wording may still fit but verify.

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
- [x] §2.5 Retrieval-Augmented Generation — 5 claims initially reviewed and written to main.tex
  - RAG defined (inference-time automated prompt construction via retrieval)
  - Distinction from prompt engineering (same principle, different context origin)
  - Question-decomposition RAG (organization of retrieval improves content precision)
  - Corrective RAG (filtering prevents low-quality content from degrading output)
  - Synthesis: organization + specificity together outperform either in isolation
  - Section's job in through-line: advances "structure helps" (§2.4) to "structure + specificity is better"
  - Does NOT make gap claims (that's §2.6) or position the framework (that's §3)
  - Citation needed: `corrective_rag2024` added to bib (unreviewed)
  - All citations flagged as unreviewed: `lewis2020rag`, `rag_survey2023`, `sahoo2024promptsurvey`, `question_decomp_rag2025`, `corrective_rag2024`
- [x] §2.6 Unconstrained Prediction — 7 claims reviewed and finalized
  - Define hallucination → reframe as unconstrained prediction (no separate failure mode)
  - Parameters set baseline distribution; small models approximate at lower resolution (Godey et al.)
  - Approximation compounds during generation (LPSR 2026 + exposure bias)
  - "We argue" scope reduced by narrowing output space (empirical: brevity constraints)
  - Synthesis: existing approaches narrow space via weight modification, generic context, and targeted content respectively
  - General principle: matched structure + specific context especially effective for small models (ICL is architectural)
  - Dropped hallucination_unified2024 (definition conflict). Added olsson2022inductionheads, taskspecific_prompts2025, blueprints_slm2025 (all unverified)
  - Section does NOT name answer structure as the solution — leaves that to §2.8

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
