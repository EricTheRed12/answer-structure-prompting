"""
Run conditions 1-6 on the base model (llama3:text) using raw mode.

Raw mode skips the chat template entirely — no system prompt injection,
no <|start_header_id|> wrapping. The model sees exactly the tokens we send.

Prompts are formatted as completion-style:
  "Q: {question}\nA:" (baseline)
  "Context: {passage}\n\nQ: {question}\nA:" (with passage)
  "{schema}\n\nQ: {question}\nA:" (with structure)

Uses the same 1000-question stratified sample as the main experiment.
Checkpoint/resume every 25 questions.

Usage (run from the repository root):
  caffeinate -i python3 study1_main/run_base_model.py
"""

import json
import re
import string
import time
from collections import defaultdict
from pathlib import Path

import requests

import sys
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from scaffold_builder import get_answer_structure, get_random_class_id, condition_name
from eval_pipeline import normalize_answer, _token_f1, best_span_extraction

MODEL = "llama3:text"
BASE_URL = "http://localhost:11434"
STUDY_DIR = Path(__file__).parent
RESULTS_DIR = STUDY_DIR / "results"
CHECKPOINTS_DIR = STUDY_DIR / "checkpoints"
SAMPLE_PATH = PROJECT_ROOT / "data" / "sample_1000.json"
SAVE_EVERY = 25
SEED = 42


# ============================================================
# INFERENCE
# ============================================================


