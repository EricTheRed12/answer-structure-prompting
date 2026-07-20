---
inclusion: auto
---

# Literature Review — Section Map

Each section has ONE job. This document tracks what each section establishes and what it sets up. Use it to determine where a claim belongs and to prevent overlap.

## Through-line (the escalation):

- §2.1: How the technology works (mechanism)
- §2.2: Scale gives structural encoding; gap is partly structural (identifies the problem)
- §2.3: Fine-tuning is not the answer (rules out weight modification)
- §2.4: Prompt engineering works at any scale, and structure helps (establishes viability)
- §2.5: RAG shows that structure with specific relevant information is better (specificity matters)
- §2.6: Errors are a failure of constraining the problem space (mechanistic why / synthesis)
- §2.7: Question classification exists as prior art (precursor)
- §2.8: Answer structure types are the solution direction (taxonomy hypothesis / payoff)

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
- §2.6 can invoke "autoregressive generation compounds errors" without re-explaining what autoregressive means
- §3 (Architecture) can reference encoder vs decoder distinction

**Does NOT cover:**
- Why scale matters (that's §2.2)
- Why small models specifically struggle (that's §2.2)
- How to intervene on the generation process (that's §2.4, §2.5, and §3)

---

## §2.2 Scale and Structure

**Job:** Establish that the performance gap between large and small models is partly structural, not purely about knowledge capacity, and that external structure can partially close it.

**Core ideas:**
- Scale = parameter count; dominant performance predictor (scaling laws)
- Larger models outperform smaller ones (well-established)
- Conventional explanation: more parameters = more encoded connections
- But even large models fail on structured/multi-step tasks
- Gap is conditional, not absolute: small models match large ones given appropriate context
- Small models are architecturally identical to large models; same system, lower-resolution approximation of same distributions
- Author's argument: part of large-model advantage is structural encoding (capacity to encode answer structure patterns)
- This structural encoding is statistical, never deterministic
- External structure (CoT, brevity constraints) partially compensates
- Neither CoT nor brevity constraints are matched to the specific question

**Sets up:**
- §2.3 can reference distributional narrowing as the mechanism fine-tuning uses
- §2.4 can discuss prompt engineering approaches as partially structural
- §2.6 can reference dimensional bottleneck for unconstrained prediction argument
- §3 can reference "matched to the specific question" as the gap this framework fills

**Does NOT cover:**
- Specific prompting techniques in detail (that's §2.4)
- RAG (that's §2.5)
- The mechanistic why of unconstrained prediction (that's §2.6)

---

## §2.3 Fine-Tuning and Parameter-Efficient Adaptation

**Job:** Establish that weight-modification approaches are the standard approach, then argue they are both unnecessary (required abilities already exist) AND counterproductive (actively narrows distribution, harms generalization). Rules out the entire parameter-modification design space. Positions inference-time intervention as the right approach.

**Core ideas:**
- Weight modification is the most established approach
- Variants: full fine-tuning, PEFT (LoRA, adapters, prefix tuning). All modify the learned distribution
- Instruction tuning: often framed as generalization, but is still distributional narrowing
- Knowledge distillation: student still has same dimensional bottleneck
- All approaches narrow distribution toward training task, degrading performance outside it. Counterproductive for our goal
- Weight modification addresses a problem that is not the bottleneck (ICL and language understanding survive downscaling)
- The deficit is parametric but the fix is input-side. Provide structure in the input rather than relying on weights

**Sets up:**
- §2.4: inference-time alternatives that avoid retraining
- §3 (Architecture): framework operates on any model as-is, no weight updates

**Does NOT cover:**
- What inference-time approaches look like (that's §2.4, §2.5)
- The mechanistic argument for why structure specifically (that's §2.6)

---

## §2.4 Prompt Engineering and In-Context Learning

**Job:** Establish that prompt engineering works at any scale and that structure in the input helps. Show ICL is the mechanism. Establishes viability of input-side interventions.

**Core ideas:**
- Prompt engineering is the category of input-side interventions
- Zero-shot and system/instruction prompting provide task-level context (uniform across all questions)
- Few-shot and many-shot provide example input-output pairs
- CoT provides generic process structure; variations include ToT and Self-Consistency
- Common principle: additional context narrows the prediction space; each technique narrows differently
- ICL defined: the mechanism enabling all of the above
- ICL is scale-independent: operates through attention (architectural), not stored parameters (capacity-dependent)

**Sets up:**
- §2.5: RAG applies same principle but automates content selection through retrieval
- §2.6: synthesizes what's still missing after §2.3–§2.5

**Does NOT cover:**
- RAG (that's §2.5)
- Gap claims or "what's missing" (that's §2.6's synthesis job)
- Answer structure definition (that's §2.8)

---

## §2.5 Retrieval-Augmented Generation

**Job:** Show that RAG demonstrates structure with specific, relevant information produces better results than generic structure alone. Advances the escalation: §2.4 shows structure helps; §2.5 shows specificity and organization together outperform either in isolation.

**Core ideas:**
- RAG is an inference-time system that automates prompt construction through retrieval from external corpus
- Distinction from prompt engineering: same input-side principle, different context origin (external knowledge source indexed at runtime vs prompt author's design)
- Question-decomposition RAG: simplifies complex info needs into focused retrieval targets, provides more precise content
- Corrective RAG: filters low-quality retrievals, prevents degraded output
- Synthesis: organization and specificity together outperform either in isolation

**Sets up:**
- §2.6: can synthesize what's missing across §2.3–§2.5 (none provide matched output structure)
- §2.8: must differentiate "answer structure" from "structured RAG" (output-side vs retrieval-side)
- §8 (Future work): structure-aware retrieval (answer structure as retrieval guide)

**Does NOT cover:**
- The gap argument or "what's still missing" (that's §2.6)
- Prediction space / generation space language (that's §2.6)
- Definition of answer structure (that's §2.8)
- Self-RAG / output-structuring RAG (dropped for now; steelman if committee raises it)

---

## §2.6 Unconstrained Prediction

**Job:** Serve as the PIVOT from "here's what exists" to "here's what's missing." Reframe hallucination as unconstrained prediction. Synthesize preceding sections: none provide the specific type of narrowing needed. Set up answer structure as the solution direction.

**Core ideas:**
- "Hallucination" = output that doesn't match expected answer (literature's definition)
- Reframe: same mechanism produces all output; no separate failure mode; unconstrained prediction
- Parameters determine baseline distribution; small models approximate at lower resolution (dimensional bottleneck)
- Approximation compounds during autoregressive generation (imprecision propagates)
- Compounding cannot be eliminated but scope reduced by narrowing output space
- The preceding sections reviewed approaches that reduce the prediction space: weight modification (§2.3), prompting (§2.4), retrieval (§2.5)
- Answer structure reduces space by providing output form (model populates content)

**Sets up:**
- §2.7/§2.8: how to identify and define the right structure
- §3 (Architecture): the mechanism that provides output form

**Does NOT cover:**
- Detailed discussion of any single approach (those live in §2.3–§2.5)
- Definition of answer structure (that's §2.8)
- The taxonomy or classifier (that's §2.7/§2.8/§3)

**NOTE:** Needs re-review after §2.5 revision. Claim 6 references §2.5 and may need softer language now that §2.5 no longer makes explicit gap claims.

---

## §2.7 Question Classification in QA

**Job:** Establish that question type classification is recognized prior art, grounding the classifier component in existing work. Distinguish question types from answer structure types.

**Core ideas:**
- Classical QA recognizes question classification as preprocessing
- Cognitive science: experts categorize problem type before solving
- Different question types require structurally different reasoning
- Prior work classifies question types but not the structure a valid answer must take

**Sets up:**
- §2.8 (Answer Structure Types): the taxonomy hypothesis

**Does NOT cover:**
- The taxonomy itself (that's §2.8)
- The classifier architecture (that's §3)

---

## §2.8 Answer Structure Types: A Taxonomy Hypothesis

**Job:** State the novel hypothesis: answer structure types are finite, enumerable, classifiable from question text alone. Define what an answer structure IS.

**Core ideas:**
- Not all questions require the same answer structure
- Hypothesis: structural types are finite, enumerable, classifiable by an encoder
- An answer structure defines dimensions/components a valid answer must contain (not content)
- Implication: if structure classification is natural for humans and QA systems, an encoder can replicate it

**Must include (per concepts doc):**
- Explicit differentiation of "answer structure" from "structured RAG" (output-side vs retrieval-side)
- Differentiation from format-level output constraints (JSON, templates — generic, not question-matched)
- CoT deep-dive: why process-level structure is different from answer structure
- Formal, operational definition of answer structure

**Sets up:**
- §3 (Architecture): the classifier and taxonomy are the implementation of this hypothesis

**NOTE:** Placement decision deferred — may belong in §3 since it IS the novel contribution. Revisit after all sections complete.
