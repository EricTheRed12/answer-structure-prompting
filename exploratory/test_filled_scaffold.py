"""
Test the filled-scaffold hypothesis: two-pass extraction + generation.

Pipeline:
  Pass 1 (Extract): model fills in the answer structure schema from the passage
  Pass 2 (Generate): model answers the question using ONLY the filled schema (no passage)

Compared against:
  - Baseline: question only (no passage, no structure)
  - Passage only: question + raw passage
  - Filled scaffold: question + filled schema (no passage in pass 2)

This tests whether structured extraction is a more efficient context than raw passage.

Usage:
  cd /Users/core/Documents/GradSchool/CS699/rational-thinking
  python3 experiments/test_filled_scaffold.py

Results saved to: experiments/results/filled_scaffold_test.json
"""

import json
import re
import string
import time
from collections import defaultdict
from pathlib import Path

import requests

import sys
sys.path.insert(0, str(Path(__file__).parent))
from scaffold_builder import get_answer_structure
from eval_pipeline import (
    normalize_answer, _token_f1, best_span_extraction,
    exact_match_extracted, build_dataset
)

MODEL = "llama3:8b"
BASE_URL = "http://localhost:11434"
RESULTS_DIR = Path(__file__).parent / "results"


# ============================================================
# INFERENCE
# ============================================================


def query_ollama(prompt: str, max_tokens: int = 512) -> str:
    try:
        resp = requests.post(f"{BASE_URL}/api/generate", json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0, "num_predict": max_tokens},
        }, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except Exception as e:
        print(f"  ERROR: {e}")
        return ""


# ============================================================
# METRICS
# ============================================================


def f1_ext(prediction: str, gold_answers: list) -> float:
    """Compute F1 on extracted span."""
    extracted = best_span_extraction(prediction, gold_answers)
    best = 0.0
    for gold in gold_answers:
        f1 = _token_f1(extracted.split(), normalize_answer(gold).split())
        best = max(best, f1)
    return best


# ============================================================
# SCAFFOLD FORMATS
# ============================================================


def build_extraction_prompt(question: str, passage: str, class_id: int) -> str:
    """
    Pass 1: Ask model to extract information from passage into the schema.
    """
    schema = get_answer_structure(class_id)
    schema_str = json.dumps(schema, indent=2)

    return f"""Extract the answer to the question from the passage and fill in the schema fields below.
Respond with ONLY the filled JSON schema, no other text.

Question: {question}

Passage: {passage}

Schema to fill:
{schema_str}"""


def build_generation_from_filled(question: str, filled_schema: str) -> str:
    """
    Pass 2: Generate answer from the filled schema (no passage).
    """
    return f"""Answer the question using the following extracted information. Respond concisely with just the answer.

Question: {question}

Extracted information:
{filled_schema}"""


def build_passage_prompt(question: str, passage: str) -> str:
    """Baseline with passage."""
    return f"Question: {question}\n\nContext: {passage}"


# ============================================================
# MAIN
# ============================================================


def main():
    print("Loading dataset...")
    dataset = build_dataset()

    # Load stratified sample
    sample_path = Path(__file__).parent / "sample_1000.json"
    with open(sample_path) as f:
        sample_data = json.load(f)
    sample_ids = [q["id"] for q in sample_data["questions"][:200]]
    items = [d for d in dataset if d["id"] in sample_ids][:200]
    print(f"Testing {len(items)} questions with {MODEL}\n")

    results = {
        "baseline": [],        # question only
        "passage": [],         # question + passage
        "filled_scaffold": [], # question + filled schema (two-pass)
    }

    for i, item in enumerate(items):
        q = item["question"]
        passage = item["passage"]
        gold = item["gold_answers"]
        cid = item["class_id"]

        # --- Condition A: Baseline (question only) ---
        pred_a = query_ollama(q)
        em_a = exact_match_extracted(pred_a, gold)
        f1_a = f1_ext(pred_a, gold)
        results["baseline"].append({
            "id": item["id"], "em_ext": em_a, "f1_ext": f1_a,
            "tokens": len(pred_a.split()), "prediction": pred_a,
        })

        # --- Condition B: Passage only ---
        pred_b = query_ollama(build_passage_prompt(q, passage))
        em_b = exact_match_extracted(pred_b, gold)
        f1_b = f1_ext(pred_b, gold)
        results["passage"].append({
            "id": item["id"], "em_ext": em_b, "f1_ext": f1_b,
            "tokens": len(pred_b.split()), "prediction": pred_b,
        })

        # --- Condition C: Filled scaffold (two-pass) ---
        # Pass 1: Extract into schema
        extraction_prompt = build_extraction_prompt(q, passage, cid)
        filled_schema = query_ollama(extraction_prompt, max_tokens=256)

        # Pass 2: Generate from filled schema
        gen_prompt = build_generation_from_filled(q, filled_schema)
        pred_c = query_ollama(gen_prompt)
        em_c = exact_match_extracted(pred_c, gold)
        f1_c = f1_ext(pred_c, gold)
        results["filled_scaffold"].append({
            "id": item["id"], "em_ext": em_c, "f1_ext": f1_c,
            "tokens": len(pred_c.split()), "prediction": pred_c,
            "filled_schema": filled_schema,
        })

        # Progress every 10 questions
        if (i + 1) % 10 == 0:
            n = i + 1
            avg_a = sum(r["f1_ext"] for r in results["baseline"]) / n
            avg_b = sum(r["f1_ext"] for r in results["passage"]) / n
            avg_c = sum(r["f1_ext"] for r in results["filled_scaffold"]) / n
            print(
                f"  [{n}/200] "
                f"baseline={avg_a:.3f}  passage={avg_b:.3f}  filled={avg_c:.3f}"
            )

    # Final summary
    print(f"\n{'='*70}")
    print(f"FINAL RESULTS (n={len(items)}, {MODEL})")
    print(f"{'='*70}")
    print(f"{'Condition':<20s} {'EM_ext':>8s} {'F1_ext':>8s} {'Tokens':>8s}")
    print("-" * 50)

    for name, res in results.items():
        n = len(res)
        avg_em = sum(r["em_ext"] for r in res) / n
        avg_f1 = sum(r["f1_ext"] for r in res) / n
        avg_tok = sum(r["tokens"] for r in res) / n
        print(f"{name:<20s} {avg_em:>8.4f} {avg_f1:>8.4f} {avg_tok:>8.1f}")

    # Save full results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "filled_scaffold_test.json"
    summary = {}
    for name, res in results.items():
        n = len(res)
        summary[name] = {
            "n": n,
            "em_ext": round(sum(r["em_ext"] for r in res) / n, 4),
            "f1_ext": round(sum(r["f1_ext"] for r in res) / n, 4),
            "avg_tokens": round(sum(r["tokens"] for r in res) / n, 1),
        }

    with open(output_path, "w") as f:
        json.dump({
            "model": MODEL,
            "n": len(items),
            "summary": summary,
            "results": results,
        }, f, indent=2)

    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
