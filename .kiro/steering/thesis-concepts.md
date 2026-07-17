---
inclusion: auto
---

# Thesis Key Concepts

These are load-bearing conceptual decisions for the paper. Apply them everywhere.

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

Requirements for the definition (to be written crisply in §2.7 and §3):
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
- **Structural argument threading:** §2.2 establishes the principle (advantage is partly structural, external structure helps). Subsequent sections must BUILD on this, not restate it. §2.4 shows why small models specifically need it. §2.5 shows existing prompt approaches don't provide it matched to the question. §2.6–2.7 show other approaches address different problems. Each section advances the argument; none repeat.
- **Section ordering:** May need to revisit lit review section ordering later. Ideally each section provides context for the rest of the paper, not just for the next section.
- **REVISIT after all sections complete:** Review the ordering of the lit review sections. Consider whether Answer Structure Types (§2.8/§2.9) should come earlier to provide context for §2.3's final claim. Evaluate once all sections have their claims finalized.

## §2.2 Scale and Structure — REVISIT: Add Architectural Equivalence Claim

§2.2 currently establishes what scale gives (structural encoding) and that the gap is conditional. It does NOT establish that small models are architecturally identical to large models — same system, same distributions, lower resolution.

**Proposed addition to §2.2** (place after the "gap is conditional, not absolute" claim):

> Small models are not architecturally distinct from large models. They share the same training objective, generation mechanism, and target distributions. What differs is the dimensionality available to represent those distributions; scale determines the resolution of the approximation, not its kind `\cite{godey2024softmax, costofdownscaling2023}`

This is needed because §2.3 claim 4 references it. Without it, §2.3 makes a claim that has no prior grounding.

**Citation note:** `godey2024softmax` (HIGH confidence, unverified) directly supports the "same distribution, fewer dimensions" framing.

---

## §2.3 Unconstrained Prediction — REVIEWED

- **Section title:** "Unconstrained Prediction" (renamed from "Reframing Model Errors")
- **Section job:** Argue that "hallucination" is not a distinct failure mode but the expected output of unconstrained prediction. Establish that narrowing the prediction space reduces divergence. Set up answer structure as the specific dimension of constraint this paper adds.
- **Claims (finalized, in main.tex):**
  1. Define hallucination as it appears in the literature
  2. Reframe: same mechanism produces all output; no separate failure mode; "we argue"
  3. Parameters determine baseline distribution; small models approximate at lower resolution (dimensional bottleneck via Godey et al.)
  4. Approximation compounds during autoregressive generation (imprecision propagates, limited self-correction)
  5. "We argue" compounding cannot be eliminated but scope reduced by narrowing output space (empirical backing: brevity constraints)
  6. Existing approaches reduce space via parameters or context
  7. Answer structure reduces space by providing output form (model only needs to populate content)
- **Cross-references:** §2.1 (autoregressive mechanism), §2.2 (architectural equivalence, brevity constraints), §2.5/§2.6 (existing approaches), §2.8 (answer structure defined)
- **Remaining items for future passes:**
  - Full-text verification of citations (deferred milestone)
  - `hallucination_unified2024` — decide keep or drop (potential "world model" definition conflict)
  - Claim 3 wording depends on §2.2 architectural equivalence claim being finalized
  - Claim 7 wording may need workshopping
  - Em-dashes to be removed in prose pass
- **Style notes:** no "this paper aims to" framing; no mind language; "we argue" for synthesis claims; no em-dash pauses
