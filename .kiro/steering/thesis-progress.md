---
inclusion: auto
---

# Thesis Progress

## Current Status

**Currently working on:** Lit Review claims complete (§2.1–§2.8 all initially reviewed). Next: decomposition and prose rewrite pass over completed sections. Also pending: §2.7 minor revision (trim final bullet, add Typed-RAG adjacent work).

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

- **§2.2 (end):** The roadmap sentence at the end of §2.2 describes what §2.3–§2.6 will do. Needs re-review against the new flow (§2.3 = rules out fine-tuning, §2.4 = structure helps, §2.5 = specificity matters, §2.6 = constraining the problem space). Current wording may still fit but verify.

## Completed Work (All Sessions)

### Introduction
- [x] Problem Statement (§1.2) — 20 claims, full citation coverage, all reviewed
- [x] Purpose of the Paper (§1.3) — first pass done (claims reviewed/revised, citations logged)

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
- **sample.bib:** Add `typed_rag2025` entry (Lee et al., "Typed-RAG: Type-Aware Decomposition of Non-Factoid Questions for RAG", XLLM@ACL 2025)

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

### §2.8 Citation Verification Status
- `liroth2002questions` — Li & Roth 2002, "Learning Question Classifiers" — UNREVIEWED (HIGH confidence: foundational QC paper, finite taxonomy of question types)
- `nonfactoid_taxonomy2022` — Bolotova et al. 2022, "A Non-Factoid Question-Answering Taxonomy" — UNREVIEWED (HIGH confidence: SIGIR Best Paper, finite set of answer-type categories)
- `xie2022icl` — Xie et al. 2022, "An Explanation of In-context Learning as Implicit Bayesian Inference" — UNREVIEWED (MEDIUM-HIGH confidence: supports "few-shot relies on model inferring latent pattern"; exact framing needs full-text verification)

## Still TODO (Non-Lit-Review)

- [ ] Hook (§1.1) — needs rewrite after Problem Statement/Purpose finalized
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
