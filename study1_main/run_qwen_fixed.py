"""
Re-run conditions 1-6 for Qwen 3 8B with thinking disabled.

Qwen 3 is a reasoning model and, under Ollama, thinks by default. In the
original main experiment (num_predict=512, /api/generate), that reasoning
frequently consumed the entire token budget, leaving an empty `response`
field that scored zero (300-700 empty responses per condition).

To evaluate Qwen on the same footing as the other instruction-tuned models,
which answer directly, this run disables thinking with `think: false`. Because
the /api/generate endpoint ignores the think flag for qwen3, this uses
/api/chat (which respects it), sending the identical JSON scaffold as a single
user message. Everything else matches the original main experiment:
  - same 1000-question stratified sample
  - same JSON scaffold (scaffold_builder.build_scaffold)
  - same scoring (EM, EM_ext, F1, F1_ext) and aggregation
  - same condition 5/6 random-seed logic

Output files are tagged `qwen3_8b_fixed_*` so the original (artifact-affected)
`qwen3_8b_*` files are preserved unchanged.

Usage (run from the repository root):
  caffeinate -i python3 study1_main/run_qwen_fixed.py
"""

import json
import time
from collections import defaultdict
from pathlib import Path

import requests

import sys
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from scaffold_builder import build_scaffold, condition_name
from run_condition import (
    normalize_answer,
    _token_f1,
    best_span_extraction,
    exact_match,
    exact_match_extracted,
    f1_score,
)

BASE_URL = "http://localhost:11434"
MODEL = "qwen3:8b"
NUM_PREDICT = 512
SEED = 42
SAVE_EVERY = 25

STUDY_DIR = Path(__file__).parent
RESULTS_DIR = STUDY_DIR / "results"
CHECKPOINTS_DIR = STUDY_DIR / "checkpoints"
SAMPLE_PATH = PROJECT_ROOT / "data" / "sample_1000.json"

TAG = "qwen3_8b_fixed"


def query_ollama(prompt: str) -> str:
    """Chat endpoint with thinking disabled. Returns the answer text."""
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "think": False,
        "stream": False,
        "options": {"temperature": 0.0, "num_predict": NUM_PREDICT},
    }
    try:
        resp = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=180)
        resp.raise_for_status()
        data = resp.json()
        return (data.get("message", {}).get("content", "") or "").strip()
    except requests.exceptions.Timeout:
        return ""
    except Exception as e:
        print(f"  ERROR: {e}")
        return ""


def checkpoint_path(condition: int) -> Path:
    return CHECKPOINTS_DIR / f"{TAG}_{condition_name(condition)}_checkpoint.json"


def load_checkpoint(condition: int) -> list:
    path = checkpoint_path(condition)
    if path.exists():
        with open(path) as f:
            return json.load(f).get("results", [])
    return []


def save_checkpoint(condition: int, results: list):
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(checkpoint_path(condition), "w") as f:
        json.dump({"model": MODEL, "condition": condition, "results": results}, f)


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
            "em": round(sum(r["exact_match"] for r in cr) / cn, 4),
            "em_extracted": round(sum(r["exact_match_extracted"] for r in cr) / cn, 4),
            "f1": round(sum(r["f1"] for r in cr) / cn, 4),
            "f1_extracted": round(sum(r["f1_extracted"] for r in cr) / cn, 4),
            "avg_tokens": round(sum(r["prediction_tokens"] for r in cr) / cn, 1),
        }

    return {
        "n": n,
        "em": round(sum(r["exact_match"] for r in results) / n, 4),
        "em_extracted": round(sum(r["exact_match_extracted"] for r in results) / n, 4),
        "f1": round(sum(r["f1"] for r in results) / n, 4),
        "f1_extracted": round(sum(r["f1_extracted"] for r in results) / n, 4),
        "avg_prediction_tokens": round(sum(r["prediction_tokens"] for r in results) / n, 1),
        "empty_predictions": sum(1 for r in results if not (r["prediction"] or "").strip()),
        "by_class": class_metrics,
    }


