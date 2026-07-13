---
inclusion: auto
---

# Thesis Writing Rules

## Format

- All thesis sections should be written as **bullet-point claims only** — no prose paragraphs.
- Each bullet point represents a single claim made in the paragraph it will eventually become.
- Do not write out full paragraphs unless explicitly asked.

## Citations

- Every claim that is not the author's own contribution must have an associated citation.
- **All suggested citations must be reviewed before being considered final.** Mark unverified citations clearly.
- When uncertain about whether a citation supports a claim, flag it for manual review rather than assuming it fits.
- **All unverified citations must be flagged with a confidence rating (HIGH / MEDIUM / LOW)** in the Citation Verification Tracker below.
  - **HIGH** — Title/abstract directly states the claim; venue is strong; very unlikely to be wrong
  - **MEDIUM** — Abstract supports inference but specific claim not confirmed in full text; could be slightly off-target
  - **LOW** — Speculative match based on topic area; needs full read before relying on it

## Key Conceptual Notes

### Terminology: "answer structure" (NOT "reasoning structure")
**DECISION (author):** Use **"answer structure"** consistently everywhere. Do NOT use "reasoning structure" — it is too hard to both define and prove, and it invites confusion with CoT-style reasoning chains (which §2.6 explicitly distinguishes the framework from).

Places that currently drift and MUST be reconciled to "answer structure":
- **Title:** "Generative Contextual *Reasoning* Prompts" → reconsider wording so it does not promise "reasoning."
- **§1.2 research question:** "external *reasoning* structure" → "external answer structure."
- **§1.1 Hook:** "peripheral for reasoning" phrasing → align to answer structure (will be handled in Hook rewrite).
- Abstract, §1.4 Purpose, §3 Architecture already use "answer structure" — these are the correct baseline.

### "Small models" definition
When the paper refers to "small models" or "small language models" in the Problem Statement and elsewhere, it means **small autoregressive decoder LLMs** (same architecture as GPT, just fewer parameters — e.g. Llama 3B, Phi-2, Mistral 7B). Not encoder models like BERT, and not classical NLP. The classifier component in the framework is a separate BERT-style encoder — that distinction should remain clear in context.

### Answer Structure as Dimensional Framework
The answer structure does not provide the answer itself — it provides the *dimensions that matter* for a given type of problem. The model then populates those dimensions with whatever relational knowledge it already has.

**Example:** A structure for "how to identify a sport" might include: name, tools used to play, where it is played. A small model that has fragments (soccer, ball, field) in its parameters — even if it doesn't deeply "know" soccer — can use the structure to organize those fragments into a coherent answer. The structure tells the model *what to look for*, not *what the answer is*.

This is the core mechanism: small models have relational fragments scattered in parameter space. They lack the organizational structure to know what to do with those fragments when asked a question. The answer structure provides that organization.

### ⚠️ CRITICAL: The definition of "answer structure" is load-bearing for the entire paper
**This is the single most important definition in the thesis. Get it right before anything downstream depends on it.**

Why it matters:
- Every core claim rests on it — the central hypothesis ("an answer structure *matched to the question*"), the core mechanism ("dimensions that matter"), the operating premises, the classifier's output space (Component 1), and the scaffold's contents (Component 2). If "answer structure" is fuzzy, all of these become fuzzy.
- It is the term that distinguishes this work from everything adjacent: RAG (retrieves *content*), CoT (generates a *reasoning path*), question-type classification (labels the *question*). Our contribution is classifying the *structure the answer must take*. A weak definition collapses that distinction and invites "isn't this just X?" objections.
- It carries the whole generalization argument: the claim that a *finite* set of answer structures can cover a task only makes sense if "answer structure" is defined precisely enough to be enumerable and to be told apart from a "question type."
- The classifier can only be trained/evaluated against a definition concrete enough to label consistently — vague definition → unlabelable data → no RQ3.

