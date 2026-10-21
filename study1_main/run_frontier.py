"""
Run the six-condition study against a frontier (foundation) model, zero-shot,
via the Anthropic API.

This is the frontier-scale probe requested at the defense: run the same six
conditions used in the six-model study against a large foundation model to see
whether scale changes the schema outcome. It reuses the exact scaffold builder
and scoring functions from the Ollama runner (src/run_condition.py), swapping
only the inference call for the Anthropic API, so the output files are drop-in
comparable with the rest of study1_main/results/.

Scope note (do not drop this framing when reporting): a positive result at
frontier scale would NOT falsify the scoped thesis. It would be consistent with
"larger models can read more forms." The thesis claim is bounded to small models.

Setup:
  pip install anthropic
  export ANTHROPIC_API_KEY="sk-ant-..."

Run (from the repository root):
  python3 study1_main/run_frontier.py --list-models            # confirm your Opus id first
  python3 study1_main/run_frontier.py --model claude-opus-5-5 --limit 100
  python3 study1_main/run_frontier.py --model claude-opus-5-5 --limit 100 --conditions 1 2 3

Output:
  study1_main/results/<model>_<condition>.json   (same schema as run_condition.py)
  Checkpoints every --save-every questions; resumes automatically on re-run.
"""

import argparse
import json
import sys
import time
from pathlib import Path

import anthropic

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

# Reuse the exact scaffold construction and scoring used everywhere else.
from scaffold_builder import build_scaffold, condition_name  # noqa: E402
from run_condition import (  # noqa: E402
    exact_match,
    exact_match_extracted,
    f1_score,
    best_span_extraction,
    normalize_answer,
    _token_f1,
    compute_aggregates,
)

STUDY_DIR = Path(__file__).parent
RESULTS_DIR = STUDY_DIR / "results"
CHECKPOINTS_DIR = STUDY_DIR / "checkpoints"
SAMPLE_PATH = PROJECT_ROOT / "data" / "sample_1000.json"

DEFAULT_MODEL = "claude-opus-5-5"  # override with --model to match your account's Opus ID
MAX_TOKENS = 512
TEMPERATURE = 0.0  # deterministic, matching the Ollama runs


def model_tag(model: str) -> str:
    """Filesystem-safe tag for a model id."""
    return model.replace(":", "_").replace("/", "_").replace(".", "-")


def checkpoint_path(model: str, condition: int) -> Path:
    return CHECKPOINTS_DIR / f"{model_tag(model)}_{condition_name(condition)}_checkpoint.json"


def load_checkpoint(model: str, condition: int) -> list:
    path = checkpoint_path(model, condition)
    if path.exists():
        with open(path) as f:
            return json.load(f).get("results", [])
    return []


def save_checkpoint(model: str, condition: int, results: list):
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(checkpoint_path(model, condition), "w") as f:
        json.dump({"model": model, "condition": condition, "results": results}, f)


# Some newer models (e.g. Opus 5.x) reject the `temperature` parameter outright.
# We try to pin temperature=0 for determinism, matching the Ollama runs, and fall
# back to omitting it when the model does not accept it. This flips to True the
# first time a model rejects temperature, so we only pay the failed call once.
_OMIT_TEMPERATURE = False


def query_anthropic(client, prompt: str, model: str) -> str:
    """Send the scaffold prompt to the Anthropic API and return the response text.

    The scaffold IS the prompt, exactly as in the Ollama runs: no extra system
    instruction is added, so the zero-shot condition matches the six-model study.
    """
    global _OMIT_TEMPERATURE
    kwargs = {
        "model": model,
        "max_tokens": MAX_TOKENS,
        "messages": [{"role": "user", "content": prompt}],
    }
    if not _OMIT_TEMPERATURE:
        kwargs["temperature"] = TEMPERATURE
    try:
        resp = client.messages.create(**kwargs)
    except anthropic.BadRequestError as e:
        if not _OMIT_TEMPERATURE and "temperature" in str(e).lower():
            # This model does not accept temperature; drop it and retry once.
            _OMIT_TEMPERATURE = True
            kwargs.pop("temperature", None)
            print("  note: this model rejects `temperature`; retrying without it "
                  "(model default sampling used for all subsequent calls).")
            resp = client.messages.create(**kwargs)
        else:
            raise
    parts = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
    return "".join(parts).strip()


