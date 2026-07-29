---
inclusion: auto
---

# Thesis Key Concepts

These are load-bearing conceptual decisions for the paper. Apply them everywhere.

## Terminology: "answer structure" (NOT "reasoning structure")

Use **"answer structure"** consistently everywhere. Do NOT use "reasoning structure" — it invites confusion with CoT-style reasoning chains.

## "Small models" definition

When the paper refers to "small models" or "small language models," it means **small autoregressive decoder LLMs** (same architecture as GPT, just fewer parameters — e.g. Llama 3B, Phi-2, Mistral 7B). Not encoder models like BERT. The classifier component is a separate BERT-style encoder — that distinction must remain clear.

## Answer Structure as Dimensional Framework

The answer structure does not provide the answer itself — it provides the *dimensions that matter* for a given type of problem. The model then populates those dimensions with content.

- A schema with labeled blank fields
- Tells the model *what to look for*, not *what the answer is*
- Each dimension is a required component of the answer

## The Novel Contribution = the ANSWER STRUCTURE itself

The single novel solution is **the answer structure** — the idea of supplying the model with the structure a correct answer must take. Everything else (the classifier, the taxonomy routing, the encoder, the scaffold delivery) is supporting machinery, NOT the contribution.

- The novelty is the SPECIFIC kind of structure (the answer's structural form), not structure in general.
- It is a form of prompt engineering — own it and differentiate it by the fact that it's *matched to the question* via classification and provides the pattern directly rather than examples to infer from.

## Central vs Enabling Hypothesis

- **Central hypothesis** (what the experiments test): conditioning a small LLM on an answer structure matched to the question improves its accuracy enough to narrow the gap with larger models.
- **Finiteness hypothesis** (§2.8): answer structure types form a finite, bounded set classifiable from question text. The approach works without this being true, but this hypothesis means it can be automated.
- **Operating premises** (assumed, not proven):
  - A finite set of answer structure types is sufficient to cover a given task domain
  - The answer structure can be inferred from the question alone

## Key Framing Rules

- Use "**narrow** the gap" — never "close" or "surpass"
- Use "**matched to the question**" — never "appropriate" (too vague/circular)
- The offline LLM used to generate training data is a **tool**, not part of the framework
- Framework requires **no weight updates** to the generator — inference-time only
- No em-dashes in prose

## Prediction Engine Framing

- Models are prediction engines. Output = statistically most likely token given context and prompt.
- "Hallucination" is unconstrained prediction, not a separate failure mode.
- The model is deterministic (same input + same config = same output).
- Input defines the trajectory of the prediction — it's the only point of intervention.
- Temperature/seed create variety but don't improve generation.
- Answer structure shapes the context so probability distribution is biased toward correct output structure from the start. It narrows the prediction space. Input intervention, not capability enhancement.

## Structural Argument (the escalation)

- §2.2: Advantage of scale is partly structural encoding
- §2.3: Fine-tuning can't add capacity and hurts generalization
- §2.4: Prompting provides generic structure via ICL; scale-resistant but still relies on parametric capacity
- §2.5: RAG provides specificity; organization matters; but doesn't provide matched structural form
- §2.6: Model is deterministic; input is only intervention; existing techniques don't provide matched structure; what's needed is task-independent, dimension-specific, consistent in form
- §2.7: Classification is feasible; we propose answer classification; satisfies requirements
- §2.8: Answer structure defined; enables generalization; finiteness hypothesis (content infinite, form bounded)

## Experimental Design — SQuAD, no RAG

**Dataset:** SQuAD (extractive QA). Passage provided in prompt — knowledge problem solved by dataset format.

**Three conditions:**
1. Baseline: passage + question → generate answer
2. Scaffolded: passage + question + classifier-selected answer structure → generate answer
3. Ablation (random scaffold): passage + question + wrong answer structure → generate answer

**What this tests:**
- Condition 2 vs 1: Does matched answer structure improve performance?
- Condition 3 vs 2: Does classification quality matter?
- Condition 3 vs 1: Does wrong structure still help vs no structure?

RAG is future work (§8).

## Forward References to the Framework

- The lit review should NOT use "this paper aims to" framing.
- Each section's final claim can state the gap factually, but "our contribution" framing belongs in §3/§4.
- The lit review earns the framework's place by establishing facts, mechanisms, and gaps.