Requirements for the definition (to be written crisply in §2.7 and §3):
- State what an answer structure IS: the set of dimensions/components a valid answer to a question must contain (NOT the answer content itself).
- Distinguish it explicitly from "question type" and from "reasoning path."
- Make it operational: concrete enough that two annotators (or the data-generating model) would assign the same structure to the same question.
- Ground it with worked examples (e.g. sport → name, tools used, where played).
- §1.4 Purpose only gives the intuition ("dimensions that matter"); the FORMAL, load-bearing definition must live in §2.7/§3.

- [ ] Review all suggested citations in the Hook section for accuracy (do they actually say what we claim?)
- [ ] Specifically verify: `rag_survey2023`, `cot_mirage2025` — confirm they discuss shortcomings/limitations
- [ ] Specifically verify: `modelsizematters2024` — confirm it shows small models competing with large ones
- [ ] Specifically verify: `cot_limitations2025` — confirm it shows CoT underperforming in some cases
- [ ] Specifically verify: `costofdownscaling2023` — confirm fact recall drops but comprehension survives
- [ ] Specifically verify: `nonfactoid_taxonomy2022` — confirm it defines answer types (not just question types); check if it provides example answer structures that could serve as inspiration for our taxonomy
- [ ] Specifically verify: `liroth2002questions` — confirm finite question type classification with learned classifier
- [ ] Consider enhancing Claim 3 to strengthen the "comprehension survives scale" argument — find additional evidence for why language understanding is preserved when model size shrinks

## ⭐ DEFERRED MILESTONE: Full-text citation verification (after ALL claims are done)
**Author intent:** once every section's claims are finalized, do a dedicated pass to verify EVERY cited paper against its FULL TEXT — not just the abstract/snippet.

Why this is a separate pass:
- Everything verified so far (esp. §1.4) was checked against abstracts, TL;DRs, and search snippets only. That is NOT sufficient for final confidence.
- Abstracts can support a claim that the full paper actually qualifies, contradicts, or scopes narrowly. Need to read methods/results/limitations.

