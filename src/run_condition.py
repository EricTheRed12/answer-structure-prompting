"""
Run a single experimental condition for a single model with checkpoint/resume.

This is the production experiment runner. It processes one condition at a time,
saves progress every 25 questions, and can resume from where it left off.

Usage (run from the repository root):
  python3 src/run_condition.py --model llama3.2:3b --condition 1
  python3 src/run_condition.py --model llama3:8b --condition 4 --sample data/sample_1000.json

Features:
  - Checkpoint/resume: saves every 25 questions, resumes automatically
  - Single condition per invocation: run in parallel or sequence
  - Fixed sample: all conditions/models use the same question set
  - Verbosity tracking: records prediction token count per question
"""

import argparse
import json
import re
import string
import time
from collections import defaultdict
from pathlib import Path
from typing import Optional

import requests

import sys
sys.path.insert(0, str(Path(__file__).parent))
from scaffold_builder import build_scaffold, condition_name

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).parent.parent
RESULTS_DIR = PROJECT_ROOT / "study1_main" / "results"
CHECKPOINTS_DIR = PROJECT_ROOT / "study1_main" / "checkpoints"

# ============================================================
# METRICS
# ============================================================


def normalize_answer(text: str) -> str:
    """Lower, strip articles/punctuation/whitespace for SQuAD evaluation."""
    text = text.lower()
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = " ".join(text.split())
    return text


def _token_f1(pred_tokens: list, gold_tokens: list) -> float:
    """Compute token-level F1 between two token lists."""
    if not pred_tokens or not gold_tokens:
        return 0.0
    common = set(pred_tokens) & set(gold_tokens)
    num_common = sum(min(pred_tokens.count(t), gold_tokens.count(t)) for t in common)
    if num_common == 0:
        return 0.0
    precision = num_common / len(pred_tokens)
    recall = num_common / len(gold_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def best_span_extraction(prediction: str, gold_answers: list) -> str:
    """
    Extract the contiguous token span from prediction that maximizes F1
    against the best-matching gold answer.
    """
    pred_tokens = normalize_answer(prediction).split()
    if not pred_tokens:
        return ""

    gold_token_lists = [normalize_answer(g).split() for g in gold_answers]
    max_gold_len = max(len(g) for g in gold_token_lists) if gold_token_lists else 1
    max_span_len = min(len(pred_tokens), max_gold_len * 2)

    best_f1 = 0.0
    best_span_tokens = pred_tokens

    for start in range(len(pred_tokens)):
        for end in range(start + 1, min(start + max_span_len + 1, len(pred_tokens) + 1)):
            span = pred_tokens[start:end]
            for gold_tokens in gold_token_lists:
                f1 = _token_f1(span, gold_tokens)
                if f1 > best_f1:
                    best_f1 = f1
                    best_span_tokens = span

    return " ".join(best_span_tokens)


def exact_match(prediction: str, gold_answers: list) -> float:
    pred_norm = normalize_answer(prediction)
    for gold in gold_answers:
        if pred_norm == normalize_answer(gold):
            return 1.0
    return 0.0


def exact_match_extracted(prediction: str, gold_answers: list) -> float:
    extracted = best_span_extraction(prediction, gold_answers)
    for gold in gold_answers:
        if extracted == normalize_answer(gold):
            return 1.0
    return 0.0


def f1_score(prediction: str, gold_answers: list) -> float:
    pred_tokens = normalize_answer(prediction).split()
    best_f1 = 0.0
    for gold in gold_answers:
        gold_tokens = normalize_answer(gold).split()
        f1 = _token_f1(pred_tokens, gold_tokens)
        best_f1 = max(best_f1, f1)
    return best_f1


# ============================================================
# OLLAMA INFERENCE
# ============================================================


def query_ollama(
    prompt: str,
    model: str,
    base_url: str = "http://localhost:11434",
    temperature: float = 0.0,
    max_tokens: int = 512,
) -> str:
    """Send a prompt to Ollama and return the response text."""
    url = f"{base_url}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }

    try:
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            f"Cannot connect to Ollama at {base_url}. "
            "Make sure Ollama is running (ollama serve)."
        )
    except requests.exceptions.Timeout:
        return ""
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Ollama HTTP error: {e}")


# ============================================================
# CHECKPOINT MANAGEMENT
# ============================================================