def query_ollama(prompt: str, max_tokens: int = 64) -> str:
    """Send prompt in raw mode — no chat template."""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "raw": True,
        "stream": False,
        "options": {"temperature": 0, "num_predict": max_tokens},
    }
    try:
        resp = requests.post(f"{BASE_URL}/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        response = resp.json().get("response", "").strip()
        # Take only first line (base models tend to keep generating)
        first_line = response.split("\n")[0].strip()
        return first_line
    except requests.exceptions.Timeout:
        return ""
    except Exception as e:
        print(f"  ERROR: {e}")
        return ""


# ============================================================
# METRICS
# ============================================================


def exact_match_extracted(prediction: str, gold_answers: list) -> float:
    extracted = best_span_extraction(prediction, gold_answers)
    for gold in gold_answers:
        if extracted == normalize_answer(gold):
            return 1.0
    return 0.0


def f1_ext(prediction: str, gold_answers: list) -> float:
    extracted = best_span_extraction(prediction, gold_answers)
    best = 0.0
    for gold in gold_answers:
        f1 = _token_f1(extracted.split(), normalize_answer(gold).split())
        best = max(best, f1)
    return best


# ============================================================
# PROMPT BUILDERS (completion-style for base model)
# ============================================================


def build_prompt(question: str, condition: int, passage: str = None,
                 class_id: int = None, random_seed: int = None) -> str:
    """
    Build a completion-style prompt for the base model.

    Conditions:
      1: Q: {question}\nA:
      2: Context: {passage}\n\nQ: {question}\nA:
      3: {schema}\n\nQ: {question}\nA:
      4: {schema}\n\nContext: {passage}\n\nQ: {question}\nA:
      5: {random_schema}\n\nQ: {question}\nA:
      6: {random_schema}\n\nContext: {passage}\n\nQ: {question}\nA:
    """
    import random

    schema_str = ""
    if condition in (3, 4):
        schema = get_answer_structure(class_id)
        schema_str = json.dumps(schema)
    elif condition in (5, 6):
        if random_seed is not None:
            random.seed(random_seed)
        wrong_id = get_random_class_id(exclude_id=class_id)
        schema = get_answer_structure(wrong_id)
        schema_str = json.dumps(schema)

    parts = []

    # Add schema if applicable
    if condition in (3, 4, 5, 6):
        parts.append(f"Answer structure: {schema_str}")
        parts.append("")

    # Add passage if applicable
    if condition in (2, 4, 6):
        parts.append(f"Context: {passage}")
        parts.append("")

    # Always end with Q/A format
    parts.append(f"Q: {question}")
    parts.append("A:")

    return "\n".join(parts)


# ============================================================
# CHECKPOINT
# ============================================================


def checkpoint_path(condition: int) -> Path:
    cond_label = condition_name(condition)
    return CHECKPOINTS_DIR / f"llama3_text_{cond_label}_checkpoint.json"


def load_checkpoint(condition: int) -> list:
    path = checkpoint_path(condition)
    if path.exists():
        with open(path) as f:
            return json.load(f).get("results", [])
    return []


def save_checkpoint(condition: int, results: list):
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    path = checkpoint_path(condition)
    with open(path, "w") as f:
        json.dump({"model": MODEL, "condition": condition, "results": results}, f)


# ============================================================
# AGGREGATES
# ============================================================


def compute_aggregates(results: list) -> dict:
    if not results:
        return {}
    n = len(results)
    by_class = defaultdict(list)
    for r in results:
        by_class[str(r["class_id"])].append(r)

    class_metrics = {}
    for cid, cr in sorted(by_class.items()):
        cn = len(cr)
        class_metrics[cid] = {
            "n": cn,
            "em_ext": round(sum(r["exact_match_extracted"] for r in cr) / cn, 4),
            "f1_ext": round(sum(r["f1_extracted"] for r in cr) / cn, 4),
            "avg_tokens": round(sum(r["prediction_tokens"] for r in cr) / cn, 1),
        }

    return {
        "n": n,
        "em_ext": round(sum(r["exact_match_extracted"] for r in results) / n, 4),
        "f1_ext": round(sum(r["f1_extracted"] for r in results) / n, 4),
        "avg_prediction_tokens": round(sum(r["prediction_tokens"] for r in results) / n, 1),
        "by_class": class_metrics,
    }


# ============================================================
# MAIN
# ============================================================


def run_condition(condition: int, questions: list):
    """Run one condition with checkpoint/resume."""
    cond_label = condition_name(condition)

    # Check if already complete
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / f"llama3_text_{cond_label}.json"
    if output_path.exists():
        print(f"SKIPPED: {output_path.name} already exists")
        return

    # Load checkpoint
    existing = load_checkpoint(condition)
    sample_ids = {q["id"] for q in questions}
    existing = [r for r in existing if r["id"] in sample_ids]
    completed_ids = {r["id"] for r in existing}

    if existing:
        print(f"  Resuming from checkpoint: {len(existing)} already done")

    remaining = [q for q in questions if q["id"] not in completed_ids]

    print(f"\n{'='*60}")
    print(f"Model: {MODEL} (raw mode)")
    print(f"Condition {condition}: {cond_label}")
    print(f"Remaining: {len(remaining)}/{len(questions)}")
    print(f"{'='*60}")

    if not remaining:
        print("All done!")
        results = existing
    else:
        results = existing.copy()

        for i, item in enumerate(remaining):
            prompt = build_prompt(
                question=item["question"],
                condition=condition,
                passage=item["passage"] if condition in (2, 4, 6) else None,
                class_id=item["class_id"] if condition >= 3 else None,
                random_seed=SEED + questions.index(item) if condition in (5, 6) else None,
            )

            t0 = time.time()
            prediction = query_ollama(prompt)
            latency = time.time() - t0

            em = exact_match_extracted(prediction, item["gold_answers"])
            f1 = f1_ext(prediction, item["gold_answers"])
            tokens = len(prediction.split())

            results.append({
                "id": item["id"],
                "question": item["question"],
                "gold_answers": item["gold_answers"],
                "prediction": prediction,
                "class_id": item["class_id"],
                "exact_match_extracted": em,
                "f1_extracted": f1,
                "prediction_tokens": tokens,
                "latency_s": round(latency, 2),
            })

            done = len(results)
            if done % 10 == 0 or (i + 1) == len(remaining):
                avg_em = sum(r["exact_match_extracted"] for r in results) / done
                avg_f1 = sum(r["f1_extracted"] for r in results) / done
                avg_tok = sum(r["prediction_tokens"] for r in results) / done
                print(f"  [{done}/{len(questions)}] EM_ext={avg_em:.3f} F1_ext={avg_f1:.3f} tokens={avg_tok:.0f}")

            if done % SAVE_EVERY == 0:
                save_checkpoint(condition, results)

        save_checkpoint(condition, results)

    # Save final
    aggregates = compute_aggregates(results)
    with open(output_path, "w") as f:
        json.dump({
            "model": MODEL,
            "condition": condition,
            "condition_name": cond_label,
            "raw_mode": True,
            "sample_size": len(questions),
            "aggregates": aggregates,
            "results": results,
        }, f, indent=2)

    print(f"\n  DONE: {output_path.name}")
    print(f"  EM_ext={aggregates['em_ext']:.4f}  F1_ext={aggregates['f1_ext']:.4f}  tokens={aggregates['avg_prediction_tokens']:.0f}")

    # Clean checkpoint
    cp = checkpoint_path(condition)
    if cp.exists():
        cp.unlink()


def main():
    print(f"Loading sample from: {SAMPLE_PATH}")
    with open(SAMPLE_PATH) as f:
        sample_data = json.load(f)
    questions = sample_data["questions"]
    print(f"Sample size: {len(questions)}")

    # Need passage and class_id — load full dataset and merge
    from eval_pipeline import build_dataset
    dataset = build_dataset()
    ds_map = {d["id"]: d for d in dataset}

    # Enrich sample with passage/class_id
    enriched = []
    for q in questions:
        if q["id"] in ds_map:
            enriched.append(ds_map[q["id"]])
        else:
            enriched.append(q)
    questions = enriched

    print(f"\n{'='*60}")
    print(f"BASE MODEL EXPERIMENT")
    print(f"Model: {MODEL} (raw mode, no chat template)")
    print(f"Conditions: 1-6")
    print(f"Questions: {len(questions)}")
    print(f"{'='*60}")

    for condition in [1, 2, 3, 4, 5, 6]:
        run_condition(condition, questions)

    # Print summary
    print(f"\n\n{'='*60}")
    print(f"SUMMARY: {MODEL}")
    print(f"{'='*60}")
    print(f"{'Condition':<30s} {'EM_ext':>8s} {'F1_ext':>8s} {'Tokens':>8s}")
    print("-" * 55)

    for condition in [1, 2, 3, 4, 5, 6]:
        cond_label = condition_name(condition)
        path = RESULTS_DIR / f"llama3_text_{cond_label}.json"
        if path.exists():
            with open(path) as f:
                data = json.load(f)
            agg = data["aggregates"]
            print(f"{cond_label:<30s} {agg['em_ext']:>8.4f} {agg['f1_ext']:>8.4f} {agg['avg_prediction_tokens']:>8.1f}")


if __name__ == "__main__":
    main()
