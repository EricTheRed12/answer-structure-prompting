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
- §2.5: RAG shows that specificity matters; organization of retrieval matters; but still relies on model to organize output
- §2.6: The model is deterministic; input defines trajectory; when input lacks context, output diverges; existing techniques don't provide matched structure
- §2.7: Question classification exists; we propose answer classification; it satisfies the requirements
- §2.8: Answer structure defined; examples; mechanistic why; enables generalization; finiteness hypothesis
- §2.9 (planned): Related/adjacent work distinguished from our contribution

---

## §2.1 Large Language Models — PROSE COMPLETE

**Job:** Establish how the technology works at the architectural level.

**Core ideas:**
- Transformer architecture, self-attention
- LLMs are probabilistic token predictors (probability engines, not knowledge databases)
- Autoregressive decoding: one token at a time, no lookahead, no revision, early tokens propagate
- Output is a probability distribution over the full vocabulary at every step
- What the model receives as input directly determines the distribution

**Sets up:**
- §2.2 can discuss what scale adds without re-explaining the mechanism
- §2.6 can invoke determinism and trajectory without re-explaining autoregressive decoding
- §3 (Architecture) can reference encoder vs decoder distinction

---

## §2.2 Scale and Structure — PROSE COMPLETE

**Job:** Establish that the performance gap between large and small models is partly structural, not purely about knowledge capacity, and that external structure can partially close it.

**Core ideas:**
- Scale = parameter count; dominant performance predictor (scaling laws)
- Larger models outperform smaller ones (demonstrated: GPT-3 175B vs 1.3B)
- Gap is conditional, not absolute: small models with context match large ones
- Small models are architecturally identical; same system, lower-resolution approximation
- Author's argument: advantage of scale is structural (image resolution analogy)
- Structural patterns are statistically encoded and non-deterministic
- External structure (brevity constraints) compensates; structure determines quality
- Prompting alone does not solve generalization

**Sets up:**
- §2.3 references distributional narrowing
- §2.4 discusses prompt engineering as partially structural
- §2.6 references parametric resolution and the "limited resolution" framing

---

## §2.3 Fine-Tuning and Parameter-Efficient Adaptation — PROSE COMPLETE

**Job:** Establish that weight-modification approaches are standard, then argue they are unnecessary AND counterproductive for generalization. Rules out the entire parameter-modification design space.

