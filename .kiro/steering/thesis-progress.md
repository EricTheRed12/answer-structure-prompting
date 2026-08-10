---
inclusion: auto
---

# Thesis Progress

## Current Status

**Last session:** August 6, 2026 — §3 Architecture fully complete. §3.3 Classifier, §3.4 Scaffold Construction, and §3.5 Generator all written as prose. Key design decisions: scaffold redefined as configurable runtime assembly (schema + question + optional passage, no worked examples); generator produces free-form answers; expanded experimental conditions noted in §4. NOTE left to specify exact BERT variant after experiment.

## Section Status

| Section | Status |
|---------|--------|
| §1.1 Hook | PROSE COMPLETE |
| §1.2 Problem Statement | PROSE COMPLETE |
| §1.3 Purpose of the Paper | PROSE COMPLETE |
| §2.1 Large Language Models | PROSE COMPLETE |
| §2.2 Scale and Structure | PROSE COMPLETE |
| §2.3 Fine-Tuning | PROSE COMPLETE |
| §2.4 Prompt Engineering and ICL | PROSE COMPLETE |
| §2.5 Retrieval-Augmented Generation | PROSE COMPLETE |
| §2.6 Unconstrained Prediction | PROSE COMPLETE |
| §2.7 Question Classification in QA | PROSE COMPLETE |
| §2.8 Answer Structure Types | PROSE COMPLETE |
| §2.9 Related Work | PROSE COMPLETE (citations unverified) |
| §3 Architecture | PROSE COMPLETE (all 5 subsections: Overview, Taxonomy, Classifier, Scaffold Construction, Generator) |
| §4 Methodology | SCAFFOLD (revised — 8 subsections: RQs, Dataset, Taxonomy Derivation, Classifier Training, Scaffold Design, Conditions, Models, Metrics) |
| §5 Results | TBD (after experiments) |
| §6 Discussion | SCAFFOLD (STALE) |
| §7 Limitations | TBD |
| §8 Conclusion | SCAFFOLD |
| Abstract | TBD |

## Key Decisions Made

- §2.5 closer: "a prompt needs to provide everything but the answer" (principle)
- §2.6 framing: model is deterministic; input defines trajectory; hallucination = just prediction; generalization gap = absence of matched structure
- §2.7 scope: classification exists → we propose answer classification → satisfies requirements. Adjacent work moved to §2.9.
- §2.8 definition: answer structure = schema (dimensions, not content); model populates; finiteness hypothesis (bounded by interrogatives)
- Experimental design: SQuAD, 4 conditions (baseline, scaffolded, random scaffold, oracle). No RAG — passage provided. RAG is future work.
- Terminology locked: "answer structure" = the dimensional schema (the contribution); "scaffold" = the prompt artifact that delivers it; "taxonomy" = the classification index
- §3 ordering: Overview → Taxonomy → Classifier → Scaffold Construction → Generator. Taxonomy comes first because it defines what the classifier targets.
- §3 cuts: "Why this works" removed (already argued in §2.6/§2.8). MoE routing analogy removed (comparison, not part of the system).
- §4 methodology: SQuAD extractive QA isolates the structural variable (passage provided eliminates knowledge recall). Open-ended generation noted as possible secondary experiment if time permits.
- §4 evaluation: EM + F1 as primary (SQuAD-standard). Classifier accuracy is a system validity check, not a headline metric.
- §4 fine-tuning scope: base models across all sizes (1B–13B); task-tuned only at 1–3B (LoRA or community fine-tunes). Resource-dependent.
- §3/§4 split: §3 describes taxonomy conceptually (what it is, its role); §4 describes the specific taxonomy derived from SQuAD (which classes, how derived).
- §3 tone: direct, expository, declarative. Not argumentative like the lit review.
- Answer structures are domain-agnostic: defined by form, not content. Same types apply across subject domains.

## Flagged for Future Passes

- Full citation audit (flagged papers in main.tex §2.7/§2.8 NOTE block)
- Terminology consistency pass (form/structure/pattern across paper)
- §2.4 prose rewrite: thread "specificity" and "structure" as terms that §2.5 callbacks to
- Consider merging §1.1 and §1.2 into single flowing Introduction
- §4.3 Taxonomy Derivation: find literature on reasoning types (Bloom's taxonomy, etc.) to ground the taxonomy justification
- §2.8: consider adding one explicit sentence seeding the term "taxonomy" for §3 callback
- No dedicated lit review section needed for taxonomy — §2.7/§2.8 already cover the ground

## Open Decisions

- [ ] §2.8 placement: stays in lit review or moves to §3? (Deferred until all sections complete)
- [ ] §1.3: add explicit Contributions subsection?
- [ ] Gap-vs-larger-models comparison: where does it live? (Purpose vs Methodology vs Discussion)
- [ ] Open-ended generation as secondary experiment: pursue if time/resources allow
