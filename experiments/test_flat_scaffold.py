"""
Test: Flat scaffold — schema field names as plain keywords, no JSON structure.

Conditions:
  A) baseline: question only
  B) passage_only: question + passage
  C) json_scaffold: full JSON schema in user prompt (what we've been doing)
  D) flat_scaffold: field names as keywords appended to question
  E) flat_scaffold_passage: flat keywords + passage
  F) flat_system: flat keywords in system prompt, question as user
  G) flat_system_passage: flat keywords in system, question + passage as user

50 random questions, llama3:8b.

Usage:
  cd /Users/core/Documents/GradSchool/CS699/rational-thinking
  python3 experiments/test_flat_scaffold.py
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
SEED = 77


# ============================================================
# FLAT SCAFFOLD BUILDERS
# ============================================================

# Class ID → flat keyword string (schema fields without JSON syntax)
FLAT_KEYWORDS = {
    1: "answer: single, object, relation",
    2: "answer: single, concept or person, identity, defining_property",
    3: "answer: multiple, list, components, shared_category",
    4: "answer: single, quantity, unit, measurement_context",
    5: "answer: single, time, event, time_expression, temporal_type",
    6: "answer: single, location, relation",
    7: "answer: single, agent, action_performed, object_of_action",
    8: "answer: single, quality, description_domain",
    9: "answer: single, cause, effect, mechanism",
    10: "answer: single, outcome, action, actor",
}


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

    random.seed(SEED)
    items = random.sample(dataset, N)
    print(f"Testing {len(items)} random questions with {MODEL}")
    print(f"7 conditions × {len(items)} = {7 * len(items)} API calls\n")

    scores = {
        "A_baseline": [],
        "B_passage_only": [],
        "C_json_scaffold": [],
        "D_flat_scaffold": [],
        "E_flat_scaffold_passage": [],
        "F_flat_system": [],
        "G_flat_system_passage": [],
    }

    for i, item in enumerate(items):
        q = item["question"]
        passage = item["passage"]
        gold = item["gold_answers"]
        cid = item["class_id"]
        schema = get_answer_structure(cid)
        flat = FLAT_KEYWORDS.get(cid, "answer: single")

        # A) Baseline
        pred = query_ollama(q)
        scores["A_baseline"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # B) Passage only
        pred = query_ollama(f"Question: {q}\n\nContext: {passage}")
        scores["B_passage_only"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # C) JSON scaffold + passage (original approach)
        scaffold_json = json.dumps({
            "question": q,
            "answer_structure": schema,
            "context_passage": passage,
        }, indent=2)
        pred = query_ollama(scaffold_json)
        scores["C_json_scaffold"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # D) Flat scaffold, no passage
        pred = query_ollama(f"Question: {q}\n{flat}")
        scores["D_flat_scaffold"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # E) Flat scaffold + passage
        pred = query_ollama(f"Question: {q}\n{flat}\n\nContext: {passage}")
        scores["E_flat_scaffold_passage"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # F) Flat in system prompt, question as user
        pred = query_ollama(q, system=f"Answer structure: {flat}")
        scores["F_flat_system"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # G) Flat in system prompt, question + passage as user
        pred = query_ollama(
            f"Question: {q}\n\nContext: {passage}",
            system=f"Answer structure: {flat}",
        )
        scores["G_flat_system_passage"].append({
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
    print(f"FINAL RESULTS (n={len(items)}, {MODEL}, seed={SEED})")
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
    vals = {name: sum(r["f1"] for r in res) / n for name, res in scores.items()}

    b = vals["B_passage_only"]
    print(f"  Passage only (B):              {b:.4f} [REFERENCE]")
    print(f"  JSON scaffold+passage (C):     {vals['C_json_scaffold']:.4f}  {'BETTER' if vals['C_json_scaffold'] > b else 'worse'}")
    print(f"  Flat+passage user (E):         {vals['E_flat_scaffold_passage']:.4f}  {'BETTER' if vals['E_flat_scaffold_passage'] > b else 'worse'}")
    print(f"  Flat+passage system (G):       {vals['G_flat_system_passage']:.4f}  {'BETTER' if vals['G_flat_system_passage'] > b else 'worse'}")
    print()
    a = vals["A_baseline"]
    print(f"  Baseline no passage (A):       {a:.4f} [REFERENCE]")
    print(f"  Flat scaffold (D):             {vals['D_flat_scaffold']:.4f}  {'BETTER' if vals['D_flat_scaffold'] > a else 'worse'}")
    print(f"  Flat system (F):               {vals['F_flat_system']:.4f}  {'BETTER' if vals['F_flat_system'] > a else 'worse'}")

    # Save
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "flat_scaffold_test.json"
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
