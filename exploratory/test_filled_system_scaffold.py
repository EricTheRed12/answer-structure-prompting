"""
Test: Fill structure from passage, then use filled structure as system prompt.

Pipeline:
  Pass 1: Model extracts info from passage into the answer schema
  Pass 2: Filled schema goes in SYSTEM prompt, question as user prompt (no passage)

Compared against baseline and passage-only on 50 random questions.

Usage:
  cd /Users/core/Documents/GradSchool/CS699/rational-thinking
  python3 experiments/test_filled_system_scaffold.py
"""

import json
import random
import re
import string
import time
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
N = 50
SEED = 99  # different seed for a random subset


# ============================================================
# INFERENCE
# ============================================================


def query_ollama(prompt: str, system: str = None, max_tokens: int = 256) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0, "num_predict": max_tokens},
    }
    if system:
        payload["system"] = system

    try:
        resp = requests.post(f"{BASE_URL}/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except Exception as e:
        print(f"  ERROR: {e}")
        return ""


# ============================================================
# METRICS
# ============================================================


def f1_ext(prediction: str, gold_answers: list) -> float:
    extracted = best_span_extraction(prediction, gold_answers)
    best = 0.0
    for gold in gold_answers:
        f1 = _token_f1(extracted.split(), normalize_answer(gold).split())
        best = max(best, f1)
    return best


# ============================================================
# MAIN
# ============================================================


def main():
    print("Loading dataset...")
    dataset = build_dataset()

    # Random 50 questions (different from previous tests)
    random.seed(SEED)
    items = random.sample(dataset, N)
    print(f"Testing {len(items)} random questions with {MODEL}\n")

    scores = {
        "A_baseline": [],
        "B_passage_only": [],
        "C_user_scaffold_passage": [],
        "D_filled_as_user": [],
        "E_filled_as_system": [],
    }

    for i, item in enumerate(items):
        q = item["question"]
        passage = item["passage"]
        gold = item["gold_answers"]
        cid = item["class_id"]
        schema = get_answer_structure(cid)
        schema_str = json.dumps(schema, indent=2)

        # A) Baseline: question only
        pred = query_ollama(q)
        scores["A_baseline"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # B) Passage only: question + passage
        pred = query_ollama(f"Question: {q}\n\nContext: {passage}")
        scores["B_passage_only"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # C) User scaffold + passage (what we've been doing)
        scaffold_json = json.dumps({
            "question": q,
            "answer_structure": schema,
            "context_passage": passage,
        }, indent=2)
        pred = query_ollama(scaffold_json)
        scores["C_user_scaffold_passage"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # --- PASS 1: Extract into schema ---
        extraction_prompt = f"""Extract the answer to the question from the passage and fill in the schema fields.
Respond with ONLY the filled JSON, no other text.

Question: {q}

Passage: {passage}

Schema:
{schema_str}"""

        filled_schema = query_ollama(extraction_prompt, max_tokens=256)

        # D) Filled schema as user prompt (no passage in pass 2)
        gen_prompt_d = f"""Answer the question using the extracted information below. Respond concisely.

Question: {q}

Extracted:
{filled_schema}"""
        pred = query_ollama(gen_prompt_d)
        scores["D_filled_as_user"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
            "filled": filled_schema[:200],
        })

        # E) Filled schema as SYSTEM prompt, question as user (no passage in pass 2)
        system_msg = f"Use the following extracted information to answer the user's question. Respond concisely with just the answer.\n\n{filled_schema}"
        pred = query_ollama(q, system=system_msg)
        scores["E_filled_as_system"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # Progress
        if (i + 1) % 10 == 0:
            n = i + 1
            line = f"  [{n}/{N}]"
            for name in scores:
                avg_f1 = sum(r["f1"] for r in scores[name]) / n
                short = name[2:14]
                line += f"  {short}={avg_f1:.3f}"
            print(line)

    # Final summary
    print(f"\n{'='*70}")
    print(f"FINAL RESULTS (n={len(items)}, {MODEL}, random seed={SEED})")
    print(f"{'='*70}")
    print(f"{'Condition':<30s} {'EM_ext':>8s} {'F1_ext':>8s} {'Tokens':>8s}")
    print("-" * 60)

    for name, res in scores.items():
        n = len(res)
        avg_em = sum(r["em"] for r in res) / n
        avg_f1 = sum(r["f1"] for r in res) / n
        avg_tok = sum(r["tok"] for r in res) / n
        print(f"{name:<30s} {avg_em:>8.4f} {avg_f1:>8.4f} {avg_tok:>8.1f}")

    # Key comparisons
    print(f"\nKEY COMPARISONS (F1_ext):")
    n = len(items)
    a = sum(r["f1"] for r in scores["A_baseline"]) / n
    b = sum(r["f1"] for r in scores["B_passage_only"]) / n
    c = sum(r["f1"] for r in scores["C_user_scaffold_passage"]) / n
    d = sum(r["f1"] for r in scores["D_filled_as_user"]) / n
    e = sum(r["f1"] for r in scores["E_filled_as_system"]) / n

    print(f"  Passage only (B):              {b:.4f}")
    print(f"  User scaffold+passage (C):     {c:.4f} ({'BETTER' if c > b else 'worse'} than passage)")
    print(f"  Filled as user (D):            {d:.4f} ({'BETTER' if d > b else 'worse'} than passage)")
    print(f"  Filled as system (E):          {e:.4f} ({'BETTER' if e > b else 'worse'} than passage)")
    print(f"  Baseline no passage (A):       {a:.4f}")

    # Save
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "filled_system_scaffold_test.json"
    summary = {}
    for name, res in scores.items():
        n = len(res)
        summary[name] = {
            "n": n,
            "em_ext": round(sum(r["em"] for r in res) / n, 4),
            "f1_ext": round(sum(r["f1"] for r in res) / n, 4),
            "avg_tokens": round(sum(r["tok"] for r in res) / n, 1),
        }
    with open(output_path, "w") as f:
        json.dump({"model": MODEL, "n": len(items), "seed": SEED, "summary": summary}, f, indent=2)
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
