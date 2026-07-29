---
inclusion: auto
---

# Thesis Progress

## Current Status

**Last session:** July 27, 2026 — §2.9 Related Work prose complete. Five papers (SMART, DTS, TemplateRL, Han et al. Blueprints, Constrained Decoding) framed as contributing elements synthesized by our approach. Citations added to sample.bib (all flagged UNVERIFIED).

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
| §3 Architecture | SCAFFOLD (itemize) |
| §4 Methodology | SCAFFOLD (itemize, STALE — still has old 2x2 RAG design) |
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
- Experimental design: SQuAD, 3 conditions (baseline, scaffolded, random scaffold). No RAG — passage provided. RAG is future work.
- Terminology: "answer structure" is the contribution term. Form/structure/pattern need consistency pass later.

## Flagged for Future Passes

- Full citation audit (flagged papers in main.tex §2.7/§2.8 NOTE block)
- Terminology consistency pass (form/structure/pattern across paper)
- §2.4 prose rewrite: thread "specificity" and "structure" as terms that §2.5 callbacks to
- §4 Methodology: currently stale (old 2×2 RAG design). Needs full rewrite for SQuAD 3-condition design.
- Consider merging §1.1 and §1.2 into single flowing Introduction
- §3 should clarify framework is compatible with instruction-tuned models

## Open Decisions

- [ ] §2.8 placement: stays in lit review or moves to §3? (Deferred until all sections complete)
- [ ] §1.3: add explicit Contributions subsection?
- [ ] Gap-vs-larger-models comparison: where does it live? (Purpose vs Methodology vs Discussion)
