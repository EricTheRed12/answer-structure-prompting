---
inclusion: auto
---

# Thesis Progress

## Current Status

**Currently working on:** Prose rewrite of §2.1 COMPLETE. Prose rewrite of §2.2 (Scale and Structure) COMPLETE. Encoder/decoder split moved to §2.7. Next: prose rewrite of §2.3 (Fine-Tuning) or address flagged §2.7 revisions.

**⚠️ IMPORTANT: All sections written as bullet-point claims are DRAFTS.** Claims can be written/reviewed with Kiro but the final prose must be written by the author. No section is truly "done" until it has been rewritten in the author's voice as flowing paragraphs. "Initially reviewed" means claims are structured and reviewed — NOT that the section is publication-ready.

## Section Order (Lit Review)

1. [x] Large Language Models (§2.1) — initially reviewed
2. [x] Scale and Structure (§2.2) — initially reviewed
3. [x] Fine-Tuning and Parameter-Efficient Adaptation (§2.3) — initially reviewed
4. [x] Prompt Engineering and In-Context Learning (§2.4) — initially reviewed
5. [x] Retrieval-Augmented Generation (§2.5) — initially reviewed
6. [x] Unconstrained Prediction (§2.6) — reviewed and finalized
7. [x] Question Classification in QA (§2.7) — initially reviewed, written to LaTeX
8. [x] Answer Structure Types: A Taxonomy Hypothesis (§2.8) — initially reviewed, written to LaTeX

## Re-Review Notes

- **§2.2 (end):** Roadmap sentence removed. Section now closes with "prompting alone does not solve generalization" — verify this transitions cleanly into §2.3 opener when §2.3 is rewritten.
- **§2.4:** Note added to thread "generalization" — prompting doesn't sacrifice generalization (no weight changes) but is generic, not per-question.
- **§2.5:** Note added to thread "generalization" — RAG preserves general capability while augmenting with relevant context, but doesn't provide matched structure.
- **§2.6:** Note added to thread "generalization" — without structure, model defaults to degraded general distribution; generalization without guidance = unconstrained prediction.
- **§2.6 (brevity reference):** §2.6 still references brevity_constraints2025 with the old framing ("constraining output form alone inverts model-size performance rankings"). Needs updating to match corrected §2.2 framing when §2.6 is rewritten.

## Completed Work (All Sessions)

### Introduction
- [x] Problem Statement (§1.2) — 20 claims, full citation coverage, all reviewed
- [x] Purpose of the Paper (§1.3) — first pass done (claims reviewed/revised, citations logged)
- [x] Hook (§1.1) — PROSE REWRITE COMPLETE
  - 4 sentences flowing as one paragraph
  - Covers: LLMs transformative → scale/resource cost → small models lose ability → conventional explanation (scale) → but language ability preserved → what's missing?
  - Sets up §2 (Literature Review) as the answer to the closing question
- [x] Problem Statement (§1.2) — PROSE REWRITE COMPLETE
  - 3 paragraphs: closed models hinder community → open-source alternatives are flawed (scaling laws, parametric limits, brittleness) → linguistic competence preserved, existing approaches don't overcome capacity limits, research question stated
  - Claims compressed from 22 to 3 focused paragraphs
  - Original bullet claims removed from file
- [x] Purpose of the Paper (§1.3) — PROSE REWRITE COMPLETE
  - 3 paragraphs: hypothesis + system overview (classifier + generator) → two key premises (finite taxonomy, classifiable from question) → scope and evaluation (SQuAD, multiple model sizes, baseline comparison)
  - Original bullet claims removed from file
  - Key terms established: "answer structure," "prediction space," "answer dimensions"

### Literature Review
- [x] §2.1 Large Language Models — PROSE REWRITE COMPLETE
  - 4 claims (reordered from original 5; encoder/decoder split moved to §2.7)
  - Claim 1: Architecture — transformers, attention, structural features of language, parametric capacity constraint
  - Claim 2: Function — prediction engine, statistical relationships, forward pass, probability distribution, no guarantee of correctness, deterministic distribution per input, sampling configuration
  - Claim 3: Autoregressive decoding — sequential, each token becomes input for next, error propagation, contingent on initial prompt. Footnote re: closed models.
  - Claim 4: Closing implication — input directly determines the distribution from which tokens are selected
  - Note added to §2.7 to introduce encoder architecture there (motivated by classification argument)
  - Original bullet claims removed from file
