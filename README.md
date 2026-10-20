# Answer-Structure Prompting for Small Language Models

Experiment code and data for the MS thesis *Answer-Structure Prompting for Small
Language Models*.

The project asks a single question: **in what form can structure be delivered to a
small language model, and what does the answer reveal about how these models process
information?** We supply a model with an *answer structure* (a schema naming the
dimensions a correct answer must contain, without supplying the answer itself),
matched to the question, and measure whether that improves extractive question
answering on SQuAD.

**Headline result (scoped to extractive QA).** Supplying an empty answer-structure
schema does **not** improve accuracy; in the untuned setting it slightly hurts. What
*does* matter is the delivery *form*: the same structure written as prose beats the
same structure written as a JSON schema. The interpretation the thesis argues is that
small models read language-as-distribution and are sensitive to the surface form that
content arrives in. The result is presented as a negative-with-mechanism, not a claim
about model capability.

See the thesis in [`Masters_Thesis/`](Masters_Thesis/) for the full argument, the
seven research questions (RQ1–RQ7), and all confidence intervals.

> Note on terminology: the repository is organized around *answer structure* (the
> schema the model is given). "Structure" is used in the thesis in three distinct
> senses (the schema, the model's internal representation, and the relational
> structure of prose); the thesis defines these explicitly.

---

## Repository layout

```
.
├── data/                   SQuAD dev set + the fixed 1,000-question eval sample
├── src/                    Shared pipeline: prompt builder, eval harness, helpers
├── taxonomy/               Answer-structure taxonomy: classification + schemas
├── study1_main/            Study 1 — 6 models x 6 conditions (prompt-only, Ollama)
├── study2_finetune/        Study 2 — multi-arm fine-tuning + delivery-form conditions
├── exploratory/            One-off diagnostic probes (run as-is, not maintained)
├── archive/                Superseded checkpoints and throwaway scripts (kept, inert)
└── Masters_Thesis/         LaTeX source for the thesis
```

Paths in all core scripts are resolved relative to the repository root, so run every
command from the root of the repo.

### `data/`
- `squad_dev.json` — SQuAD v2 dev set (public dataset).
- `sample_1000.json` — the fixed, class-stratified 1,000-question evaluation sample
  used across every model and condition.

### `src/` (shared pipeline)
- `scaffold_builder.py` — builds the prompt (the "scaffold") for each condition by
  combining the question, optional passage, and optional answer-structure schema.
- `eval_pipeline.py` — runs questions through a model and computes EM / F1, including
  the extracted-span metrics (EM_ext / F1_ext) the thesis reports.
- `run_condition.py` — production runner for a single model + condition, with
  checkpoint/resume.
- `generate_sample.py` — regenerates the stratified eval sample.
- `generate_labeled_dataset.py` — builds the class-labeled dataset from the taxonomy.
- `inspect_squad.py`, `sample_squad.py` — small dataset inspection helpers.

### `taxonomy/`
- `classify_all.py` — classifies all SQuAD questions by answer-structure features via
  the Anthropic API (reads `ANTHROPIC_API_KEY` from the environment).
- `schemas.json` — the ten answer-structure schemas (one per class).
- `populate_schemas.py`, `restructure_passages.py` — Claude data-build scripts for
  Study 2 (filled schemas and restructured passages).
- `taxonomy_final.md`, `map_to_taxonomy.py`, `aggregate_results.py` — taxonomy
  derivation and reporting.
- `all_results.json` — the committed classification output for all 5,928 answerable
  questions.

### `study1_main/` (Study 1 — prompt-only, 6 models)
Six conditions over six models, 1,000 questions each:

| Condition | Prompt contents |
|-----------|-----------------|
| 1 | question only |
| 2 | question + passage |
| 3 | question + matched answer structure |
| 4 | question + passage + matched answer structure |
| 5 | question + random answer structure (ablation) |
| 6 | question + passage + random answer structure (ablation) |

"Matched" uses the oracle (gold) class for the question. The question classifier was
dropped from the thesis, so conditions 7–8 (classifier-selected structure) exist in
`scaffold_builder.py` but were not run; classification is future work.

- `run_all.sh` — drives every model x condition sequentially.
- `run_base_model.py`, `run_instruct_raw.py`, `run_qwen_fixed.py` — specialized
  runners (raw/base-model mode and a Qwen chat-template fix).
- `analyze_results.py` — matched-vs-random-vs-baseline comparison tables.
- `results/` — the committed per-model, per-condition result files.
- `FINDINGS_SUMMARY.md` — consolidated findings for the Results/Discussion chapters.

### `study2_finetune/` (Study 2 — fine-tuning + delivery form)
Multi-arm LoRA fine-tuning plus the delivery-form conditions (empty prose vs schema,
filled prose, structured passage), each 1,000 questions with bootstrap 95% CIs.
- `answer_structure_finetune.ipynb` — the training/eval notebook (run on Colab, A100).
- `build_finetune_pairs.py` — builds the per-arm train/val pairs.
- `analyze_results.py` — interprets `multiarm_results.json` against RQ1–RQ7 with paired
  bootstrap 95% CIs on F1_ext deltas.
- `multiarm_results.json` — the committed results (includes per-question F1_ext lists).

### `exploratory/`
One-off diagnostic probes (alternate scaffold formats, system-prompt placement, filled
schemas, flat keywords, sentence scaffolds, recompute utilities). These were run
against a local Ollama server during the investigation and are kept **as-run**; they
are not part of the maintained reproduction path.

---

## Setup

```bash
pip install -r requirements.txt
```

Study 1 and the exploratory probes talk to a locally running
[Ollama](https://ollama.com) server (default `http://localhost:11434`) and expect the
relevant models to be pulled, e.g.:

```bash
ollama pull llama3.2:1b gemma2:2b llama3.2:3b phi3:mini llama3:8b qwen3:8b
```

The taxonomy classifier and the Claude data-build scripts call the Anthropic API. Set
your key in the environment (never commit it):

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Study 2 (fine-tuning) was run on Google Colab (A100). See the notebook header for the
exact runtime; it is not installed by `requirements.txt`.

---

## Reproducing the analyses

The committed result files let you reproduce every reported number without re-running
the models:

```bash
# Study 2: RQ1–RQ7 deltas with bootstrap 95% CIs (and SEMs)
python3 study2_finetune/analyze_results.py

# Study 1: matched vs random vs baseline tables
python3 study1_main/analyze_results.py
```

To re-run the experiments from scratch (requires Ollama + the Anthropic API):

```bash
# 1. Classify questions by answer-structure features (Anthropic API)
python3 taxonomy/classify_all.py

# 2. Regenerate the fixed evaluation sample
python3 src/generate_sample.py --size 1000

# 3. Run the full main study (long-running; resumable via checkpoints)
bash study1_main/run_all.sh

# 4. Build the fine-tuning data, then train/evaluate in the Colab notebook
python3 study2_finetune/build_finetune_pairs.py
#   -> study2_finetune/answer_structure_finetune.ipynb
```

---

## Data provenance and reproducibility notes

- The main study (Study 1) was run through Ollama on quantized instruction-tuned
  models; Study 2 was run on a single Hugging Face base model in bf16 on Colab. These
  are **separate measurement environments**: compare deltas and directions across the
  two studies, not absolute values.
- All reported estimates use F1_ext (F1 on the best extracted span), n = 1000, with
  bootstrap 95% confidence intervals. Per-question F1_ext lists are saved in the result
  files so every estimate carries an interval.
- No API keys or secrets are stored in this repository or its history.

## License

See [`LICENSE`](LICENSE).
