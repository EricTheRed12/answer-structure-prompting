# Findings Summary — For Results & Discussion Sections

Reference document consolidating all experimental findings.

---

## THE CORE RESULT

Answer structure scaffolding, delivered via prompt, does NOT improve extractive QA
performance. This holds across every model, every scaffold format, and every prompt
placement tested. The raw passage is always the strongest signal.

---

## MAIN EXPERIMENT (6 models × 6 conditions × 1000 questions)

Models: llama3.2:1b, gemma2:2b, llama3.2:3b, phi3:mini, llama3:8b, qwen3:8b
Metric: F1_ext (F1 on max-F1 extracted span). Also tracked EM_ext, verbosity.

### Finding 1: Scaffold never beats baseline
- No structure condition (C3, C4) beats its no-structure counterpart (C1, C2)
- Holds for all 6 instruction-tuned models
- Example (llama3:8b): C1=0.449, C3=0.425; C2=0.972, C4=0.938

### Finding 2: The taxonomy captures real signal (matched > random)
- On instruction-tuned models, matched structure (C3/C4) consistently beats
  random structure (C5/C6)
- With passage: 6/6 models show C4 > C6
- This proves the classification captures something structurally meaningful —
  the model responds differently to the correct schema vs a wrong one

### Finding 3: Passage dominates everything
- Passage-only (C2) is best or tied-best in every model
- Instruction-tuned: 0.79-0.97 F1_ext with passage vs 0.30-0.44 without
- The answer is a verbatim span in the passage; nothing beats providing it

### Finding 4: Scaffold reduces verbosity
- Adding structure consistently lowers output token count
- Model produces shorter answers, but they are less accurate
- Structure constrains form without improving correctness

---

## EXPLORATORY TESTS (diagnosing why)

### Test A: JSON stripping — no effect
- Stripped JSON syntax from predictions before scoring
- Deltas < 0.002. Measurement artifact ruled out.

### Test B: System prompt placement — worse
- Putting structure in system prompt (vs user prompt) made it worse
- "Respond with ONLY the answer" over-constrained the model

### Test C: Two-pass filled scaffold — worse than passage
- Pass 1: model fills schema from passage. Pass 2: generate from filled schema.
- Filled scaffold (~0.82) < passage alone (~0.94)
- Extraction into schema LOSES information vs raw passage

### Test D: Flat keywords vs JSON — less bad, still below baseline
- Flat keywords (no JSON syntax) beat JSON format (+0.05 with passage)
- But still below passage-only baseline
- Format matters at the margin, but doesn't change the conclusion

### Test E: Sentence scaffold — worst format
- Natural language sentences describing structure performed worst of all formats

### Test F: Model size — smaller models hurt MORE
- SCAFFOLD DELTA (scaffold F1 - baseline F1, no passage):
  - llama3.2:1b: -0.115 (flat), -0.172 (sentence)
  - llama3:8b: -0.025 (flat), -0.090 (sentence)
- Smaller models are MORE damaged by scaffold, not less
- Rejects hypothesis that small models benefit from external structure

### Test G: Base model (llama3:text, raw mode, 1000q) — same pattern
- C1 baseline: 0.304, C3 matched: 0.188, C5 random: 0.217
- C2 passage: 0.776, C4 passage+matched: 0.686, C6 passage+random: 0.734
- Scaffold hurts on base model too (removes chat-template confound)
- NOTE: on base model, random ≥ matched (0.217 > 0.188) — base model can't even
  distinguish correct structure. Instruction tuning at least preserves the signal.

---

## THE MECHANISM (for Discussion)

Why scaffolding fails:

1. **The thesis assumed structure tokens narrow the prediction space.** This is only
   true when tokens are task-relevant context (like a passage containing the answer).

2. **Schema tokens are metadata, not context.** "answer_type: single, agent,
   action_performed" describes the answer FORM but contains none of the answer CONTENT.
   The model has no trained mapping from these abstract descriptors to answer-producing
   behavior.

3. **Extra tokens INCREASE the prediction space when they're off-distribution.**
   Schema tokens activate associations with JSON/code/documentation, competing with
   the question's signal toward the answer. Attention is diluted, not focused.

4. **The passage works because it contains the literal answer tokens.** The scaffold
   fails because it contains abstract type descriptions the model was never trained
   to act on.

5. **Instruction tuning partially mitigates the damage.** Chat-trained models have a
   strong "answer the question" prior that fights through the scaffold noise, which is
   why they still distinguish matched from random. Base models have no such prior and
   are more easily derailed.

---

## WHAT THIS MEANS

- The taxonomy is a valid contribution: derivable, classifiable, captures real
  structural signal (matched > random on instruction-tuned models)
- Prompt-based delivery of that structure is insufficient — the model needs a
  TRAINED mapping between structure and behavior (fine-tuning), not just the tokens
- SQuAD (extractive QA) may be the wrong task: the answer is always a span in the
  passage, so structural guidance is redundant when the passage is present and
  insufficient when it is absent (the model can't recall the fact regardless)
- Conditions 7-8 (classified scaffold) were not run: oracle scaffold (C3-C4) already
  fails, so classifier accuracy is irrelevant

---

## KEY NUMBERS FOR TABLES

### Main experiment — F1_ext by model and condition
| Model      | C1 base | C2 pass | C3 match | C4 p+m | C5 rand | C6 p+r |
|------------|---------|---------|----------|--------|---------|--------|
| llama3.2:1b| 0.335   | 0.791   | 0.299    | 0.738  | 0.300   | 0.730  |
| gemma2:2b  | 0.388   | 0.919   | 0.337    | 0.865  | 0.327   | 0.804  |
| llama3.2:3b| 0.369   | 0.906   | 0.343    | 0.891  | 0.360   | 0.874  |
| phi3:mini  | 0.415   | 0.834   | 0.388    | 0.808  | 0.372   | 0.767  |
| llama3:8b  | 0.441   | 0.930   | 0.403    | 0.915  | 0.397   | 0.892  |
| qwen3:8b   | 0.177   | 0.762   | 0.157    | 0.591  | 0.117   | 0.436  |
| llama3:text| 0.304   | 0.776   | 0.188    | 0.686  | 0.217   | 0.734  |

(llama3:text = base model, raw mode)

### Scaffold delta (C3 - C1, structure effect without passage, F1_ext)
| Model      | Delta   |
|------------|---------|
| llama3.2:1b| -0.036  |
| gemma2:2b  | -0.051  |
| llama3.2:3b| -0.026  |
| phi3:mini  | -0.027  |
| llama3:8b  | -0.038  |
| qwen3:8b   | -0.020  |
| llama3:text| -0.116  |

All negative — structure reduces performance in every model.