- [x] §2.2 Scale and Structure — PROSE REWRITE COMPLETE
  - 7 claims rewritten as prose (original bullet claims removed from file)
  - Claim 1: Scale defined — parameter count, dominant predictor, capacity explanation (higher-resolution approximation)
  - Claim 2: Demonstrated — Brown et al. GPT-3 ablation (175B vs 1.3B, same architecture/training, only parameters differ)
  - Claim 3: Scale isn't everything — large models still fail (hallucinations, multi-step reasoning); gap is conditional, not absolute; small models with context match large ones
  - Claim 4: Architectural equivalence — same generation mechanisms, same corpora, same target distribution; difference is resolution of approximation
  - Claim 5: Structural argument (author synthesis) — advantage of scale is structural; image resolution analogy; patterns are statistically encoded and non-deterministic (unlike JSON schema); corruption possible regardless of size
  - Claim 6: External structure compensates — prompting compensates for degraded structural encoding; brevity constraints shift hierarchies by 26pp; structure determines quality
  - Claim 7: Closing — prompting alone doesn't solve generalization; need direct way to compensate for parametric constraint
  - CITATION FIX: brevity_constraints2025 finding was inverted in original claims (paper shows constraining form helps large models regain advantage, not small models outperform). Corrected to focus on the 26pp hierarchy shift principle.
  - Notes added to §2.4, §2.5, §2.6 to thread "generalization" through those sections during prose rewrite
  - Roadmap sentence (listing §2.3–§2.6) dropped — sections speak for themselves
- [x] §2.3 Fine-Tuning and Parameter-Efficient Adaptation — 6 claims reviewed
  - Weight modification as established approach
  - Variants (full fine-tuning, PEFT, instruction tuning, distillation)
  - All narrow distribution toward training task; counterproductive for general-task goal
  - Weight modification addresses wrong bottleneck (ICL survives downscaling)
  - Fix is input-side: provide structure in input rather than relying on weights
- [x] §2.4 Prompt Engineering and In-Context Learning — 7 claims initially reviewed
  - Prompt engineering defined (input-side interventions)
  - Zero-shot, system/instruction prompting (task-level, uniform)
  - Few-shot/many-shot (example-level)
  - CoT and variations (ToT, Self-Consistency — process structure)
  - Common principle: additional context narrows prediction space
  - ICL defined as the mechanism
  - ICL is scale-independent (architectural via attention, not capacity-dependent)
- [x] §2.5 Retrieval-Augmented Generation — 5 claims initially reviewed and written to main.tex
  - RAG defined (inference-time automated prompt construction via retrieval)
  - Distinction from prompt engineering (same principle, different context origin)
  - Question-decomposition RAG (organization of retrieval improves content precision)
  - Corrective RAG (filtering prevents low-quality content from degrading output)
  - Synthesis: organization + specificity together outperform either in isolation
- [x] §2.6 Unconstrained Prediction — 7 claims reviewed and finalized
  - Define hallucination → reframe as unconstrained prediction (no separate failure mode)
  - Parameters set baseline distribution; small models approximate at lower resolution (Godey et al.)
  - Approximation compounds during generation (LPSR 2026 + exposure bias)
  - Scope reduced by narrowing output space (empirical: brevity constraints)
  - Synthesis: existing approaches narrow space via weight modification, generic context, and targeted content
  - General principle: matched structure + specific context especially effective for small models (ICL is architectural)
- [x] §2.7 Question Classification in QA — 5 claims reviewed and written to main.tex
  - QC is well-established prior art (Li & Roth 2002, 20+ years)
  - Observable surface features distinguish question types (factual, analogical, multi-step)
  - Encoder-based classifiers reliably do this; same mechanism applies to novel label sets (de-risks classifier)
  - Gap: literature stops at question level; adjacent work (blueprints, TemplateRL, DTS) acknowledged and distinguished
  - Author synthesis: if question types are classifiable and structurally distinct, answer types must be too
- [x] §2.8 Answer Structure Types — 5 claims reviewed and written to main.tex
  - Bridge from §2.7: structural regularity extends to the answer side
  - Definition: answer structure = set of dimensions a valid answer must address (schema analogy)
  - Worked examples: three question types with dimensional structures; scope note (constrained domain)
  - Hypothesis: finite, enumerable, classifiable; supported by QC precedent (Li & Roth) and answer-type taxonomy (Bolotova et al.); generalization payoff for small models
  - Supporting properties: externally supplied (§2.6), matched per-question (§2.2/§2.5), semantic-level constraint; few-shot distinction (provides pattern directly vs relying on inference)