How to run it (when the time comes):
- Go citation by citation through the Citation Verification Tracker below.
- For each: read the full paper (PDF/HTML), confirm the specific claim it's attached to is actually supported in the body, check scope/caveats, then flip Status to "✅ Full-text verified" (or fix/replace).
- Pay special attention to entries currently marked "various" as author (many bib entries have placeholder authors) — confirm real authorship/venue too.
- Priorities flagged from the §1.4 abstract-level pass: `costofdownscaling2023` (confirm the fact-recall-vs-ICL split holds as worded), `nonfactoid_taxonomy2022` (confirm the non-factoid scope doesn't undercut general use), `xie2022icl` (confirm the "uncertainty collapses with few examples" framing).
- Also: many bib entries have `author = "various"` placeholders — fix real author lists during this pass.

## Citation Verification Tracker

### Hook Section

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `kaplan2020scaling` | Large models superior but resource-constrained | HIGH | arXiv (2700+ citations) | Unverified |
| `strubell2019energy` | Resource constraints | HIGH | ACL 2019 | Unverified |
| `patterson2021carbon` | Resource constraints | HIGH | arXiv (Google) | Unverified |
| `smalllmsready2024` | Small models compete with large | MEDIUM | arXiv | Unverified |
| `modelsizematters2024` | Small models compete with large | MEDIUM | arXiv | Unverified |
| `wei2022cot` | CoT can improve small model performance | HIGH | arXiv (highly cited) | Unverified |
| `cot_limitations2025` | CoT has shortcomings | MEDIUM | arXiv | Unverified |
| `cot_mirage2025` | CoT has shortcomings | MEDIUM | arXiv | Unverified |
| `lewis2020rag` | RAG can improve small models / given right peripherals | HIGH | NeurIPS 2020 | Unverified |
| `rag_survey2023` | RAG has shortcomings | MEDIUM | arXiv | Unverified |
| `devlin2019bert` | Small models comprehend language | HIGH | NAACL 2019 | Unverified |
| `liu2019roberta` | Small models comprehend language | HIGH | arXiv | Unverified |
| `costofdownscaling2023` | Comprehension survives downscaling | MEDIUM | arXiv | Unverified |
| `liroth2002questions` | Finite question type classification | HIGH | COLING 2002 | Unverified |
| `nonfactoid_taxonomy2022` | Finite answer structures exist | HIGH | SIGIR 2022 | Unverified |

### Problem Statement

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `eloundou2023gpts` | LLMs are transformative (labor market impact) | MEDIUM | arXiv / Science 2024 | Unverified |
| `llm_critical_societal2024` | LLMs are transformative (healthcare, finance, law) | MEDIUM | arXiv | Unverified |
| `llmoverview2023` | LLMs are transformative (general survey) | MEDIUM | arXiv | Unverified |
| `liesenfeld2024closed` | Most capable are closed/proprietary; training decisions concentrated; "open" isn't open | HIGH | Nature 2024 | Unverified |
| `kapoor2024societal` | Concentrated control limits contributions | MEDIUM | arXiv / ICML 2024 | Unverified |
| `bommasani2023fmti` | No external input on training; can't be audited | HIGH | arXiv (Stanford) | Unverified |
| `liesenfeld2024openwashing` | "Open-source" models aren't truly open | HIGH | ACM FAccT 2024 | Unverified |
| `strubell2019energy` | Environmental cost | HIGH | ACL 2019 | Unverified |
| `patterson2021carbon` | Environmental cost | HIGH | arXiv (Google) | Unverified |
| `modelsizematters2024` | Small models underperform | MEDIUM | arXiv | Unverified |
| `kaplan2020scaling` | Limited parametric capacity; hard cap | HIGH | arXiv (2700+ citations) | Unverified |
| `costofdownscaling2023` | Can't encode everything; brittleness | MEDIUM | arXiv | Unverified |
| `devlin2019bert` | Both model sizes understand language | HIGH | NAACL 2019 | Unverified |

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `strubell2019energy` | Only well-resourced orgs (cost barrier) | HIGH | ACL 2019 | Unverified |
| `slm_survey2024` | Only well-resourced orgs; small models accessible to researchers; domain training | MEDIUM | arXiv (Penn State, 14 authors) | Unverified |
| `domain_expert_smalllm2024` | Small models trained on domains match experts | MEDIUM | arXiv | Unverified |

### Purpose of the Paper (§1.4)  — reviewed via web search

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `devlin2019bert` | Encoder classifier maps question → structure type | HIGH | NAACL 2019 | ✅ Verified (canonical fit) |
| `costofdownscaling2023` | Core mechanism: in-context ability survives down-scaling | MEDIUM | ICLR 2024 / arXiv | ✅ Verified; claim REWORDED to match |
| `xie2022icl` | Scaffold narrows probability space (few examples reduce task uncertainty) | HIGH | ICLR 2022 | ✅ NEW — direct fit, replaced stochastic paper |
| `liroth2002questions` | Answer structure inferable from question text | HIGH | COLING 2002 | ✅ Verified (canonical fit) |
| `nonfactoid_taxonomy2022` | Finite set of answer structure types exists | HIGH | SIGIR 2022 (Best Paper) | ✅ VERIFIED — direct hit |
| `smalllmsready2024` | Generator can be any small model | MEDIUM | arXiv | ✅ Keep (carries the claim) |
| `slm_survey2024` | Generator can be any small model | MEDIUM | arXiv (Penn State) | ✅ NEW here — replaced modelsizematters2024 |

APPLIED CHANGES (this session):
- Generator claim: dropped `modelsizematters2024` (requirements-classification, wrong support), added `slm_survey2024`.
- Core-mechanism claim: kept `costofdownscaling2023`, REWORDED claim to credit surviving in-context learning ability (not "retained fragments" — parametric recall is what degrades).
- Probability-space claim: replaced `llmreasoning_stochastic2024` with NEW `xie2022icl` (Xie/Raghunathan/Liang/Ma, ICLR 2022 — ICL as implicit Bayesian inference; few examples collapse task uncertainty). New bib entry added. `llmreasoning_stochastic2024` still used in §1.2/§2/§3, remains in bib.
- [x] Metadata bug FIXED: `llmreasoning_stochastic2024` bib year corrected 2024 → 2025 (matches arXiv 2512 = Dec 2025). Key name left unchanged to avoid churn across §1.2/§2/§3.

#### §1.4 citation review findings (web-verified)
- **`nonfactoid_taxonomy2022` — VERIFIED direct hit.** SIGIR page: presents "the first comprehensive taxonomy of NFQ categories and **the expected structure of answers**"; finite label set (FACTOID, DEBATE, EVIDENCE-BASED, INSTRUCTION, REASON, EXPERIENCE, COMPARISON); SIGIR 2022 Best Paper. Directly supports "finite set of answer structure types." CAVEAT: scoped to non-factoid QA — note that when leaning on it.
- **`costofdownscaling2023` — VERIFIED but claim wording needs a tweak.** Actual finding (OpenReview TL;DR + ICLR 2024): fact recall degrades past ~30% down-scaling, BUT in-context learning withstands aggressive down-scaling. So it supports "small models can USE a provided scaffold (ICL survives)" — NOT "relational fragments it already RETAINS" (parametric recall is exactly what degrades). ACTION: reword core-mechanism claim to emphasize the model's surviving ability to *use context/structure*, not retained parametric knowledge. The "or retrieves" addition is consistent with this.
- **`modelsizematters2024` — VERIFIED WEAK.** It's about REQUIREMENTS CLASSIFICATION (software-eng), SLMs nearly matching LLMs there. Supports "small models compete on a narrow task," NOT "any small model is a capable generator." ACTION: drop from generator claim; pair `smalllmsready2024` + `slm_survey2024` instead.
- **`llmreasoning_stochastic2024`** — OK as grounding for "LLMs are stochastic probability engines," but does NOT show scaffold-narrowing→improvement (that's our inference). METADATA BUG: bib year=2024 but arXiv id 2512.x = Dec 2025. If the narrowing→improvement link needs a cite, use `brown2020gpt3`/`manyshot2024`.
- `devlin2019bert`, `liroth2002questions` — canonical, no concern.

#### Central vs enabling hypothesis reframing (DONE)
Author decision: the point of the paper is NOT to prove the answer-structure set exists — it ASSUMES the set exists and shows that WITH it, small LLMs get better.
- **Central hypothesis** (what the experiments test, RQ1/RQ2): conditioning a small LLM on the correct answer structure improves its accuracy enough to narrow the gap with larger models. Added as an explicit claim near the top of §1.4.
- **Operating premises (assumed, not proven):** (a) a finite set of answer structure types is sufficient to cover a task — assumed and constructed, not proven; (b) answer structure is determined by the question's semantic context and inferable from the question alone (general mapping is out of scope, could be its own paper).
- **Classifier learnability:** the "answer structure type is learnable by a classifier" point was briefly added to §1.4 as an "enabling hypothesis," then REMOVED — it over-detailed the Purpose section. The classifier is already covered in the pipeline (Component 1). Its feasibility evaluation (RQ3) and the point that the oracle/manually-assigned-scaffold condition decouples the central claim from classifier accuracy both belong in §4 Methodology / §5 Discussion, NOT in Purpose.
- The old "Central hypothesis: finite taxonomy exists and is learnable" was mislabeled — demoted (existence → premise; learnability → not a Purpose-level claim, handled in §4).
- **ABSTRACT SYNCED:** abstract now states the gap-closing central hypothesis and lists the finite-taxonomy claim as an "enabling assumption."

#### Claim 5 split (DONE) + resulting §4 methodology item
- Old bundled "central hypothesis" claim split into three by epistemic status:
  1. **Operating premise** (adopted, NOT proven here): answer structure is dictated by question form (type, entities, actions), so it's inferable from the question alone. Establishing this mapping in general is its own paper / out of scope. Author intent: this must read as an assumption, not a demonstrated result.
  2. **Central hypothesis (this paper, scoped):** for a bounded task, a finite set of answer structure types is sufficient and learnable by a classifier from question text.
  3. **Scope/conjecture:** MCQA is a **proof of concept only**; generalization to the general question space is hypothesized, explicitly NOT demonstrated. ("covers the general question space" was moved out of the hypothesis into here.)
- [ ] **§4 METHODOLOGY — labeling mechanism:** training labels for answer structure type are assigned by the data-generating (large) model, offline. Must state this in classifier-training methodology so the "learnable from question text alone" claim isn't circular. The LLM is only a data-generation tool, not part of the framework (see removed claim 7).
- [ ] Author frame to preserve throughout: "if I had time, identifying answer structure from a question could be its own paper" — keep MCQA-as-proof-of-concept boundary explicit in every section.

#### Purpose polish pass (claims 1–5 review)
- [x] **1. "close" → "narrow" the gap.** Author intent: framework makes small LLMs *more effective*, NOT surpass large models. This alone won't close the gap — more components would be needed. Use "narrow" everywhere; never "close/surpass."
- [ ] **2. Gap-vs-larger-models comparison — WHERE does it live? (decide later).** Plan: compare scaffolded small models against BOTH (a) the small-model baseline and (b) existing published benchmark scores for large models (MMLU/ARC etc.) — i.e. don't run a large model, use its published benchmark number as the reference point. Author unsure this belongs in Purpose/§1.4. TODO: place the large-model-benchmark comparison in §4 Evaluation (and interpret in §5 Discussion); confirm claim 9 (evaluation) reflects it once decided. For now the central hypothesis references "larger models" but the eval bullet does not — reconcile when §4 is written.
- [x] **"appropriate" → "matched to the question".** "Appropriate answer structure" was vague/circular (appropriate for what?). Changed central hypothesis to "an answer structure **matched to the question**" — concrete, ties to the operating premise (structure determined by the question) and to Component 1 (classifier does the matching).
- [ ] **DEFINE "answer structure" crisply in §2.7/§3.** Purpose (§1.4) leans heavily on the term but only gives intuition ("dimensions that matter"). The formal definition lives in the taxonomy sections — make sure it's explicit there since the whole paper rests on it. (Steering example: sport → name, tools used, where played.)
- [x] **3. "correct" → "appropriate" answer structure.** Central hypothesis now says "an appropriate answer structure" (author rejected the verbose "need not be exact, only close enough" clause — kept the claim clean). Author's underlying view still holds: a *close enough* structure suffices, not just the single exact one — but express that in §4/§5, not in the hypothesis line. Also: core-mechanism claim now says fragments the model "retains **or retrieves**" — deliberately leaves room to combine with RAG. NOTE the tension to resolve in §4/§5: the ablation condition uses a RANDOM (wrong) scaffold to prove correct structure matters — so "close enough suffices" implies a tolerance band between "close enough" (helps) and "wrong" (random, doesn't help). Methodology/Discussion should address where that boundary is (robustness to classifier near-misses). This robustness is a plus — classifier need not be perfect.
- [x] **4. Terminology fix:** claim 5 "for a given question type" → "for a given question" (was reintroducing old "question type" vocab; keep "answer structure" consistent).
- [x] **5. Redundancy tightened:** claim 3 keeps "no weight updates to the generator"; claim 4 reduced to "The generator can be any small model that understands English" (dropped duplicate "no fine-tuning").

#### Novelty claim in Purpose — DECISION: NO (do not add)
Considered adding an explicit "unlike RAG/CoT/question-classification, we classify answer structure" novelty line to §1.4. Decided against it: novelty is already asserted in §1.2 (Problem Statement gap + research question) and detailed in §2.6 (prompt-engineering gap summary = "the novel contribution") and §2.8 (RAG differentiation). Adding it to Purpose = triple repetition (same failure we removed from the Hook). Purpose stays lean — its job is what we DO about the gap, not re-argue the gap. Novelty lives in §1.2 and §2.

#### Purpose section open items
- [x] **"Offline, disposable LLM" claim — REMOVED.** Author's call: the large model is only a tool for generating classifier training data (which could be produced other ways), not part of the proposed framework's architecture. Does not belong in Purpose or Architecture as a framework component.
- [ ] **Core-mechanism claim citation** — the "dimensions that matter, not the answer" mechanism is the author's own hypothesis (no cite needed); `costofdownscaling2023` is attached only to the "retains fragments" sub-claim. Verify it actually shows fragment retention under downscaling, else drop the cite and leave the claim uncited as author contribution.
- [ ] Opening framing claim intentionally uncited (author's own contribution).

### Legacy review items
- [ ] Consider enhancing Hook Claim 3 to strengthen the "comprehension survives scale" argument — find additional evidence for why language understanding is preserved when model size shrinks
- [ ] Verify `nonfactoid_taxonomy2022` defines answer types (not just question types); check if it provides example answer structures for our taxonomy
- [ ] Verify `liroth2002questions` finite question type classification with learned classifier


## Process Notes (for continuing sessions)

### What we did for the Hook section:
1. Identified the claims being made in the section (bullet points, not prose)
2. Reviewed each claim for accuracy and correct framing
3. Iterated on wording with the author until each claim felt right
4. For each finalized claim, reviewed the associated citations:
   - Does the citation actually support what the claim is saying?
   - Is it peer-reviewed? How well-cited?
   - Are we relying on it only because it was already in the bib, or is it the best fit?
   - Are there better papers we should find?
5. Searched for additional/replacement papers where needed and added to `sample.bib`
6. Updated the tex with revised claims and corrected citations
7. Flagged citations that need full verification for later literature review

### Next sections to process (same approach):
- [ ] The Hook (§1.1) — **NEEDS REWRITE after Problem Statement and Purpose are finalized.** Current version overlaps significantly with Problem Statement (claims 1, 3, 4 are restated). Hook also previews the solution (pipeline, hypothesis, scope) which may duplicate Purpose. Rewrite to: short pitch that previews the final argument, not an earlier draft. Also update citations (BERT/RoBERTa → decoder-specific papers for the "comprehension" claim). **See detailed rewrite plan below.**
- [x] The Purpose of the Paper (§1.4) — first pass done (claims reviewed/revised, citations logged). Two open decisions parked in Purpose tracker (offline-LLM claim placement; core-mechanism cite verification).
- [ ] Literature Review (§2) — all subsections

### Hook rewrite plan (§1.1) — DETAILED, do this next
Goal: Hook does ONLY the "why care" job (broad stakes). Strip everything that belongs to Problem Statement (§1.2) or Purpose (§1.4). This removes the "said three times" feeling where "small models comprehend but lack depth" repeats across Hook/§1.2.

Claim-by-claim changes to the current Hook:
- **Claim 1** (LLMs superior but resource-constrained) — REFRAME. Drop the cost/energy lead (that's §1.2). Reframe to broad stakes: LLMs are transformative AND the best are closed/concentrated. Cites: `eloundou2023gpts`, `llmoverview2023`, `liesenfeld2024closed`.
- **Claim 2** (small models compete; RAG/CoT help but fall short) — COMPRESS to one sentence. Naming techniques + shortcomings belongs in §2.6 and §1.2. Drop the 7-citation pileup. Keep at most: small open models compete on narrow tasks, lag on general use. Cite: `modelsizematters2024`.
- **Claim 3** (comprehension survives, deficit is associative depth) — DELETE from Hook. This is THE §1.2 reframe (stated twice there already). Also fixes the citation bug: `devlin2019bert`/`liu2019roberta` are encoder papers used for a decoder claim — when this lives in §1.2, swap for decoder-specific evidence (`costofdownscaling2023`, `linguistic_competence_scale2025`, `emergent_reducedscale2024`).
- **Claim 4** (finite-answer-structure hypothesis + classifier) — DELETE from Hook. This is Purpose (§1.4 central hypothesis). Hook must not reveal the mechanism.
- **Claim 5** (multiple choice QA scope, designed to generalize) — DELETE from Hook. Scope lives in Purpose (§1.4).

Target Hook after rewrite (~4 light claims):
1. LLMs are transformative, reshaping how we work with information `[eloundou2023gpts, llmoverview2023]`
2. but the most capable are large, closed, expensive — concentrating access/control `[liesenfeld2024closed, strubell2019energy]`
3. small open models are accessible to anyone but underperform on general tasks `[modelsizematters2024]`
4. one tension/forward-pointing sentence — "closing that gap without scale is the challenge this paper takes on" — WITHOUT revealing taxonomy/classifier

Net: 5 dense claims → ~4 light claims; ~10 citations pushed down into §1.2/§1.4/§2.6 where they're actually argued; stop previewing the solution.

### Layout review (done this session)
- Top-level section order (Intro → Lit Review → Architecture → Methodology → Results → Discussion → Limitations → Conclusion) is sound, no change.
- Intro three-move split (Hook → Problem Statement → Purpose) is the right pattern; only the Hook does the wrong job (see rewrite plan).
- Numbering note: Hook/Problem/Purpose are §1.1/§1.2/§1.3 by doc order but notes call Purpose §1.4 — no §1.3 exists between them. DECIDE: add an explicit Contributions subsection (common in CS theses) or let Purpose absorb that role.

### Key principles established:
- The paper is about small language models + answer structure classification
- Two hypotheses: (1) small models comprehend language, they lack associative depth; (2) finite answer structures exist for any problem set
- Framework: encoder classifier identifies answer structure → scaffold guides any small LLM (no fine-tuning required)
- LLM is only used once to generate taxonomy/training data (offline, disposable)
- Answer structures provide *dimensions that matter*, not answers themselves
- The framework should work with any small LLM, trained or untrained (comparing both)
- Tested on multiple choice QA, but designed to generalize

### Adjacent work reviewed:
- Han et al. 2025 "Blueprints" (arXiv:2506.08669) — similar concept but uses LLM at training time, task-specific blueprints, not answer-structure classification. Our work is novel because: no LLM dependency at runtime/training, domain-agnostic taxonomy, classifier-driven routing.

### Problem Statement session notes (to pick up next time):
- **DONE:** Problem Statement is complete — 20 claims, full citation coverage, all reviewed
- Structure: LLMs transformative → not open → concentrated control harmful → "open" isn't open → large models costly/exclusive → constraints inherent to scale (transition) → small models limited → how they're limited → reframing (comprehension survives, deficit is depth) → small models accessible/domain-trainable but specialization costs generality → existing approaches don't structure the response → hypothesis → research question
- All new citations added to bib and logged in the Citation Verification Tracker with confidence ratings
- Key citations added this session: liesenfeld2024closed (Nature), kapoor2024societal, bommasani2023fmti, liesenfeld2024openwashing, eloundou2023gpts, llm_critical_societal2024, slm_survey2024, domain_expert_smalllm2024, linguistic_competence_scale2025, emergent_reducedscale2024 (NAACL), catastrophic_forgetting2023

### AUTHOR PLAN (stated): draft claims + citations for the REST of the paper
Before/instead of doing the Hook next, the author wants to write the claim bullets + citations for the remaining undrafted/outline sections — Literature Review (§2), Architecture (§3), Methodology (§4), Discussion (§5), Limitations (§6), Conclusion (§7) — using the SAME workflow used for Problem Statement and Purpose (identify claims → refine wording → review/verify citations). Hook rewrite + full-text citation verification come AFTER claims across the paper are drafted.

### MASTER REWRITE / WRITE LIST (as of end of Purpose session)
**A. Claims that need REWRITING (content exists, must change):**
1. **Hook §1.1** — full rewrite (detailed plan logged above). Includes swapping encoder cites (devlin/roberta) off the "comprehension" claim.
2. **§1.2 research question** — "external *reasoning* structure" → "external *answer* structure" (terminology decision).
3. **Title** — "Generative Contextual *Reasoning* Prompts" → reconsider to drop "reasoning" (terminology decision).
4. **§2.1 Large Language Models** — un-comment and place the "Relocated claims from earlier Problem Statement draft" block (lines ~102–109).
5. **§2.6 Prompt Engineering (CoT)** — develop the CoT argument (NOTE at ~line 182): frame as "we argue" that CoT is self-generated reasoning / context accumulation, not external structure; cite cot_mirage2025 + cot_limitations2025; do NOT overstate (CoT does help large models).

**B. [NEED PAPER] / citation-fill items (write claim is fine, needs a source):**
- §2.3 Generalization: Wei et al. 2022 "Emergent Abilities of LLMs" (currently analogical_reasoning2022 placeholder).
- §2.4 Problem with Scale: brevity/constraint paper arXiv:2604.00025 (large underperforms small).
- §2.7 Taxonomy: cognitive-science taxonomy (Bloom's / Kahneman dual-process); TREC fill (liroth2002questions now in bib — drop the NEED PAPER); Kahneman dual-process review.
- §4 Methodology: ARC / MMLU / HellaSwag dataset citations.

**C. Sections needing the full claims+citations pass (author's next goal):**
- §2 Literature Review (all subsections) — incl. the CRITICAL load-bearing "answer structure" definition (see ⚠️ note) which belongs in §2.7/§3.
- §3 Architecture — taxonomy definition + derivation; citation review.
- §4 Methodology — plus Purpose carry-forwards: large-model benchmark comparison, "close enough" tolerance vs random-scaffold ablation, offline labeling mechanism.
- §5 Discussion, §6 Limitations (currently just "TBD"), §7 Conclusion.
- Abstract + Results — result previews are "TBD after experiments" (fill post-experiment).

### NEXT SESSION:
- [x] The Purpose of the Paper (§1.4) — DONE. Claims reviewed, reframed (central hypothesis = gap-narrowing benefit; taxonomy = assumed premise), reordered, wording tightened. Citations logged (all unverified). Carry-forward items below.
- [ ] **Hook rewrite (§1.1)** — NEXT. Detailed plan already logged above ("Hook rewrite plan").
- [ ] Then: Literature Review (§2) — all subsections.

### Purpose §1.4 carry-forward (resolve in later sections, NOT reopening Purpose):
- [ ] §4: reconcile "narrow the gap with larger models" (central hypothesis) with evaluation — plan is to compare against PUBLISHED large-model benchmark scores (MMLU/ARC), not run a large model. Claim 9 must reflect this.
- [ ] §4/§5: address "close enough structure suffices" vs ablation's random/wrong scaffold — define the tolerance/robustness band.
- [ ] §4: state that answer-structure labels are assigned offline by the data-generating model (defuses "learnable from question alone" circularity).
- [ ] §2.7/§3: write the CRITICAL load-bearing definition of "answer structure" (see ⚠️ note in Key Conceptual Notes).
- [ ] Global: terminology "answer structure" (not "reasoning structure") — fix title, §1.2 research question, Hook.
- [ ] Citations: all §1.4 cites Unverified; check costofdownscaling2023 fit on core-mechanism claim first.

### Open reminders:
- Hook (§1.1) needs rewrite after Purpose is done — overlaps with Problem Statement, previews solution, has encoder-paper citations for a decoder claim
- Claim 18 (gap claim) — add "to the best of our knowledge" when writing prose
- CoT lit review note is in §2.6 — argument that CoT is iterative context accumulation, not reasoning
