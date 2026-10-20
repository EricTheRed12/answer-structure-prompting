"""
Recompute metrics after stripping JSON syntax from predictions.

The model often echoes the scaffold schema back in its response, polluting
the extraction window with JSON tokens ({, }, "answer_type", etc.).
This script strips JSON syntax before running max-F1 extraction.

Usage:
  cd /Users/core/Documents/GradSchool/CS699/rational-thinking
  python3 experiments/recompute_stripped.py
"""

import json
import re
import string
from collections import defaultdict
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"


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


def strip_json_syntax(text: str) -> str:
    """
    Strip JSON structural tokens from a prediction.

    Removes:
    - JSON brackets/braces: { } [ ]
    - JSON keys that are schema fields (answer_type, answer_structure, etc.)
    - Quotation marks used as JSON delimiters
    - Colons and commas in JSON context
    """
    # Remove common schema field names the model echoes
    schema_fields = [
        "answer_type", "answer_structure", "answer_form",
        "object", "relation", "identity", "defining_property",
        "components", "shared_category", "quantity", "unit",
        "measurement_context", "event", "time_expression",
        "temporal_type", "location", "agent", "action_performed",
        "object_of_action", "quality", "description_domain",
        "effect", "cause", "mechanism", "action", "actor", "outcome",
        "context_passage", "question",
        # Common JSON values the model might echo
        "single", "multiple", "list",
    ]

    # Remove JSON structural characters
    text = text.replace("{", " ").replace("}", " ")
    text = text.replace("[", " ").replace("]", " ")
    text = text.replace('"', " ")

    # Remove schema field names as whole words
    for field in schema_fields:
        text = re.sub(r"\b" + re.escape(field) + r"\b", " ", text, flags=re.IGNORECASE)

    # Collapse whitespace
    text = " ".join(text.split())
    return text


def _token_f1(pred_tokens: list, gold_tokens: list) -> float:
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
    """Extract best span after normalization."""
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


def compute_metrics_stripped(prediction: str, gold_answers: list) -> dict:
    """Compute EM_ext and F1_ext after stripping JSON from prediction."""
    stripped = strip_json_syntax(prediction)

    # EM_ext on stripped
    extracted_span = best_span_extraction(stripped, gold_answers)
    em_ext = 0.0
    for gold in gold_answers:
        if extracted_span == normalize_answer(gold):
            em_ext = 1.0
            break

    # F1_ext on stripped
    f1_ext = 0.0
    for gold in gold_answers:
        f1 = _token_f1(extracted_span.split(), normalize_answer(gold).split())
        f1_ext = max(f1_ext, f1)

    return {"em_ext_stripped": em_ext, "f1_ext_stripped": f1_ext}


# ============================================================
# MAIN
# ============================================================


def main():
    result_files = sorted(RESULTS_DIR.glob("*.json"))
    print(f"Found {len(result_files)} result files\n")

    # Collect summary for comparison
    summary = []

    print(f"{'File':<50s} {'EM_ext':>7s} {'EM_str':>7s} {'F1_ext':>7s} {'F1_str':>7s} {'Δ F1':>7s}")
    print("-" * 90)

    for filepath in result_files:
        with open(filepath) as f:
            data = json.load(f)

        results = data["results"]
        n = len(results)

        # Compute stripped metrics for each result
        em_ext_sum = 0.0
        f1_ext_sum = 0.0
        em_ext_stripped_sum = 0.0
        f1_ext_stripped_sum = 0.0

        for r in results:
            em_ext_sum += r["exact_match_extracted"]
            f1_ext_sum += r.get("f1_extracted", r["f1"])

            metrics = compute_metrics_stripped(r["prediction"], r["gold_answers"])
            em_ext_stripped_sum += metrics["em_ext_stripped"]
            f1_ext_stripped_sum += metrics["f1_ext_stripped"]

        em_ext = em_ext_sum / n
        f1_ext = f1_ext_sum / n
        em_str = em_ext_stripped_sum / n
        f1_str = f1_ext_stripped_sum / n
        delta = f1_str - f1_ext

        print(
            f"{filepath.name:<50s} "
            f"{em_ext:>7.4f} {em_str:>7.4f} "
            f"{f1_ext:>7.4f} {f1_str:>7.4f} "
            f"{delta:>+7.4f}"
        )

        summary.append({
            "file": filepath.name,
            "em_ext": em_ext,
            "em_ext_stripped": em_str,
            "f1_ext": f1_ext,
            "f1_ext_stripped": f1_str,
            "delta_f1": delta,
        })

    # Now show the key comparison: does stripping fix the C3 > C1 relationship?
    print("\n" + "=" * 80)
    print("KEY QUESTION: After stripping, does matched structure beat baseline?")
    print("=" * 80)

    models = ["llama3.2_1b", "gemma2_2b", "llama3.2_3b", "phi3_mini", "llama3_8b", "qwen3_8b"]

    print(f"\n{'Model':<15s} {'C1 F1_str':>9s} {'C3 F1_str':>9s} {'C5 F1_str':>9s} {'C3>C1?':>7s} {'C3>C5?':>7s}")
    print("-" * 60)

    for model in models:
        c1 = next((s for s in summary if s["file"] == f"{model}_question_only.json"), None)
        c3 = next((s for s in summary if s["file"] == f"{model}_question_matched.json"), None)
        c5 = next((s for s in summary if s["file"] == f"{model}_question_random.json"), None)
        if not c1 or not c3 or not c5:
            continue
        print(
            f"{model:<15s} "
            f"{c1['f1_ext_stripped']:>9.4f} "
            f"{c3['f1_ext_stripped']:>9.4f} "
            f"{c5['f1_ext_stripped']:>9.4f} "
            f"{'YES' if c3['f1_ext_stripped'] > c1['f1_ext_stripped'] else 'no':>7s} "
            f"{'YES' if c3['f1_ext_stripped'] > c5['f1_ext_stripped'] else 'no':>7s}"
        )

    print(f"\n{'Model':<15s} {'C2 F1_str':>9s} {'C4 F1_str':>9s} {'C6 F1_str':>9s} {'C4>C2?':>7s} {'C4>C6?':>7s}")
    print("-" * 60)

    for model in models:
        c2 = next((s for s in summary if s["file"] == f"{model}_question_passage.json"), None)
        c4 = next((s for s in summary if s["file"] == f"{model}_question_passage_matched.json"), None)
        c6 = next((s for s in summary if s["file"] == f"{model}_question_passage_random.json"), None)
        if not c2 or not c4 or not c6:
            continue
        print(
            f"{model:<15s} "
            f"{c2['f1_ext_stripped']:>9.4f} "
            f"{c4['f1_ext_stripped']:>9.4f} "
            f"{c6['f1_ext_stripped']:>9.4f} "
            f"{'YES' if c4['f1_ext_stripped'] > c2['f1_ext_stripped'] else 'no':>7s} "
            f"{'YES' if c4['f1_ext_stripped'] > c6['f1_ext_stripped'] else 'no':>7s}"
        )


if __name__ == "__main__":
    main()