def checkpoint_path(model: str, condition: int) -> Path:
    """Get the checkpoint file path for a model+condition."""
    model_safe = model.replace(":", "_").replace("/", "_")
    cond_label = condition_name(condition)
    return CHECKPOINTS_DIR / f"{model_safe}_{cond_label}_checkpoint.json"


def load_checkpoint(model: str, condition: int) -> list:
    """Load existing checkpoint results, or return empty list."""
    path = checkpoint_path(model, condition)
    if path.exists():
        with open(path) as f:
            data = json.load(f)
        return data.get("results", [])
    return []


def save_checkpoint(model: str, condition: int, results: list):
    """Save current results to checkpoint."""
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    path = checkpoint_path(model, condition)
    with open(path, "w") as f:
        json.dump({"model": model, "condition": condition, "results": results}, f)


# ============================================================
# MAIN RUNNER
# ============================================================


def compute_aggregates(results: list) -> dict:
    """Compute aggregate metrics from per-question results."""
    if not results:
        return {"em": 0.0, "em_extracted": 0.0, "f1": 0.0, "n": 0}

    n = len(results)
    avg_em = sum(r["exact_match"] for r in results) / n
    avg_em_ext = sum(r["exact_match_extracted"] for r in results) / n
    avg_f1 = sum(r["f1"] for r in results) / n
    avg_f1_ext = sum(r.get("f1_extracted", r["f1"]) for r in results) / n
    avg_latency = sum(r["latency_s"] for r in results) / n
    avg_tokens = sum(r["prediction_tokens"] for r in results) / n

    # Per-class breakdown
    by_class = defaultdict(list)
    for r in results:
        by_class[r["class_id"]].append(r)

    class_metrics = {}
    for cid, class_results in sorted(by_class.items()):
        cn = len(class_results)
        class_metrics[str(cid)] = {
            "n": cn,
            "em": round(sum(r["exact_match"] for r in class_results) / cn, 4),
            "em_extracted": round(sum(r["exact_match_extracted"] for r in class_results) / cn, 4),
            "f1": round(sum(r["f1"] for r in class_results) / cn, 4),
            "f1_extracted": round(sum(r.get("f1_extracted", r["f1"]) for r in class_results) / cn, 4),
            "avg_tokens": round(sum(r["prediction_tokens"] for r in class_results) / cn, 1),
        }

    return {
        "n": n,
        "em": round(avg_em, 4),
        "em_extracted": round(avg_em_ext, 4),
        "f1": round(avg_f1, 4),
        "f1_extracted": round(avg_f1_ext, 4),
        "avg_latency_s": round(avg_latency, 2),
        "avg_prediction_tokens": round(avg_tokens, 1),
        "by_class": class_metrics,
    }


