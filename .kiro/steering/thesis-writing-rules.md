---
inclusion: auto
---

# Thesis Writing Rules

## Format

- All thesis sections should be written as **bullet-point claims** — each claim is an independent bullet written in prose (a complete, well-formed sentence or short paragraph).
- Each bullet point represents a single claim that will become one paragraph in the final draft.
- Do not write out multi-paragraph flowing sections unless explicitly asked. Each claim stands alone.

## Citations

- Every claim that is not the author's own contribution must have an associated citation.
- **Multiple citations per claim are encouraged** when different papers support the same claim from different angles (e.g., one for the mechanism, one for the outcome).
- **All suggested citations must be reviewed before being considered final.** Mark unverified citations clearly.
- When uncertain about whether a citation supports a claim, flag it for manual review rather than assuming it fits.
- **All unverified citations must be flagged with a confidence rating (HIGH / MEDIUM / LOW)** in the Citation Verification Tracker (see `thesis-citations.md`).
  - **HIGH** — Title/abstract directly states the claim; venue is strong; very unlikely to be wrong
  - **MEDIUM** — Abstract supports inference but specific claim not confirmed in full text; could be slightly off-target
  - **LOW** — Speculative match based on topic area; needs full read before relying on it

## Section Review Workflow

Before reviewing or drafting claims for any section:
1. **Discuss the section's purpose first.** What is this section's ONE job in the paper's argument? What does it set up? What does it connect to?
2. Only after the purpose is agreed, proceed to reviewing/writing claims.
3. **After completing work on a section** (claims finalized, citations first-passed, context-checked), update `thesis-progress.md` and `thesis-concepts.md` to reflect the current state.

This prevents scope drift and ensures every claim serves the section's argumentative function.

## Style

- Do not use em-dashes (—) as pauses in claim text. They are not academic. Use "because," semicolons, or restructure the sentence instead.
- Write claims as direct, single-idea sentences suitable for academic prose.

## Relevance Filter

- Every claim and sub-point in the lit review must **earn its place** by connecting forward to the paper's argument.
- If a sub-point is textbook knowledge that the committee knows implicitly and doesn't advance the thesis argument, cut it.
- The test: "does this sub-point get referenced or built upon later in the paper?"

## Scope Control

- Each subsection has ONE job. Do not let claims from one section bleed into another.
- If a claim appears in the Problem Statement (§1.2), it does not need to be restated in the lit review — the lit review provides the *evidence* that supports those claims.
- Avoid "said three times" syndrome: a point should live in exactly one place and be referenced from others, not restated.

## Hedging Language

- **Author's own contributions/hypotheses:** state confidently — "we propose," "we hypothesize," "this paper introduces"
- **Reporting cited work:** attribute clearly — "X et al. find that," "according to [cite]," "Y demonstrates that"
- **Author's inferences drawn from others' work:** hedge appropriately — "this suggests," "taken together, these findings imply," "we argue that"
- **Contested or debated claims:** flag the debate — "the mechanism is debated [cite]," "proposed causes include... [cite]"
- Never state another researcher's finding as if it were universal fact without attribution

## Claim Attribution — Whose Voice Is This?

Every claim falls into one of three categories. Make it clear which:

1. **Reporting literature:** summarizing what others have found (requires citation)
2. **Author's interpretation:** synthesizing or reframing multiple findings into a new argument (underlying findings cited, the synthesis itself is uncited — it's your contribution)
3. **Author's novel contribution:** the framework, hypothesis, or mechanism you are proposing (no citation needed; state with confidence)

The committee wants to see you clearly distinguish between summarizing others and contributing your own ideas. When in doubt, make the attribution explicit.

## Forward References to the Framework

- The lit review sections should NOT use "this paper aims to" or "Connection to this paper" framing.
- Each section's final claim can state the mechanism or gap factually, but the framing of "our contribution" belongs entirely in §3 (Architecture) and §4 (Methodology).
- The lit review earns the framework's place by establishing facts, mechanisms, and gaps. It does not sell the framework — the architecture section does that.
- Cross-references to §3 are fine ("see §3"), but do not describe the framework in detail within the lit review.

## Counter-Arguments and Limitations

- When reviewing a technique or approach, state BOTH its contribution AND its limitation as it relates to your gap.
- This is what makes a lit review argumentative rather than a summary.
- Pattern: "[Technique] achieves X [cite]. However, it does not address Y — [explain why Y matters for our problem]."
- Do not dismiss prior work — acknowledge what it does well, then identify what it leaves unresolved.

## Footnotes vs. Inline

- Use footnotes for: epistemic caveats, scope limitations, or asides that would break the argument's flow
- Use inline text for: claims that are part of the logical chain of the argument
- Test: if removing the footnote would leave the argument incomplete, it should be inline. If the argument stands without it but benefits from the nuance, it's a footnote.

## Forward and Cross-References

- When a claim depends on detail provided in a later section, add an explicit forward reference: "(see §3)" or "(detailed in §4.2)"
- When a lit review claim provides evidence for something asserted in the introduction, do NOT re-state the introduction's claim — the structural position (lit review after intro) implies the connection
- Use forward references sparingly — they are a signal that the reader needs reassurance, not a default

## What Counts as "Author's Own Contribution" (No Citation Needed)

- Novel interpretations that synthesize multiple cited findings into a new framing are the author's contribution — no citation needed for the synthesis itself
- BUT: the underlying findings being synthesized must each be individually cited
- The framework, hypothesis, taxonomy, and mechanism proposed in this paper are all author contributions
- If a claim could be read as "someone else showed this," it needs a citation. If it could only be read as "the author is arguing this," it doesn't.
