"""
Recompute F1_extracted on all existing result files.

Reads each result JSON, computes F1 on the max-F1 extracted span
for every prediction, updates per-question results and aggregates,
then saves back to the same file.

Usage:
  cd /Users/core/Documents/GradSchool/CS699/rational-thinking
  python3 experiments/recompute_f1_extracted.py
"""

import json
import re
import string
from collections import defaultdict
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"


# ============================================================
# METRICS (same as run_condition.py)
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


def f1_extracted(prediction: str, gold_answers: list) -> float:
    """Compute F1 on the extracted span, max over all gold answers."""
    extracted_span = best_span_extraction(prediction, gold_answers)
    extracted_tokens = extracted_span.split()
    best_f1 = 0.0
    for gold in gold_answers:
        gold_tokens = normalize_answer(gold).split()
        f1 = _token_f1(extracted_tokens, gold_tokens)
        best_f1 = max(best_f1, f1)
    return best_f1


# ============================================================
# RECOMPUTE
# ============================================================


def recompute_file(filepath: Path) -> dict:
    """Recompute F1_extracted for all results in a file."""
    with open(filepath) as f:
        data = json.load(f)

    results = data["results"]
    updated = 0

    for r in results:
        f1_ext = f1_extracted(r["prediction"], r["gold_answers"])
        r["f1_extracted"] = f1_ext
        updated += 1

    # Recompute aggregates
    n = len(results)
    if n > 0:
        data["aggregates"]["f1_extracted"] = round(
            sum(r["f1_extracted"] for r in results) / n, 4
        )
        # Also ensure other aggregates are current
        data["aggregates"]["em"] = round(
            sum(r["exact_match"] for r in results) / n, 4
        )
        data["aggregates"]["em_extracted"] = round(
            sum(r["exact_match_extracted"] for r in results) / n, 4
        )
        data["aggregates"]["f1"] = round(
            sum(r["f1"] for r in results) / n, 4
        )
        data["aggregates"]["avg_prediction_tokens"] = round(
            sum(r["prediction_tokens"] for r in results) / n, 1
        )

        # Per-class breakdown
        by_class = defaultdict(list)
        for r in results:
            by_class[str(r["class_id"])].append(r)

        class_metrics = {}
        for cid, class_results in sorted(by_class.items()):
            cn = len(class_results)
            class_metrics[cid] = {
                "n": cn,
                "em": round(sum(r["exact_match"] for r in class_results) / cn, 4),
                "em_extracted": round(sum(r["exact_match_extracted"] for r in class_results) / cn, 4),
                "f1": round(sum(r["f1"] for r in class_results) / cn, 4),
                "f1_extracted": round(sum(r["f1_extracted"] for r in class_results) / cn, 4),
                "avg_tokens": round(sum(r["prediction_tokens"] for r in class_results) / cn, 1),
            }
        data["aggregates"]["by_class"] = class_metrics

    # Save back
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    return data["aggregates"]


def main():
    result_files = sorted(RESULTS_DIR.glob("*.json"))
    print(f"Found {len(result_files)} result files\n")
    print(f"{'File':<50s} {'EM_ext':>7s} {'F1':>7s} {'F1_ext':>7s} {'Tokens':>7s}")
    print("-" * 85)

    for filepath in result_files:
        agg = recompute_file(filepath)
        print(
            f"{filepath.name:<50s} "
            f"{agg['em_extracted']:>7.4f} "
            f"{agg['f1']:>7.4f} "
            f"{agg['f1_extracted']:>7.4f} "
            f"{agg['avg_prediction_tokens']:>7.1f}"
        )

    print(f"\nDone. All {len(result_files)} files updated with f1_extracted.")


if __name__ == "__main__":
    main()