def run_condition(client, model: str, condition: int, questions: list, save_every: int):
    cond_label = condition_name(condition)
    output_path = RESULTS_DIR / f"{model_tag(model)}_{cond_label}.json"
    if output_path.exists():
        print(f"SKIPPED: {output_path.name} already exists")
        return

    existing = load_checkpoint(model, condition)
    sample_ids = {q["id"] for q in questions}
    existing = [r for r in existing if r["id"] in sample_ids]
    done_ids = {r["id"] for r in existing}
    remaining = [q for q in questions if q["id"] not in done_ids]

    print(f"\n{'='*60}")
    print(f"Model: {model} | Condition {condition}: {cond_label}")
    print(f"Remaining: {len(remaining)}/{len(questions)}"
          + (f" (resumed {len(existing)})" if existing else ""))
    print(f"{'='*60}")

    results = existing.copy()
    for i, item in enumerate(remaining):
        scaffold = build_scaffold(
            question=item["question"],
            condition=condition,
            passage=item["passage"] if condition in (2, 4, 6, 8) else None,
            class_id=item["class_id"] if condition >= 3 else None,
            random_seed=(42 + questions.index(item)) if condition in (5, 6) else None,
        )

        t0 = time.time()
        try:
            prediction = query_anthropic(client, scaffold, model)
        except anthropic.APIError as e:
            print(f"  API error on {item['id']}: {e}. Saving checkpoint and stopping.")
            save_checkpoint(model, condition, results)
            raise
        latency = time.time() - t0

        gold = item["gold_answers"]
        extracted = best_span_extraction(prediction, gold)
        f1_ext = max(
            (_token_f1(extracted.split(), normalize_answer(g).split()) for g in gold),
            default=0.0,
        )
        results.append({
            "id": item["id"],
            "question": item["question"],
            "gold_answers": gold,
            "prediction": prediction,
            "class_id": item["class_id"],
            "exact_match": exact_match(prediction, gold),
            "exact_match_extracted": exact_match_extracted(prediction, gold),
            "f1": f1_score(prediction, gold),
            "f1_extracted": f1_ext,
            "prediction_tokens": len(prediction.split()),
            "latency_s": round(latency, 2),
        })

        done = len(results)
        if done % 10 == 0 or (i + 1) == len(remaining):
            avg_f1 = sum(r["f1_extracted"] for r in results) / done
            avg_em = sum(r["exact_match_extracted"] for r in results) / done
            print(f"  [{done}/{len(questions)}] F1_ext={avg_f1:.3f} EM_ext={avg_em:.3f}")
        if done % save_every == 0:
            save_checkpoint(model, condition, results)

    save_checkpoint(model, condition, results)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    aggregates = compute_aggregates(results)
    with open(output_path, "w") as f:
        json.dump({
            "model": model,
            "condition": condition,
            "condition_name": cond_label,
            "sample_size": len(questions),
            "aggregates": aggregates,
            "results": results,
        }, f, indent=2)

    print(f"DONE: {output_path.name}  "
          f"F1_ext={aggregates['f1_extracted']:.4f}  EM_ext={aggregates['em_extracted']:.4f}")
    cp = checkpoint_path(model, condition)
    if cp.exists():
        cp.unlink()


def main():
    ap = argparse.ArgumentParser(description="Frontier-model zero-shot six-condition run")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help="Anthropic model id (set to the Opus id your key can access)")
    ap.add_argument("--limit", type=int, default=100,
                    help="Number of questions from the sample (default 100)")
    ap.add_argument("--conditions", type=int, nargs="+", default=[1, 2, 3, 4, 5, 6],
                    help="Conditions to run (default 1-6)")
    ap.add_argument("--save-every", type=int, default=10,
                    help="Checkpoint every N questions (default 10)")
    ap.add_argument("--list-models", action="store_true",
                    help="List model ids available to this API key and exit (no run)")
    args = ap.parse_args()

    if args.list_models:
        client = anthropic.Anthropic()
        print("Models available to this API key:")
        for m in client.models.list(limit=100).data:
            print(f"  {m.id}")
        return

    with open(SAMPLE_PATH) as f:
        questions = json.load(f)["questions"]
    if args.limit:
        questions = questions[:args.limit]

    print(f"Frontier run: model={args.model}  n={len(questions)}  conditions={args.conditions}")
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

    for condition in args.conditions:
        run_condition(client, args.model, condition, questions, args.save_every)

    print("\nAll requested conditions complete.")


if __name__ == "__main__":
    main()