def run_condition(condition: int, questions: list):
    cond_label = condition_name(condition)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / f"{TAG}_{cond_label}.json"
    if output_path.exists():
        print(f"SKIPPED: {output_path.name} already exists")
        return

    existing = load_checkpoint(condition)
    sample_ids = {q["id"] for q in questions}
    existing = [r for r in existing if r["id"] in sample_ids]
    completed_ids = {r["id"] for r in existing}
    if existing:
        print(f"  Resuming from checkpoint: {len(existing)} already done")

    remaining = [q for q in questions if q["id"] not in completed_ids]

    print(f"\n{'='*60}")
    print(f"Model: {MODEL} (think=False via /api/chat, num_predict={NUM_PREDICT})")
    print(f"Condition {condition}: {cond_label}")
    print(f"Remaining: {len(remaining)}/{len(questions)}")
    print(f"{'='*60}")

    if not remaining:
        results = existing
    else:
        results = existing.copy()
        for i, item in enumerate(remaining):
            scaffold = build_scaffold(
                question=item["question"],
                condition=condition,
                passage=item["passage"] if condition in (2, 4, 6, 8) else None,
                class_id=item["class_id"] if condition >= 3 else None,
                random_seed=SEED + questions.index(item) if condition in (5, 6) else None,
            )
            t0 = time.time()
            prediction = query_ollama(scaffold)
            latency = time.time() - t0

            em = exact_match(prediction, item["gold_answers"])
            em_ext = exact_match_extracted(prediction, item["gold_answers"])
            f1 = f1_score(prediction, item["gold_answers"])
            extracted = best_span_extraction(prediction, item["gold_answers"])
            f1_ext = 0.0
            for gold in item["gold_answers"]:
                f1_ext = max(f1_ext, _token_f1(extracted.split(), normalize_answer(gold).split()))

            results.append({
                "id": item["id"],
                "question": item["question"],
                "gold_answers": item["gold_answers"],
                "prediction": prediction,
                "class_id": item["class_id"],
                "exact_match": em,
                "exact_match_extracted": em_ext,
                "f1": f1,
                "f1_extracted": f1_ext,
                "prediction_tokens": len(prediction.split()),
                "latency_s": round(latency, 2),
            })

            done = len(results)
            if done % 10 == 0 or (i + 1) == len(remaining):
                avg_em_ext = sum(r["exact_match_extracted"] for r in results) / done
                avg_f1_ext = sum(r["f1_extracted"] for r in results) / done
                empties = sum(1 for r in results if not (r["prediction"] or "").strip())
                print(f"  [{done}/{len(questions)}] EM_ext={avg_em_ext:.3f} F1_ext={avg_f1_ext:.3f} empty={empties}")

            if done % SAVE_EVERY == 0:
                save_checkpoint(condition, results)

        save_checkpoint(condition, results)

    aggregates = compute_aggregates(results)
    with open(output_path, "w") as f:
        json.dump({
            "model": MODEL,
            "condition": condition,
            "condition_name": cond_label,
            "num_predict": NUM_PREDICT,
            "thinking_enabled": False,
            "endpoint": "chat",
            "sample_size": len(questions),
            "aggregates": aggregates,
            "results": results,
        }, f, indent=2)

    print(f"\n  DONE: {output_path.name}")
    print(f"  EM_ext={aggregates['em_extracted']:.4f}  F1_ext={aggregates['f1_extracted']:.4f}  "
          f"empty={aggregates['empty_predictions']}  tokens={aggregates['avg_prediction_tokens']:.0f}")

    cp = checkpoint_path(condition)
    if cp.exists():
        cp.unlink()


def main():
    print(f"Loading sample from: {SAMPLE_PATH}")
    with open(SAMPLE_PATH) as f:
        questions = json.load(f)["questions"]

    print(f"\n{'='*60}")
    print(f"QWEN RE-RUN (think=False, num_predict={NUM_PREDICT})")
    print(f"Conditions 1-6 | Questions: {len(questions)}")
    print(f"{'='*60}")

    for condition in [1, 2, 3, 4, 5, 6]:
        run_condition(condition, questions)

    print(f"\n\n{'='*60}")
    print(f"SUMMARY: {MODEL} (fixed, non-thinking)")
    print(f"{'='*60}")
    print(f"{'Condition':<30s} {'EM_ext':>8s} {'F1_ext':>8s} {'Empty':>7s} {'Tokens':>8s}")
    print("-" * 64)
    for condition in [1, 2, 3, 4, 5, 6]:
        path = RESULTS_DIR / f"{TAG}_{condition_name(condition)}.json"
        if path.exists():
            with open(path) as f:
                agg = json.load(f)["aggregates"]
            print(f"{condition_name(condition):<30s} {agg['em_extracted']:>8.4f} "
                  f"{agg['f1_extracted']:>8.4f} {agg['empty_predictions']:>7d} "
                  f"{agg['avg_prediction_tokens']:>8.1f}")


if __name__ == "__main__":
    main()
