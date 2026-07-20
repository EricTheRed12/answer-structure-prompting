---
inclusion: auto
---

# Thesis Key Concepts

These are load-bearing conceptual decisions for the paper. Apply them everywhere.

## Section Review Status

| Section | Status | Notes |
|---------|--------|-------|
| §1.1 Hook | Initially reviewed | |
| §1.2 Problem Statement | Initially reviewed | |
| §1.3 Purpose of the Paper | Initially reviewed | |
| §2.1 Large Language Models | Initially reviewed | |
| §2.2 Scale and Structure | Initially reviewed | Revisit: add architectural equivalence claim |
| §2.3 Fine-Tuning | Initially reviewed and finalized | |
| §2.4 Prompt Engineering and ICL | Initially reviewed | |
| §2.5 RAG | Initially reviewed | 5 claims written; old prose/gap claims/2×2 design removed |
| §2.6 Unconstrained Prediction | **REVIEWED AND FINALIZED** | Dropped hallucination_unified2024; added 3 new citations; claim 7 rewritten as general principle (no answer structure) |
| §2.7 Question Classification | **UNREVIEWED** | Has \\needpaper{} placeholders |
| §2.8 Answer Structure Types | **UNREVIEWED** | Needs CoT deep-dive and format-constrained decoding distinction added |
| §3 Architecture | **UNREVIEWED** | MoE routing added but section not reviewed |
| §4 Methodology | **UNREVIEWED — KNOWN STALE** | Still has 2×2 RAG design and MC QA benchmarks; should be SQuAD with 3 conditions |
| §5 Results | **UNREVIEWED** | TBD |
| §6 Discussion | **UNREVIEWED — KNOWN STALE** | References RAG comparison |
| §7 Limitations | **UNREVIEWED** | TBD |
| §8 Conclusion | **UNREVIEWED** | Future work mentions RAG (this is fine — RAG IS future work) |

## Terminology: "answer structure" (NOT "reasoning structure")

Use **"answer structure"** consistently everywhere. Do NOT use "reasoning structure" — it is too hard to both define and prove, and it invites confusion with CoT-style reasoning chains.

## "Small models" definition

When the paper refers to "small models" or "small language models," it means **small autoregressive decoder LLMs** (same architecture as GPT, just fewer parameters — e.g. Llama 3B, Phi-2, Mistral 7B). Not encoder models like BERT, and not classical NLP. The classifier component is a separate BERT-style encoder — that distinction must remain clear.

## Answer Structure as Dimensional Framework

The answer structure does not provide the answer itself — it provides the *dimensions that matter* for a given type of problem. The model then populates those dimensions with whatever relational knowledge it already has.

**Example:** A structure for "how to identify a sport" might include: name, tools used to play, where it is played. A small model that has fragments (soccer, ball, field) in its parameters can use the structure to organize those fragments into a coherent answer. The structure tells the model *what to look for*, not *what the answer is*.

## ⭐ THE Novel Contribution = the ANSWER STRUCTURE itself

The single novel solution of this paper is **the answer structure** — the idea of supplying the model with the structure a correct answer must take. Everything else (the classifier, the taxonomy routing, the encoder, the scaffold delivery) is supporting machinery, NOT the contribution.