**Core ideas:**
- Weight modification is the established approach (full fine-tuning, PEFT, LoRA, adapters, prefix tuning)
- Instruction tuning: distributional narrowing, not generalization
- Knowledge distillation: student has same dimensional bottleneck
- All approaches narrow distribution toward training task; counterproductive for general-task goal
- ICL and language understanding survive downscaling (the deficit isn't in capability)
- The fix is input-side: provide structure in the input

**Sets up:**
- §2.4: inference-time alternatives that avoid retraining
- §3: framework operates on any model as-is, no weight updates

---

## §2.4 Prompt Engineering and In-Context Learning — PROSE COMPLETE

**Job:** Establish that prompt engineering works at any scale and that structure in the input helps. Show ICL is the mechanism. Establishes viability of input-side interventions.

**Core ideas:**
- Prompt engineering: category of input-side interventions
- Variations: zero-shot, few-shot, chain-of-thought (landscape)
- Common principle: additional context narrows the prediction space
- ICL defined: the mechanism enabling all of the above (attention-based, not parametric)
- ICL is scale-resistant
- Prompting still requires model to produce from parametric capacity
- CoT degrades in small models (evidence of limitation)
- Takeaway: prompt with specific information (few-shot) offers a path worth exploring

**Sets up:**
- §2.5: RAG applies same principle but automates content selection
- §2.6: synthesizes what's still missing

**Notes:**
- MoE routing concept moved to §3 (Architecture)
- CoT deep-dive and "more defined structure helps" argument available for §2.8 if needed

---

## §2.5 Retrieval-Augmented Generation — PROSE COMPLETE

**Job:** Show RAG's value is in specificity. Organization of retrieval matters. RAG is generalizable and scale-resistant. But still relies on model to organize output. Close with: "a prompt needs to provide everything but the answer."

**Core ideas:**
- RAG defined: inference-time, retrieves from external source, constructs prompt
- Distinction from prompting: same mechanism (ICL), different source (retrieved vs authored); compatible together
- RAG's value is specificity: task-relevant tokens at inference time
- More tokens = more implicit relational structure for attention; ICL mechanism
- Organization matters: question-decomposition as example of structured retrieval > naive retrieval
- Generalizable, scale-resistant, applied across domains without modification
- Limitation: still relies on model's encoded information to organize output
- Closer: "To reduce the prediction space further, a prompt needs to provide everything but the answer."

**Sets up:**
- §2.6: what happens when the prompt doesn't provide everything but the answer

---

## §2.6 Unconstrained Prediction — PROSE COMPLETE

**Job:** Reframe hallucination as just prediction. Establish that the model is deterministic and input defines the trajectory. Show what happens when input lacks context. Identify the gap across existing techniques. State what's needed.

**Core ideas:**
- "Hallucination" is misleading: no alternative failure mode, just prediction from the distribution
- Temperature/seed create variety but don't improve generation; seed is the draw, temperature reshapes the distribution
- Input defines the trajectory (deterministic); only point of intervention
- If input lacks context, output diverges (CoT as evidence)
- Larger models have structure encoded; smaller models lack resolution
- Prompting provides generic structure; RAG provides specificity but not adapted form; combined still fails
- Closer: "To surpass the parametric barrier and enable generalization, what is needed is a structure that is task-independent in mechanism, specific to the task in its dimensions, and consistent in form."

**Sets up:**
- §2.7: how to identify the right structure (classification)
- §2.8: what that structure looks like (answer structure defined)

---

## §2.7 Question Classification in QA — PROSE COMPLETE

**Job:** Establish classification is feasible. Propose answer classification. Show it satisfies §2.6 requirements. Transition to §2.8.

**Core ideas:**
- Question classification is well-established (Li & Roth, 2+ decades, surface-level signals, extends across domains)
- We propose: if questions are classifiable and every question has an answer, answer structures are classifiable
- Question type determines answer form (examples: factual, analogical, multi-step)
- Not all relationships are equally explicit, but patterns are learnable
- BERT-style encoder could be fine-tuned for this taxonomy
- Taxonomy satisfies §2.6 requirements: content-independent patterns, explicit dimensions before generation, consistent across domains
- Closer: "What remains is a clear definition of this form."

**Sets up:**
- §2.8: defines what answer structures look like

**Notes:**
- Adjacent work (Han et al., Wu et al., Yadavalli, SMART, CEUR-WS) moved to planned §2.9

---

## §2.8 Answer Structure Types: A Taxonomy Hypothesis — PROSE COMPLETE

**Job:** Define answer structure. Show examples. Explain mechanistic why. Show it enables generalization. State finiteness hypothesis.

**Core ideas:**
- Definition: schema specifying what a valid answer must contain without specifying the answer itself; dimensions = required components
- Structure provides explicit relational context, constraining prediction space before generation
- Model's remaining task: populate the structure with relevant content
- Examples: relational, causal, procedural (each with numbered dimensions); pattern = subjects, mechanism of relation, joining details
- Figure: JSON schema (empty → populated by model)
- Mechanistic why: dimensional hooks as input tokens; more tokens = more constrained attention = sharper distribution; compensates for limited parametric resolution in small models
- Generalization: same process across problems (classify, provide, populate); only the structure changes; unlike few-shot, provides pattern directly
- Finiteness hypothesis: space is bounded; six interrogatives at top level; subtypes at any granularity; static taxonomy enables automation through classification
- "Content is infinite while form is bounded."

**Sets up:**
- §3 (Architecture): the pipeline that implements this (classifier + scaffold + generator)
- §2.9 (planned): distinguishes from adjacent work

---

## §2.9 Related Work (PLANNED — not yet written)

**Job:** Distinguish this paper's contribution from adjacent work. Show awareness of landscape. Carve out novelty.

**Planned content (moved from §2.7):**
- Han et al. (2025): reasoning blueprints — reasoning process, not output form; task-category level, not per-question
- Wu et al. (2025): TemplateRL — reasoning strategy templates via RL training, not inference-time
- Yadavalli (2025): dynamic template selection — cost optimization, not accuracy; verbosity control, not structural form
- SMART (Setty 2023): answer entity type prediction — predicts WHAT (entity type), not HOW (structural form)
- CEUR-WS (2021): semantic answer type prediction — same distinction as SMART
- Conclusion: no existing work classifies questions to select structural template defining answer form as input constraint before generation

**Sets up:**
- Nothing — this is the final lit review section before §3
