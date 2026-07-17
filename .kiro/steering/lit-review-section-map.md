---
inclusion: auto
---

# Literature Review — Section Map

Each section has ONE job. This document tracks what each section establishes and what it sets up. Use it to determine where a claim belongs and to prevent overlap.

---

## §2.1 Large Language Models

**Job:** Establish how the technology works at the architectural level.

**Core ideas:**
- Transformer architecture, self-attention
- LLMs are probabilistic token predictors (probability engines, not knowledge databases)
- Two architectures: decoders (generate) vs encoders (represent); this paper uses both
- Autoregressive decoding: one token at a time, no lookahead, no revision, early tokens propagate
- Output is a probability distribution over the full vocabulary at every step

**Sets up:**
- §2.2 can discuss what scale adds without re-explaining the mechanism
- §2.3 can invoke "autoregressive generation compounds errors" without re-explaining what autoregressive means
- §3 (Architecture) can reference encoder vs decoder distinction

**Does NOT cover:**
- Why scale matters (that's §2.2)
- Why small models specifically struggle (that's §2.3 and §2.4)
- How to intervene on the generation process (that's §2.5, §2.6, and §3)

---

## §2.2 Scale and Structure

**Job:** Establish that the performance gap between large and small models is partly structural, not purely about knowledge capacity, and that external structure can partially close it.

**Core ideas:**
- Scale = parameter count; dominant performance predictor (scaling laws)
- Larger models outperform smaller ones (well-established)
- Conventional explanation: more parameters = more encoded connections
- But even large models fail on structured/multi-step tasks
- Gap is conditional, not absolute: small models match large ones given appropriate context
- Small models are architecturally identical to large models; same system, lower-resolution approximation of same distributions (REVISIT: verify wording)
- Author's argument: part of large-model advantage is structural encoding (capacity to encode answer structure patterns)
- This structural encoding is statistical, never deterministic
- External structure (CoT, brevity constraints) partially compensates
- Neither CoT nor brevity constraints are matched to the specific question

**Sets up:**
- §2.3 can reference "same distributions, fewer dimensions" for the hallucination mechanism
- §2.5 can discuss prompt engineering approaches as partially structural
- §3 can reference "matched to the specific question" as the gap this framework fills

**Does NOT cover:**
- The mechanistic *why* of the dimensional bottleneck (that's §2.3 via Godey et al.)
- What small models specifically retain or lose (that's §2.4)
- Specific prompting techniques in detail (that's §2.5)

---

## §2.3 Reframing Model Errors

**Job:** Reframe "hallucination" mechanistically as unconstrained prediction (not a failure mode), then show that narrowing the prediction space is the intervention, setting up why answer structure is a valid approach.

**Core ideas:**
- "Hallucination" = output that doesn't match expected answer (literature's definition)
- Reframe: same autoregressive mechanism produces all output; no separate failure mode; we argue hallucination is unconstrained prediction, not a defect
- Output distribution shaped by parameters and context
- Small models approximate same distributions at lower resolution (dimensional bottleneck, Godey et al.)
- Approximation compounds during autoregressive generation (imprecision propagates)
- Compounding is fundamental to autoregressive systems; scope reduced by narrowing prediction space
- Existing approaches narrow the space via parameters, retrieval, reasoning, examples
- This paper narrows it further by providing the output form, reducing what must be predicted

**Sets up:**
- §2.5 and §2.6 as approaches that narrow the space differently
- §3 (Architecture) as the mechanism that provides output form
- The experimental hypothesis: if we reduce what must be predicted, accuracy improves

**Does NOT cover:**
- Detailed discussion of RAG variants (that's §2.6)
- Detailed discussion of prompting techniques (that's §2.5)
- What small models retain linguistically (that's §2.4)

---

## §2.4 Small Language Models

**Job:** Establish what small models specifically retain and what they lose, supporting why inference-time structure (rather than retraining) is the appropriate intervention.

**Core ideas:**
- Small LLMs: same architecture as large, fewer parameters (1B-7B)
- Accessible to individual researchers
- Retain core linguistic competence (language understanding doesn't degrade proportionally)
- What degrades: parametric fact recall and associative depth, not in-context processing
- Domain specialization works but costs generality (catastrophic forgetting)
- On general tasks, still underperform
- Key implication: deficit is organizational structure, not linguistic competence

**Sets up:**
- §2.5 (prompt engineering): ICL works on small models because linguistic competence is retained
- §3 (Architecture): the framework works because small models can USE provided structure

**Does NOT cover:**
- Why the deficit exists mechanistically (that's §2.2 and §2.3)
- How to address it (that's §2.5, §2.6, §3)

---

## §2.5 Fine-Tuning and Parameter-Efficient Adaptation

**Job:** Establish that weight-modification approaches are effective but task-specific, require training per task, and risk forgetting. Distinguish from inference-time approaches.

**Core ideas:**
- Full fine-tuning: effective but expensive, needs large labeled data
- Catastrophic forgetting
- PEFT methods (LoRA, adapters, prefix tuning): reduce cost but still require training per task
- Instruction tuning: improves zero-shot but still requires training phase
- Shared limitation: task-specific, requires retraining, risks forgetting
- Distinction: this paper requires no weight updates

**NOTE — REVISIT:** Fine-tuning and context interventions don't just narrow the prediction space; they can also *expand* it in unintended directions. Fine-tuning on new data opens up regions of the distribution that were previously low-probability, potentially introducing new failure modes that didn't exist before (distinct from catastrophic forgetting — this is about creating new hallucination vectors, not losing old capabilities). This strengthens the case for inference-time structural constraint, which constrains without modifying weights and without risking new failure modes. Consider adding a claim here or in Discussion.

**Sets up:**
- §2.6 (prompting): inference-time alternatives that avoid retraining
- §3 (Architecture): framework operates on any model as-is

---

## §2.6 Prompt Engineering and In-Context Learning

**Job:** Establish existing inference-time approaches, what they provide (reasoning paths, knowledge, examples), and identify the gap (none provide answer structure matched to the question).

**Core ideas:**
- ICL: models learn from in-context examples without weight updates
- ICL as implicit Bayesian inference; survives downscaling
- CoT: step-by-step reasoning; works for large models, unreliable for small
- CoT extensions (ToT, Self-Consistency): expensive, still knowledge-dependent
- Few-shot/many-shot: examples selected by topic similarity, not answer structure type
- MoE as related routing concept (but training-time, not inference-time)
- Gap: all techniques construct prompts based on content or reasoning; none classify the structural type of answer required

**Sets up:**
- §2.7 (Answer Structure Types): what the novel structural classification looks like
- §3 (Architecture): the framework fills this gap

---

## §2.7 Retrieval-Augmented Generation

**Job:** Establish RAG as knowledge augmentation at inference time. Differentiate clearly: RAG provides content, this paper provides structure. Note they are orthogonal and combinable.

**Core ideas:**
- RAG augments parametric knowledge with retrieved documents
- RAG variants (naive, advanced, modular, speculative, question-decomposition)
- Critical differentiation: RAG = what information; question-decomp RAG = how question is broken up; this paper = what structural type the answer requires
- These are orthogonal problems; combinable
- Scaffold is conceptually similar to RAG's retrieved context but retrieves structural templates, not factual content

**Sets up:**
- §3 (Architecture): scaffold retrieval step is analogous to RAG retrieval

---

## §2.8 Question Classification in QA

**Job:** Establish that question type classification is recognized prior art, grounding the classifier component in existing work. Distinguish question types from answer structure types.

**Core ideas:**
- Classical QA recognizes question classification as preprocessing
- Cognitive science: experts categorize problem type before solving
- Different question types require structurally different reasoning
- Prior work classifies question types but not the structure a valid answer must take

**Sets up:**
- §2.9 (Answer Structure Types): the taxonomy hypothesis

---

## §2.9 Answer Structure Types: A Taxonomy Hypothesis

**Job:** State the novel hypothesis: answer structure types are finite, enumerable, classifiable from question text alone.

**Core ideas:**
- Not all questions require the same answer structure
- Hypothesis: structural types are finite, enumerable, classifiable by an encoder
- An answer structure defines dimensions/components a valid answer must contain (not content)
- Implication: if structure classification is natural for humans and QA systems, an encoder can replicate it

**Sets up:**
- §3 (Architecture): the classifier and taxonomy are the implementation of this hypothesis