- Do NOT frame the contribution as "structure helps small models" — that is ALREADY WELL KNOWN (few-shot, templates, CoT, structured prompts).
- The novelty is the SPECIFIC kind of structure (the answer's structure), not structure in general.

## ⚠️ The Definition of "Answer Structure" is Load-Bearing

Requirements for the definition (to be written crisply in §2.8 and §3):
- State what an answer structure IS: the set of dimensions/components a valid answer to a question must contain (NOT the answer content itself).
- Distinguish it explicitly from "question type" and from "reasoning path."
- Make it operational: concrete enough that two annotators would assign the same structure to the same question.
- Ground it with worked examples.

## Central vs Enabling Hypothesis

- **Central hypothesis** (what the experiments test): conditioning a small LLM on an answer structure matched to the question improves its accuracy enough to **narrow** (not close) the gap with larger models.
- **Operating premises** (assumed, not proven):
  - A finite set of answer structure types is sufficient to cover a given task
  - The answer structure is determined by the semantic context of the question and can be inferred from the question alone

## Key Framing Rules

- Use "**narrow** the gap" — never "close" or "surpass"
- Use "**matched to the question**" — never "appropriate" (too vague/circular)
- The offline LLM used to generate training data is a **tool**, not part of the framework
- Framework requires **no weight updates** to the generator — inference-time only

## Prediction Engine Framing (NOT "failure of thought")

- Models are prediction engines. They output the statistically most likely next token given the context and prompt.
- What we call "hallucination" is not a failure — it is the statistically correct output given insufficient contextual constraint. We call it hallucination because we treat models as minds, and when the output doesn't match our expectation we extend that treatment.
- Do NOT frame incorrect output as "failure to organize knowledge" or "failure to reason." The model has no knowledge to organize and performs no reasoning. It predicts tokens.
- The correct framing: given a prompt and context, the model's probability distribution may not be adequately constrained toward the output structure required by the task. The model is doing exactly what it is built to do — the issue is the input, not the engine.
- **Connection to the framework:** answer structure does not help the model "think better." It shapes the context so that the probability distribution over next tokens is biased toward the correct output structure from the start. It narrows the prediction space. It is an input intervention, not a capability enhancement.
- **Why large models are better (structural encoding argument):** Large models succeed partly because they have enough capacity to encode answer structure statistically in their parameters — they've seen enough examples to hold patterns for how answers should be structured. But because it's encoded statistically, it's probabilistic, never deterministic, never perfect. Small models lack the capacity to encode these structural patterns reliably.
- **The framework's intervention:** Rather than relying on statistically encoded structure (imperfect even in large models), provide it explicitly in the input. Make the structure deterministic in the context rather than hoping the model's parameters activate the right structural pattern probabilistically. This is an input-side intervention that replaces what large models do internally (imperfectly) with something explicit and reliable.
- **Prompt framing:** Yes, this is a form of prompt engineering — specifically a specific *type* of prompt. The answer structure is the answer in a slightly different form. Don't shy away from this; own it and differentiate it from generic prompting by the fact that it's *matched to the question* via classification.
- **Structural argument threading:** §2.2 establishes the principle (advantage is partly structural, external structure helps) and provides a roadmap of what follows. §2.3 acknowledges weight modification and argues it's unnecessary and counterproductive (the required abilities already exist; fine-tuning harms generalization). §2.4 shows existing prompt approaches don't provide structure matched to the question. §2.5 shows RAG provides knowledge but not structure (and that structure could improve RAG). §2.6 provides the mechanistic argument: hallucination is unconstrained prediction, narrowing the space reduces it, and none of the preceding approaches provide the specific narrowing this paper proposes. §2.7 shows question classification exists but stops short of defining answer structure. §2.8 introduces the taxonomy hypothesis. Each section advances the argument; none repeat.
- **Section ordering (DECIDED):** Lit review flows: §2.1 (mechanism) → §2.2 (scale/structure, identifies gap, provides roadmap) → §2.3–§2.5 (existing approaches: fine-tuning, prompting, RAG) → §2.6 (unconstrained prediction: the pivot/synthesis — why none of the above fully solve it) → §2.7 (question classification: precursor) → §2.8 (taxonomy hypothesis: the solution direction). This follows the classic pattern: context → existing work → identified gap → proposed solution.
- **REVISIT after all sections complete:** Review whether Answer Structure Types (§2.8) should move to §3 since it IS the novel contribution. Evaluate once all sections have their claims finalized.

## §2.3 (formerly §2.5) Fine-Tuning — REVIEWED AND FINALIZED

- **Section title:** "Fine-Tuning and Parameter-Efficient Adaptation"
- **Section job:** Acknowledge that weight modification is the standard approach to improving model performance, then argue it is both unnecessary (the required abilities already exist) AND counterproductive (it actively narrows the distribution, harming generalization). Rules out the entire parameter-modification design space and positions inference-time intervention as the right approach.
- **Claims (finalized, 7 claims in main.tex):**
  1. Weight modification is the most established approach to improving model performance
  2. Variants: full fine-tuning, PEFT methods (LoRA, adapters, prefix tuning). All modify the learned distribution
  3. Instruction tuning deserves particular attention: often framed as generalization, but is still distributional narrowing toward instruction-formatted responses. The mechanism is the same
  4. Knowledge distillation: teacher provides higher-quality outputs, student learns from them, but student still has the same dimensional bottleneck — holds a lower-resolution approximation
  5. All approaches narrow the distribution toward the training task, degrading performance outside it. This is the mechanism itself, not a side effect. Counterproductive for our goal
  6. Weight modification addresses a problem that is not the bottleneck — ICL and language understanding already survive downscaling
  7. The deficit is parametric but the fix is input-side. Fine-tuning can't add capacity. Provide structure in the input rather than relying on it to emerge from weights
- **Cross-references:** §2.2 (dimensional bottleneck, architectural equivalence, ICL survives)
- **Citations:** All resolved. No `\needpaper{}` remaining. Key: `peft_survey2024`, `hu2022lora`, `houlsby2019adapters`, `li2021prefixtuning`, `instructiontuning2022`, `alignment_tax2024`, `hinton2015distilling`, `catastrophic_forgetting2023`, `costofdownscaling2023`, `linguistic_competence_scale2025`
- **Notes for later:**
  - §3 (Architecture) should clarify the framework is compatible with instruction-tuned models
  - Prose pass: claims 6–7 may merge into one paragraph; vary "ICL survives downscaling" phrasing across its multiple appearances in the paper
  - "Fine-tuning cannot add capacity" — if challenged, response is architectural (softmax bottleneck = function of hidden dimension, unchanged by fine-tuning)

## §2.4 Prompt Engineering and In-Context Learning — REVIEWED

- **Section title:** "Prompt Engineering and In-Context Learning"
- **Section job:** Establish the landscape of prompt engineering techniques, show ICL is the unifying mechanism, demonstrate that input-side interventions are viable regardless of model size. Does NOT rule out prompt engineering (unlike §2.3 which rules out fine-tuning) — the paper's framework IS prompt engineering. Establishes viability and the principle that more/better context narrows the prediction space.
- **Claims (7 claims in main.tex):**
  1. Prompt engineering is the category of input-side interventions (contrasts with weight modification in §2.3)
  2. Zero-shot and system/instruction prompting provide task-level context; both operate uniformly across all questions
  3. Few-shot and many-shot prompting provide example input-output pairs; selection is by content similarity
  4. CoT provides generic process structure ("think step by step"); variations include ToT and Self-Consistency
  5. Common principle: additional context narrows the prediction space; each technique narrows differently
  6. ICL defined: the mechanism enabling all of the above; model uses context window as input influencing output distribution
  7. ICL is scale-independent: operates through attention (architectural), not stored parameters (capacity-dependent); viable regardless of model size
- **Cross-references:** §2.3 (ends with "provide structure in the input" → §2.4 explores what that looks like), §2.6 (synthesizes gap across §2.3–§2.5)
- **Citations:** `brown2020gpt3`, `sahoo2024promptsurvey`, `manyshot2024`, `wei2022cot`, `yao2023tot`, `wang2023selfconsistency`, `xie2022icl`, `costofdownscaling2023`, `prompt_control_theory2023`
- **Structural decisions:**
  - MoE routing concept moved to §3 (Architecture) — conceptually similar to classifier-based routing but operates at training time
  - CoT deep-dive (large vs small, extensions, "more defined structure helps") moved to §2.8 where it argues for why matched answer structure matters
  - Format-constrained decoding (JSON-mode, grammar-constrained generation) discussed in §2.8 where it is distinguished from answer structure
  - No gap claim at end of §2.4 — left to §2.6 synthesis
- **Notes for later:**
  - Revisit: Xie et al. Bayesian inference framing may be reintroduced when defining "prediction space" in §2.6 or §2.8
  - Revisit: potential limitations claim in later pass (not critical — section intentionally positive since framework IS prompt engineering)
  - Revisit: ordering of §2.7 (Question Classification) and §2.8 (Answer Structure Taxonomy) — consider swapping so flow becomes: unconstrained prediction → answer structure (the solution) → question classification (how to identify it)
  - §2.6 claim 6 to be revised to thread structural argument through §2.4 specifically: CoT shows structure helps, but process-level structure that is self-generated doesn't address the matched-structure gap

## §2.5 Retrieval-Augmented Generation — INITIALLY REVIEWED

- **Section title:** "Retrieval-Augmented Generation"
- **Section job:** Advance the escalation one step beyond §2.4. §2.4 shows prompt engineering works and structure helps. §2.5 shows RAG demonstrates that structure with *specific, relevant information* is even better. Organization and specificity together outperform either in isolation. Does NOT make gap claims or forward-sell the framework — that's §2.6's job.
- **Position in the through-line:**
  - §2.3: Fine-tuning is not the answer (rules out weight modification)
  - §2.4: Prompt engineering works at any scale, and structure helps (establishes viability)
  - **§2.5: RAG shows that structure with specific relevant information is better (specificity matters)**
  - §2.6: Errors are a failure of constraining the problem space (mechanistic why)
- **Claims (5 claims, initially reviewed):**
  1. RAG defined: inference-time system that automates prompt construction by retrieving relevant information from an external corpus and injecting it into the model's input before generation
  2. Distinction from prompt engineering: both input-side, no weight modification. Difference is where context originates (prompt author's design vs external knowledge source indexed at runtime)
  3. Question-decomposition RAG: breaks complex queries into sub-questions, retrieves separately for each. Provides more precise and relevant content by simplifying information needs into focused retrieval targets
  4. Corrective RAG: evaluates retrieval quality before passing to model, rejecting/revising documents below relevance thresholds. Prevents low-quality retrievals from degrading output
  5. Synthesis: RAG demonstrates that the §2.4 principle extends further — structuring the input process improves quality, and doing so with specific relevant information produces better results than generic structure alone. Organization and specificity together outperform either in isolation
- **Citations:** `lewis2020rag`, `rag_survey2023`, `question_decomp_rag2025`, `corrective_rag2024` — ALL NEED VERIFICATION (see citation review below)
- **Decisions made:**
  - Dropped naive RAG (just prompt engineering with automated retrieval)
  - Dropped Self-RAG / output-structuring RAG discussion (not needed for argument; can be steelmanned later if committee raises it)
  - Dropped "prediction space" / "generation space" language (belongs to §2.6)
  - Dropped 2×2 experimental design (experiment is now SQuAD, 3 conditions, no RAG)
  - RAG as retrieval guide for answer structure moved to future work (§8) — out of scope for this section
  - Softer landing preferred: section ends on "specificity matters" not "here's the gap" — don't give away the solution too early
- **NOTE for §2.8:** Must explicitly differentiate "answer structure" (output-side: what form the answer takes) from "structured RAG" (retrieval-side: how information is found and organized for the model). Without this distinction, readers may conflate the two.
- **Citation review needed:**
  - `lewis2020rag` — IN BIB. Verify it supports claim 1 specifically (inference-time retrieval into prompt)
  - `rag_survey2023` — IN BIB (Gao et al., arXiv:2312.10997). Verify it supports claims 2 and 5 (variants overview, organization improves quality)
  - `question_decomp_rag2025` — IN BIB (ACL 2025 SRW). Verify it supports claim 3 (sub-question decomposition, focused retrieval)
  - `corrective_rag2024` — NOT IN BIB. Likely Yan et al., "Corrective Retrieval Augmented Generation" (CRAG). Need to find, verify, and add bib entry

## §2.8 (formerly §2.9) Answer Structure Types: Taxonomy Hypothesis — NOTE

- **Placement decision deferred:** May belong in §3 (Architecture) rather than lit review since it IS the novel contribution. Keeping in §2 for now; revisit after all sections complete.

## Experimental Design — REVISED (SQuAD, no RAG)

**⚠️ main.tex is STALE:** §4 (Methodology) still contains the old 2×2 RAG design. This will be updated when that section is reviewed.

**Dataset:** SQuAD (extractive QA). The passage is provided in the prompt, so the model always has the knowledge it needs. No RAG required — the knowledge problem is solved by the dataset format itself.

**Three conditions (clean isolation of the answer-structure variable):**

1. **Baseline:** passage + question → generate answer (no scaffold, no structure)
2. **Scaffolded:** passage + question + classifier-selected answer structure scaffold → generate answer
3. **Ablation — random scaffold:** passage + question + wrong answer structure (mismatched type) → generate answer

**What this tests:**
- Condition 2 vs 1: Does matched answer structure improve performance?
- Condition 3 vs 2: Does classification quality matter, or does any scaffolding help?
- Condition 3 vs 1: Does wrong structure still help vs. no structure? (interesting either way)

**Why this is sufficient:**
- SQuAD provides the passage, so we isolate structure from knowledge
- No RAG needed — removes an entire engineering component
- RAG becomes future work: "what if the passage isn't provided? Can we retrieve it and still benefit from structure?"
- The 2×2 RAG design in the current main.tex can be moved to future work / discussion

**Optional additions (if time allows):**
- Oracle condition: manually assigned correct structure (ceiling for perfect classifier)
- Multiple model sizes: test whether improvement is consistent across parameter counts
- Base vs instruction-tuned variants

---

## §2.2 Scale and Structure — REVISIT: Add Architectural Equivalence Claim

§2.2 currently establishes what scale gives (structural encoding) and that the gap is conditional. It does NOT establish that small models are architecturally identical to large models — same system, same distributions, lower resolution.

**Proposed addition to §2.2** (place after the "gap is conditional, not absolute" claim):

> Small models are not architecturally distinct from large models. They share the same training objective, generation mechanism, and target distributions. What differs is the dimensionality available to represent those distributions; scale determines the resolution of the approximation, not its kind `\cite{godey2024softmax, costofdownscaling2023}`

This is needed because §2.3 claim 4 references it. Without it, §2.3 makes a claim that has no prior grounding.

**Citation note:** `godey2024softmax` (HIGH confidence, unverified) directly supports the "same distribution, fewer dimensions" framing.

---

## §2.6 (formerly §2.3) Unconstrained Prediction — REVIEWED

- **Section title:** "Unconstrained Prediction" (renamed from "Reframing Model Errors")
- **New position:** After existing approaches (§2.3 Fine-Tuning, §2.4 Prompt Eng, §2.5 RAG), before §2.7 Question Classification
- **Section job:** Now serves as the PIVOT from "here's what exists" to "here's what's missing." Argues that "hallucination" is not a distinct failure mode but the expected output of unconstrained prediction. Establishes that narrowing the prediction space reduces divergence. Synthesizes the preceding sections (none provide the specific type of narrowing needed) and sets up answer structure as the solution.
- **Claims (finalized, in main.tex):**
  1. Define hallucination as it appears in the literature
  2. Reframe: same mechanism produces all output; no separate failure mode; "we argue"
  3. Parameters determine baseline distribution; small models approximate at lower resolution (dimensional bottleneck via Godey et al.)
  4. Approximation compounds during autoregressive generation (imprecision propagates, limited self-correction)
  5. "We argue" compounding cannot be eliminated but scope reduced by narrowing output space (empirical backing: brevity constraints)
  6. The preceding sections reviewed approaches that reduce the prediction space: modifying parameters (§2.3), enriching context through prompting (§2.4) or retrieval (§2.5)
  7. Answer structure reduces space by providing output form (model only needs to populate content)
- **Cross-references:** §2.1 (autoregressive mechanism), §2.2 (architectural equivalence, brevity constraints), §2.3/§2.4/§2.5 (existing approaches), §2.8 (answer structure defined)
- **Remaining items for future passes:**
  - Full-text verification of citations (deferred milestone)
  - `hallucination_unified2024` — decide keep or drop (potential "world model" definition conflict)
  - Claim 3 wording depends on §2.2 architectural equivalence claim being finalized
  - Claim 7 wording may need workshopping
  - Em-dashes to be removed in prose pass
- **Style notes:** no "this paper aims to" framing; no mind language; "we argue" for synthesis claims; no em-dash pauses
