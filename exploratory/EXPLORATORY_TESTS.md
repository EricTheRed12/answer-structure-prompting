# Exploratory Tests — Scaffold Format Investigation

After the main 1000-question experiment showed structure hurting performance,
we're testing WHY and whether alternative delivery mechanisms change the outcome.

---

## Main Finding (from full experiment)
- Matched structure > random structure (consistent across all models)
- But ALL scaffold conditions < baseline (structure hurts absolute performance)
- Root cause hypothesis: models treat JSON scaffold as input to respond to, not guidance to follow

---

## Exploratory Tests

### 1. JSON Stripping (`recompute_stripped.py`)
- **Question:** Is the extraction algorithm confused by JSON tokens in the response?
- **Result:** No effect (deltas < 0.002). Measurement isn't the issue.
- **Status:** COMPLETE

### 2. System Prompt Placement (`test_system_prompt_scaffold.py`)
- **Question:** Does putting structure in system prompt (instructions) vs user prompt help?
- **Conditions:** baseline, passage, user_scaffold, system_scaffold, system_scaffold+passage
- **Result (partial, 30q):** System prompt WORSE (0.233) than baseline (0.429). "Respond with ONLY the answer" is too constraining.
- **Status:** KILLED at 30/200

### 3. Filled Scaffold — Two-Pass (`test_filled_scaffold.py`)
- **Question:** If we extract passage info INTO the schema first, is that a better context than raw passage?
- **Pipeline:** Pass 1: fill schema from passage. Pass 2: generate from filled schema (no passage).
- **Result (partial, 130q):** filled=0.824 < passage=0.895. Extraction loses information.
- **Status:** KILLED at 130/200

### 4. Filled Schema + System Prompt (`test_filled_system_scaffold.py`)
- **Question:** Combine: extract into schema, then put filled schema in system prompt.
- **Result (partial, 30q):** filled_as_system=0.849 < passage=0.939. Same pattern.
- **Status:** KILLED at 30/50

### 5. Flat Keywords — No JSON (`test_flat_scaffold.py`)
- **Question:** Do plain keywords (field names without JSON syntax) work better?
- **Conditions:** baseline, passage, json_scaffold, flat, flat+passage, flat_system, flat_system+passage
- **Result (50q, llama3:8b):**
  - passage_only=0.937, flat+passage=0.918, json+passage=0.870, baseline=0.593, flat=0.580
  - Flat format IS better than JSON format (+0.048 with passage)
  - But still below passage alone
  - Flat without passage does NOT beat baseline (initial 10q lead was noise)
- **Status:** COMPLETE

### 6. Sentence Scaffold + Smaller/Base Models (`test_sentence_and_base.py`)
- **Question:** Do standardized sentences work? Does scaffold help MORE on smaller (1B) or base (non-instruct) models?
- **Models:** llama3.2:1b (small instruct), llama3:8b (large instruct), llama3:text (8B base, raw mode)
- **Conditions:** baseline, passage, flat, flat+passage, sentence, sentence+passage
- **Result (50q):**
  - SCAFFOLD DELTA (no passage, scaffold F1 - baseline F1):
    - llama3.2:1b: flat=-0.115, sentence=-0.172 (structure HURTS more on smaller models)
    - llama3:8b: flat=-0.025, sentence=-0.090 (structure hurts)
    - llama3:text (base): flat=+0.003, sentence=+0.004 (NEUTRAL — only model where scaffold doesn't hurt)
  - Passage still best in all models: 1b=0.812, 8b=0.972, base=0.702
  - Sentence format worst of all scaffold formats
  - Base model (raw mode) is only model where scaffold is not harmful
- **Status:** COMPLETE

---

## Conclusions from Exploratory Testing

1. **Format hypothesis:** Partially confirmed — flat keywords less harmful than JSON, but still don't beat baseline
2. **Placement hypothesis:** REJECTED — system prompt makes it worse (too constraining)
3. **Two-pass hypothesis:** REJECTED — extraction loses information vs raw passage
4. **Model size hypothesis:** REJECTED — smaller models are MORE confused by scaffold, not less
5. **Instruction tuning hypothesis:** CONFIRMED — base model (no chat training) is the only model where scaffold is neutral/slightly positive. Chat template/RLHF training creates a prior that scaffolding fights against.

## Final Summary

- **Nothing beats passage alone for extractive QA on instruction-tuned models**
- The taxonomy captures real structural signal (matched > random consistently in main experiment)
- But prompt-based delivery of that structure hurts performance in all tested formats
- Root cause: instruction-tuned models already have implicit answer-type knowledge; adding structure is redundant at best and confusing at worst
- The base model result suggests fine-tuning (training the model TO USE structure) is the viable path
- SQuAD may be the wrong benchmark — extractive QA doesn't require answer construction

---

## Scripts

| Script | Status | ~Time |
|--------|--------|-------|
| `recompute_stripped.py` | DONE | instant |
| `test_system_prompt_scaffold.py` | partial (30/200) | ~80min full |
| `test_filled_scaffold.py` | partial (130/200) | ~50min full |
| `test_filled_system_scaffold.py` | partial (30/50) | ~25min full |
| `test_flat_scaffold.py` | DONE | ~30min |
| `test_sentence_and_base.py` | DONE | ~60min |
| `test_alt_scaffolds.py` | abandoned | — |
| `test_alt_scaffolds_quick.py` | abandoned | — |