### Flagged Revisions (Pending)
- **§2.7 final bullet:** Trim to end at "answer types must be too" — remove hypothesis statement and "input constraint" language (§2.8 now owns this)
- **§2.7 adjacent work:** Add Typed-RAG (Lee et al. 2025, arXiv:2503.15879) — classifies NFQs into types for retrieval decomposition; similar (finite taxonomy, classifier-driven), distinct (retrieval intervention, not answer structure)
- **§2.7 adjacent work:** Add SMART (Setty 2023, arXiv:2304.12395) — BERT/XBERT encoder predicts answer entity types from KG taxonomy. Very close to our classifier approach but predicts entity type for retrieval filtering, not structural dimensions for generation.
- **§2.7 adjacent work:** Add CEUR-WS (2021) — BERT classifier, semantic answer type prediction using DBpedia hierarchy (~760 classes). Two-stage pipeline. Same distinction as SMART: classifies what entity type the answer is, not how the answer should be structured.
- **sample.bib:** Add `typed_rag2025` entry (Lee et al., "Typed-RAG: Type-Aware Decomposition of Non-Factoid Questions for RAG", XLLM@ACL 2025)
- **sample.bib:** Add `smart_answer_type2023` entry (Setty, "Extreme Classification for Answer Type Prediction in QA", JCDL 2023, arXiv:2304.12395)
- **sample.bib:** Add CEUR-WS 2021 semantic answer type prediction paper (need to identify exact authors/venue)

### Structural Decisions Made
- Merged old §2.3 (Generalization at Scale) + §2.4 (Problem with Scale) → §2.2 (Scale and Structure)
- Renamed §2.3 to "Unconstrained Prediction" (from "Reframing Model Errors")
- Stripped "this paper" / "Connection to this paper" framing from all reviewed lit review sections
- Created lit-review-section-map.md steering doc (maps each section's job, core ideas, scope boundaries)
- §2.7 cognitive science angle dropped — section focuses on NLP prior art and operational maturity only

### Bib Entries Added (Unreviewed)
- `llama3_2024` — Meta, "The Llama 3 Herd of Models" (confirms autoregressive decoder for open models)
- `exposure_bias_ilp2022` — Arora et al., "An Imitation Learning Perspective of Error Accumulation" (exposure bias → error propagation)
- `godey2024softmax` — Godey et al., "Why Do Small Language Models Underperform? Softmax Bottleneck" (dimensional bottleneck in small models)
- `lpsr2026` — Gupta et al., "Latent Phase-Shift Rollback" (inference-time error compounding in autoregressive models)
- `xu2019qc_bert` — Xu et al., "Multi-class Hierarchical Question Classification" (BERT-based QC SOTA on TREC + domain benchmarks)
- `templaterl2025` — Wu et al., "TemplateRL" (template library via MCTS + RL training)
- `dynamic_template_selection2025` — Yadavalli, "Dynamic Template Selection" (classifier → response templates for cost optimization)

### §1.2 Citation Verification Status
- `slm_survey2024` — used for "largest open-source models require specialized hardware" — UNREVIEWED (need to verify it specifically discusses hardware requirements by model size)
- `liroth2002questions` — Li & Roth 2002, "Learning Question Classifiers" — UNREVIEWED (HIGH confidence: foundational QC paper, finite taxonomy of question types)
- `nonfactoid_taxonomy2022` — Bolotova et al. 2022, "A Non-Factoid Question-Answering Taxonomy" — UNREVIEWED (HIGH confidence: SIGIR Best Paper, finite set of answer-type categories)
- `xie2022icl` — Xie et al. 2022, "An Explanation of In-context Learning as Implicit Bayesian Inference" — UNREVIEWED (MEDIUM-HIGH confidence: supports "few-shot relies on model inferring latent pattern"; exact framing needs full-text verification)

## Still TODO (Non-Lit-Review)

- [x] Hook (§1.1) — PROSE REWRITE COMPLETE
- [x] Problem Statement (§1.2) — PROSE REWRITE COMPLETE
- [x] Purpose of the Paper (§1.3) — PROSE REWRITE COMPLETE
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
- [x] Define "answer structure" crisply in §2.8/§3 (formal, load-bearing definition) — DONE in §2.8 claim 2
- [ ] §1.3 — add explicit Contributions subsection? Or let Purpose absorb that role?