def run(args):
    """Run a single condition with checkpoint/resume."""
    # Check if final result already exists (skip completed runs)
    model_safe = args.model.replace(":", "_").replace("/", "_")
    cond_label = condition_name(args.condition)
    output_path = RESULTS_DIR / f"{model_safe}_{cond_label}.json"
    if output_path.exists():
        print(f"SKIPPED: {output_path.name} already exists")
        return

    # Load sample
    print(f"Loading sample from: {args.sample}")
    with open(args.sample) as f:
        sample_data = json.load(f)
    questions = sample_data["questions"]

    # Apply limit if specified
    if args.limit:
        questions = questions[:args.limit]

    print(f"  Sample size: {len(questions)}")

    condition = args.condition
    model = args.model
    cond_label = condition_name(condition)
    save_every = args.save_every

    # Load checkpoint
    existing_results = load_checkpoint(model, condition)
    # Only keep results for questions in our current sample
    sample_ids = {q["id"] for q in questions}
    existing_results = [r for r in existing_results if r["id"] in sample_ids]
    completed_ids = {r["id"] for r in existing_results}

    if existing_results:
        print(f"  Resuming from checkpoint: {len(existing_results)} already done")

    # Filter to remaining questions
    remaining = [q for q in questions if q["id"] not in completed_ids]
    total_remaining = len(remaining)
    total_overall = len(questions)

    print(f"\n{'='*60}")
    print(f"Model: {model}")
    print(f"Condition {condition}: {cond_label}")
    print(f"Remaining: {total_remaining}/{total_overall}")
    print(f"Save every: {save_every} questions")
    print(f"{'='*60}\n")

    if total_remaining == 0:
        print("All questions already completed!")
        results = existing_results
    else:
        results = existing_results.copy()
        random_seed = args.seed

        for i, item in enumerate(remaining):
            # Build scaffold
            scaffold = build_scaffold(
                question=item["question"],
                condition=condition,
                passage=item["passage"] if condition in (2, 4, 6, 8) else None,
                class_id=item["class_id"] if condition >= 3 else None,
                random_seed=random_seed + questions.index(item) if condition in (5, 6) else None,
            )

            # Query model
            t0 = time.time()
            prediction = query_ollama(
                scaffold, model=model, base_url=args.base_url
            )
            latency = time.time() - t0

            # Score
            em = exact_match(prediction, item["gold_answers"])
            em_ext = exact_match_extracted(prediction, item["gold_answers"])
            f1 = f1_score(prediction, item["gold_answers"])
            # F1 on extracted span (more meaningful for verbose outputs)
            extracted_span = best_span_extraction(prediction, item["gold_answers"])
            f1_ext = _token_f1(extracted_span.split(), normalize_answer(item["gold_answers"][0]).split())
            # Take max F1_ext over all gold answers
            for gold in item["gold_answers"][1:]:
                f1_ext = max(f1_ext, _token_f1(extracted_span.split(), normalize_answer(gold).split()))
            pred_tokens = len(prediction.split())

            result = {
                "id": item["id"],
                "question": item["question"],
                "gold_answers": item["gold_answers"],
                "prediction": prediction,
                "class_id": item["class_id"],
                "exact_match": em,
                "exact_match_extracted": em_ext,
                "f1": f1,
                "f1_extracted": f1_ext,
                "prediction_tokens": pred_tokens,
                "latency_s": round(latency, 2),
            }
            results.append(result)

            # Progress
            done_total = len(results)
            if done_total % 10 == 0 or (i + 1) == total_remaining:
                avg_em_ext = sum(r["exact_match_extracted"] for r in results) / done_total
                avg_f1_ext = sum(r.get("f1_extracted", r["f1"]) for r in results) / done_total
                avg_tok = sum(r["prediction_tokens"] for r in results) / done_total
                print(
                    f"  [{done_total}/{total_overall}] "
                    f"EM_ext={avg_em_ext:.3f} F1_ext={avg_f1_ext:.3f} "
                    f"avg_tokens={avg_tok:.0f}"
                )

            # Checkpoint
            if done_total % save_every == 0:
                save_checkpoint(model, condition, results)
                print(f"    (checkpoint saved: {done_total} results)")

        # Final checkpoint
        save_checkpoint(model, condition, results)

    # Compute and save final results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    aggregates = compute_aggregates(results)

    model_safe = model.replace(":", "_").replace("/", "_")
    output_path = RESULTS_DIR / f"{model_safe}_{cond_label}.json"

    with open(output_path, "w") as f:
        json.dump(
            {
                "model": model,
                "condition": condition,
                "condition_name": cond_label,
                "sample_size": len(questions),
                "aggregates": aggregates,
                "results": results,
            },
            f, indent=2,
        )

    print(f"\n{'='*60}")
    print(f"DONE: {output_path.name}")
    print(f"  EM={aggregates['em']:.4f}  EM_ext={aggregates['em_extracted']:.4f}  "
          f"F1={aggregates['f1']:.4f}  F1_ext={aggregates['f1_extracted']:.4f}  "
          f"avg_tokens={aggregates['avg_prediction_tokens']:.0f}")
    print(f"{'='*60}")

    # Clean up checkpoint
    cp = checkpoint_path(model, condition)
    if cp.exists():
        cp.unlink()
        print(f"  Checkpoint removed (run complete)")


def main():
    parser = argparse.ArgumentParser(
        description="Run one experimental condition with checkpoint/resume"
    )
    parser.add_argument(
        "--model", type=str, required=True,
        help="Ollama model name (e.g. llama3.2:3b, llama3:8b)"
    )
    parser.add_argument(
        "--condition", type=int, required=True,
        help="Condition number (1-8)"
    )
    parser.add_argument(
        "--sample", type=str, default="data/sample_1000.json",
        help="Path to sample JSON file"
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for conditions 5-6"
    )
    parser.add_argument(
        "--save-every", type=int, default=25,
        help="Save checkpoint every N questions (default 25)"
    )
    parser.add_argument(
        "--base-url", type=str, default="http://localhost:11434",
        help="Ollama API base URL"
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Limit total questions to process (for testing). Includes already-checkpointed."
    )

    args = parser.parse_args()

    if args.condition < 1 or args.condition > 8:
        parser.error("Condition must be 1-8")

    run(args)


if __name__ == "__main__":
    main()
