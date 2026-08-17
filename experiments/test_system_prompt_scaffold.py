"""
Test: structure as system prompt vs structure in user prompt.

The hypothesis is that placing answer structure guidance in the SYSTEM prompt
(where the model treats it as instructions to follow) works better than
placing it in the USER prompt (where the model treats it as input to respond to).

Conditions:
  A) baseline: question only (no structure, no passage)
  B) baseline_passage: question + passage (no structure)
  C) user_scaffold: structure in user prompt (what we've been doing)
  D) system_scaffold: structure in system prompt, question as user prompt
  E) system_scaffold_passage: structure in system prompt, question + passage as user

Tests 200 questions on llama3:8b.

Usage:
  cd /Users/core/Documents/GradSchool/CS699/rational-thinking
  python3 experiments/test_system_prompt_scaffold.py
"""

import json
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

# Class ID → system prompt instruction derived from the schema
SYSTEM_PROMPTS = {
    1: "You are answering a question. The answer is a specific object, entity, document, technology, or substance. Respond with ONLY the answer, nothing else.",
    2: "You are answering a question. The answer identifies a person or abstract concept by their defining property. Respond with ONLY the answer, nothing else.",
    3: "You are answering a question. The answer requires multiple distinct components (a list). Respond with ONLY the answer, nothing else.",
    4: "You are answering a question. The answer is a specific number, count, or measurement. Respond with ONLY the answer, nothing else.",
    5: "You are answering a question. The answer is a time expression: a date, year, era, or duration. Respond with ONLY the answer, nothing else.",
    6: "You are answering a question. The answer is a geographic location or place name. Respond with ONLY the answer, nothing else.",
    7: "You are answering a question. The answer is who or what performed an action (the agent). Respond with ONLY the answer, nothing else.",
    8: "You are answering a question. The answer describes a quality, property, or characteristic. Respond with ONLY the answer, nothing else.",
    9: "You are answering a question. The answer explains why something happened (the cause or reason). Respond with ONLY the answer, nothing else.",
    10: "You are answering a question. The answer is the outcome, effect, or result of an action. Respond with ONLY the answer, nothing else.",
}


# ============================================================
# INFERENCE
# ============================================================


def query_ollama(prompt: str, system: str = None, max_tokens: int = 128) -> str:
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

    sample_path = Path(__file__).parent / "sample_1000.json"
    with open(sample_path) as f:
        sample_data = json.load(f)
    sample_ids = [q["id"] for q in sample_data["questions"][:200]]
    items = [d for d in dataset if d["id"] in sample_ids][:200]
    print(f"Testing {len(items)} questions with {MODEL}")
    print(f"5 conditions × {len(items)} = {5 * len(items)} API calls\n")

    scores = {
        "A_baseline": [],
        "B_baseline_passage": [],
        "C_user_scaffold": [],
        "D_system_scaffold": [],
        "E_system_scaffold_passage": [],
    }

    for i, item in enumerate(items):
        q = item["question"]
        passage = item["passage"]
        gold = item["gold_answers"]
        cid = item["class_id"]
        schema = get_answer_structure(cid)
        sys_prompt = SYSTEM_PROMPTS.get(cid, "Respond with ONLY the answer, nothing else.")

        # A) Baseline: question only
        pred = query_ollama(q)
        scores["A_baseline"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # B) Baseline + passage
        pred = query_ollama(f"Question: {q}\n\nContext: {passage}")
        scores["B_baseline_passage"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # C) User scaffold (what we've been doing)
        scaffold_json = json.dumps({"question": q, "answer_structure": schema}, indent=2)
        pred = query_ollama(scaffold_json)
        scores["C_user_scaffold"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # D) System scaffold: structure as system prompt
        pred = query_ollama(q, system=sys_prompt)
        scores["D_system_scaffold"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # E) System scaffold + passage
        pred = query_ollama(
            f"Question: {q}\n\nContext: {passage}",
            system=sys_prompt,
        )
        scores["E_system_scaffold_passage"].append({
            "em": exact_match_extracted(pred, gold),
            "f1": f1_ext(pred, gold),
            "tok": len(pred.split()),
        })

        # Progress
        if (i + 1) % 10 == 0:
            n = i + 1
            line = f"  [{n}/200]"
            for name in scores:
                avg_f1 = sum(r["f1"] for r in scores[name]) / n
                short = name.split("_", 1)[1][:12]
                line += f"  {short}={avg_f1:.3f}"
            print(line)

    # Final summary
    print(f"\n{'='*70}")
    print(f"FINAL RESULTS (n={len(items)}, {MODEL})")
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
    print(f"\nKEY COMPARISONS:")
    n = len(items)
    a_f1 = sum(r["f1"] for r in scores["A_baseline"]) / n
    b_f1 = sum(r["f1"] for r in scores["B_baseline_passage"]) / n
    c_f1 = sum(r["f1"] for r in scores["C_user_scaffold"]) / n
    d_f1 = sum(r["f1"] for r in scores["D_system_scaffold"]) / n
    e_f1 = sum(r["f1"] for r in scores["E_system_scaffold_passage"]) / n

    print(f"  System scaffold vs baseline (no passage): D={d_f1:.4f} vs A={a_f1:.4f} ({'BETTER' if d_f1 > a_f1 else 'worse'})")
    print(f"  System scaffold vs user scaffold:         D={d_f1:.4f} vs C={c_f1:.4f} ({'BETTER' if d_f1 > c_f1 else 'worse'})")
    print(f"  System+passage vs passage only:           E={e_f1:.4f} vs B={b_f1:.4f} ({'BETTER' if e_f1 > b_f1 else 'worse'})")

    # Save
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "system_prompt_scaffold_test.json"
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
        json.dump({"model": MODEL, "n": len(items), "summary": summary, "scores": scores}, f, indent=2)
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
