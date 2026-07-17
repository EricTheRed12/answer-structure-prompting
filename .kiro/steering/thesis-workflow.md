---
inclusion: auto
---

# Thesis Workflow

## Process for Working on a Section

Follow this sequence for each subsection of the lit review (and other sections when writing):

### Phase 1: Structure Review
1. Read the existing claims in the section
2. Assess: does the ordering make logical sense?
3. Assess: is anything missing that the paper's argument depends on?
4. Assess: is anything present that doesn't earn its place (relevance filter)?
5. Propose structural changes (reorder, add, remove) and confirm with author

### Phase 2: Claim Review
6. Go claim by claim — review wording, accuracy, and framing
7. For each claim, check: does it connect forward to the paper's argument?
8. Expand or trim sub-points based on relevance filter
9. Iterate with author until each claim feels right

### Phase 3: Citation Review
10. For each finalized claim, review the associated citations:
    - Does the citation actually support what the claim says?
    - Is it peer-reviewed? How well-cited?
    - Are we relying on it because it was already in the bib, or is it the best fit?
    - Are there better papers we should find?
11. Search for additional/replacement papers where needed
12. Add new citations to `sample.bib` (flagged as unreviewed)
13. Log all citations in the Citation Verification Tracker (`thesis-citations.md`)

### Phase 4: Context Check
14. Review the finished section against the Problem Statement and Purpose:
    - Does it support claims made in §1.2/§1.4?
    - Does it contradict anything stated elsewhere?
    - Does it introduce terminology or framing inconsistent with the rest of the paper?
15. Check against adjacent sections for overlap or gaps

### Phase 5: Write to File
16. Write the finalized claims into `main.tex`
17. Update `thesis-progress.md` with what was done

## Key Principles

- Work section by section, not all at once
- Claims first, citations second — get the argument right before worrying about sources
- Every claim earns its place by connecting to the paper's argument
- Author has final say on all framing decisions
- Flag uncertainties rather than assuming
- When a claim needs a citation we don't have yet, mark with `\needpaper{}`
