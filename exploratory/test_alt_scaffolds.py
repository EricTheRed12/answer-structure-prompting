"""
Test alternative scaffold formats to see if the delivery mechanism matters.

Three formats tested:
  A) Original JSON (current: raw JSON with empty schema fields)
  B) Natural language hint (schema info expressed as a sentence)
  C) Instruction-prefixed JSON (adds "use this structure to guide your answer")

All compared against baseline (question only) on 50 questions, llama3:8b.

Usage:
  cd /Users/core/Documents/GradSchool/CS699/rational-thinking
  python3 experiments/test_alt_scaffolds.py
"""

import json
import re
import string
import time
from pathlib import Path
from typing import Optional

import requests

import sys
sys.path.insert(0, str(Path(__file__).parent))
from scaffold_builder import _get_schemas, get_answer_structure
from eval_pipeline import (
    normalize_answer, _token_f1, best_span_extraction,
    exact_match_extracted, f1_score, build_dataset
)

# ============================================================
# SCAFFOLD FORMATS
# ============================================================

# Class ID → natural language description of what the answer should look like
NL_HINTS = {
    1: "Answer with the name of the specific object, entity, or thing being identified.",
    2: "Answer with the name of the person or concept being identified by their defining property.",
    3: "Answer with a list of the multiple distinct components being asked about.",
    4: "Answer with the specific number, count, or measurement.",
    5: "Answer with the specific date, year, time period, or duration.",
    6: "Answer with the specific place or geographic location.",
    7: "Answer with the name of who or what performed the action.",
    8: "Answer with the quality, property, or characteristic being described.",
    9: "Answer with the cause, reason, or explanation for why it happened.",
    10: "Answer with the outcome, effect, or result of the action.",
}


def build_baseline(question: str, passage: Optional[str] = None) -> str:
    """Format A: bare question (or question + passage)."""
    if passage:
        return f"Question: {question}\n\nContext: {passage}"
    return question


def build_json_scaffold(question: str, class_id: int, passage: Optional[str] = None) -> str:
    """Format B: original JSON scaffold (what we've been using)."""
    schema = get_answer_structure(class_id)
    scaffold = {"question": question, "answer_structure": schema}
    if passage:
        scaffold["context_passage"] = passage
    return json.dumps(scaffold, indent=2)


def build_nl_scaffold(question: str, class_id: int, passage: Optional[str] = None) -> str:
    """Format C: natural language hint."""
    hint = NL_HINTS.get(class_id, "Answer the question concisely.")
    if passage:
        return f"Question: {question}\n\nContext: {passage}\n\n{hint}"
    return f"Question: {question}\n\n{hint}"


def build_instruction_json(question: str, class_id: int, passage: Optional[str] = None) -> str:
    """Format D: instruction-prefixed JSON scaffold."""
    schema = get_answer_structure(class_id)
    instruction = "Use the following answer structure to guide your response. Fill in the empty fields with your answer, responding concisely."
    scaffold = {"question": question, "answer_structure": schema}
    if passage:
        scaffold["context_passage"] = passage
    return f"{instruction}\n\n{json.dumps(scaffold, indent=2)}"


# ============================================================
# INFERENCE
# ============================================================


def query_ollama(prompt: str, model: str = "llama3:8b") -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0, "num_predict": 512},
    }
    try:
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except Exception as e:
        print(f"  ERROR: {e}")
        return ""


# ============================================================
# MAIN
# ============================================================


def compute_f1_ext(prediction: str, gold_answers: list) -> float:
    """Compute F1 on extracted span."""
    extracted = best_span_extraction(prediction, gold_answers)
    best_f1 = 0.0
    for gold in gold_answers:
        f1 = _token_f1(extracted.split(), normalize_answer(gold).split())
        best_f1 = max(best_f1, f1)
    return best_f1


def main():
    print("Loading dataset...")
    dataset = build_dataset()
    # Use first 50 from the sample for consistency
    sample_path = Path(__file__).parent / "sample_1000.json"
    with open(sample_path) as f:
        sample_data = json.load(f)
    sample_ids = [q["id"] for q in sample_data["questions"][:50]]
    items = [d for d in dataset if d["id"] in sample_ids][:50]
    print(f"Testing with {len(items)} questions on llama3:8b\n")

    formats = {
        "A_baseline": build_baseline,
        "B_json_scaffold": build_json_scaffold,
        "C_nl_hint": build_nl_scaffold,
        "D_instruction_json": build_instruction_json,
    }

    results = {name: [] for name in formats}

    for i, item in enumerate(items):
        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/50]")

        for name, builder in formats.items():
            if name == "A_baseline":
                prompt = builder(item["question"])
            else:
                prompt = builder(item["question"], item["class_id"])

            prediction = query_ollama(prompt)
            em_ext = exact_match_extracted(prediction, item["gold_answers"])
            f1_ext = compute_f1_ext(prediction, item["gold_answers"])
            tokens = len(prediction.split())

            results[name].append({
                "em_ext": em_ext,
                "f1_ext": f1_ext,
                "tokens": tokens,
            })

    # Summary
    print(f"\n{'='*70}")
    print(f"RESULTS (n=50, llama3:8b, no passage)")
    print(f"{'='*70}")
    print(f"{'Format':<25s} {'EM_ext':>8s} {'F1_ext':>8s} {'Tokens':>8s}")
    print("-" * 55)

    for name, res in results.items():
        n = len(res)
        avg_em = sum(r["em_ext"] for r in res) / n
        avg_f1 = sum(r["f1_ext"] for r in res) / n
        avg_tok = sum(r["tokens"] for r in res) / n
        print(f"{name:<25s} {avg_em:>8.4f} {avg_f1:>8.4f} {avg_tok:>8.1f}")

    # Now test WITH passage
    print(f"\n\nRunning with passage...")

    results_passage = {name: [] for name in formats}

    for i, item in enumerate(items):
        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/50]")

        for name, builder in formats.items():
            if name == "A_baseline":
                prompt = builder(item["question"], passage=item["passage"])
            else:
                prompt = builder(item["question"], item["class_id"], passage=item["passage"])

            prediction = query_ollama(prompt)
            em_ext = exact_match_extracted(prediction, item["gold_answers"])
            f1_ext = compute_f1_ext(prediction, item["gold_answers"])
            tokens = len(prediction.split())

            results_passage[name].append({
                "em_ext": em_ext,
                "f1_ext": f1_ext,
                "tokens": tokens,
            })

    print(f"\n{'='*70}")
    print(f"RESULTS (n=50, llama3:8b, WITH passage)")
    print(f"{'='*70}")
    print(f"{'Format':<25s} {'EM_ext':>8s} {'F1_ext':>8s} {'Tokens':>8s}")
    print("-" * 55)

    for name, res in results_passage.items():
        n = len(res)
        avg_em = sum(r["em_ext"] for r in res) / n
        avg_f1 = sum(r["f1_ext"] for r in res) / n
        avg_tok = sum(r["tokens"] for r in res) / n
        print(f"{name:<25s} {avg_em:>8.4f} {avg_f1:>8.4f} {avg_tok:>8.1f}")


if __name__ == "__main__":
    main()
