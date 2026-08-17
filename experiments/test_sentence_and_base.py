"""
Test: Sentence-based scaffold + smaller model + base model.

Three scaffold formats:
  - flat: "answer: single, agent, action_performed, object_of_action"
  - sentence: "The interrogative is who. The answer is a single agent.
               Identify the agent, the action performed, and the object of action."
  - json: original JSON schema (control)

Three models:
  - llama3.2:1b (small instruct — might benefit more from structure)
  - llama3:8b (large instruct — our main model)
  - llama3:text (8B base — no chat template, no instruction tuning)

50 random questions, with and without passage.

Usage:
  cd /Users/core/Documents/GradSchool/CS699/rational-thinking
  python3 experiments/test_sentence_and_base.py
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

BASE_URL = "http://localhost:11434"
RESULTS_DIR = Path(__file__).parent / "results"
N = 50
SEED = 123

MODELS = ["llama3.2:1b", "llama3:8b", "llama3:text"]

# ============================================================
# SCAFFOLD FORMATS
# ============================================================

# Flat keywords
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

# Sentence-based scaffold (standardized sentences describing the structure)
SENTENCE_SCAFFOLDS = {
    1: "The answer is a single item. It identifies a specific object, entity, or thing. Provide the object and its relation.",
    2: "The answer is a single item. It identifies a person or concept by a defining property. Provide the identity and defining property.",
    3: "The answer requires multiple parts. It is a list of components that share a category. Provide all components.",
    4: "The answer is a single quantity. It is a number with a unit in a measurement context. Provide the quantity and unit.",
    5: "The answer is a single time expression. It relates to an event. Provide the time expression and temporal type.",
    6: "The answer is a single location. It is a geographic place. Provide the location and its relation.",
    7: "The answer is a single agent. It is who or what performed an action. Provide the agent, the action performed, and the object of action.",
    8: "The answer is a single quality. It describes a property or characteristic. Provide the quality and description domain.",
    9: "The answer is a single cause. It explains why something happened. Provide the cause, the effect, and the mechanism.",
    10: "The answer is a single outcome. It is the result of an action. Provide the outcome, the action, and the actor.",
}


# ============================================================
# INFERENCE
# ============================================================


def query_ollama(prompt: str, model: str, system: str = None, raw: bool = False, max_tokens: int = 256) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0, "num_predict": max_tokens},
    }
    if system:
        payload["system"] = system
    if raw:
        payload["raw"] = True

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


def run_model(model: str, items: list, use_raw: bool = False):
    """Run all conditions for one model."""
    is_base = (model == "llama3:text")
    model_label = model.replace(":", "_").replace(".", "")

    scores = {
        "baseline": [],
        "passage": [],
        "flat": [],
        "flat_passage": [],
        "sentence": [],
        "sentence_passage": [],
    }

    for i, item in enumerate(items):
        q = item["question"]
        passage = item["passage"]
        gold = item["gold_answers"]
        cid = item["class_id"]
        flat = FLAT_KEYWORDS.get(cid, "answer: single")
        sent = SENTENCE_SCAFFOLDS.get(cid, "Answer the question.")

        # For base model, use raw mode and format as completion prompts
        if is_base:
            # Baseline
            prompt = f"Q: {q}\nA:"
            pred = query_ollama(prompt, model, raw=True, max_tokens=64)

            # Take only first line/sentence
            pred = pred.split("\n")[0].strip()
            scores["baseline"].append({"em": exact_match_extracted(pred, gold), "f1": f1_ext(pred, gold), "tok": len(pred.split())})

            # Passage
            prompt = f"Context: {passage}\n\nQ: {q}\nA:"
            pred = query_ollama(prompt, model, raw=True, max_tokens=64)
            pred = pred.split("\n")[0].strip()
            scores["passage"].append({"em": exact_match_extracted(pred, gold), "f1": f1_ext(pred, gold), "tok": len(pred.split())})

            # Flat
            prompt = f"{flat}\n\nQ: {q}\nA:"
            pred = query_ollama(prompt, model, raw=True, max_tokens=64)
            pred = pred.split("\n")[0].strip()
            scores["flat"].append({"em": exact_match_extracted(pred, gold), "f1": f1_ext(pred, gold), "tok": len(pred.split())})

            # Flat + passage
            prompt = f"{flat}\n\nContext: {passage}\n\nQ: {q}\nA:"
            pred = query_ollama(prompt, model, raw=True, max_tokens=64)
            pred = pred.split("\n")[0].strip()
            scores["flat_passage"].append({"em": exact_match_extracted(pred, gold), "f1": f1_ext(pred, gold), "tok": len(pred.split())})

            # Sentence
            prompt = f"{sent}\n\nQ: {q}\nA:"
            pred = query_ollama(prompt, model, raw=True, max_tokens=64)
            pred = pred.split("\n")[0].strip()
            scores["sentence"].append({"em": exact_match_extracted(pred, gold), "f1": f1_ext(pred, gold), "tok": len(pred.split())})

            # Sentence + passage
            prompt = f"{sent}\n\nContext: {passage}\n\nQ: {q}\nA:"
            pred = query_ollama(prompt, model, raw=True, max_tokens=64)
            pred = pred.split("\n")[0].strip()
            scores["sentence_passage"].append({"em": exact_match_extracted(pred, gold), "f1": f1_ext(pred, gold), "tok": len(pred.split())})

        else:
            # Instruct models — use normal prompting
            # Baseline
            pred = query_ollama(q, model)
            scores["baseline"].append({"em": exact_match_extracted(pred, gold), "f1": f1_ext(pred, gold), "tok": len(pred.split())})

            # Passage
            pred = query_ollama(f"Question: {q}\n\nContext: {passage}", model)
            scores["passage"].append({"em": exact_match_extracted(pred, gold), "f1": f1_ext(pred, gold), "tok": len(pred.split())})

            # Flat
            pred = query_ollama(f"Question: {q}\n{flat}", model)
            scores["flat"].append({"em": exact_match_extracted(pred, gold), "f1": f1_ext(pred, gold), "tok": len(pred.split())})

            # Flat + passage
            pred = query_ollama(f"Question: {q}\n{flat}\n\nContext: {passage}", model)
            scores["flat_passage"].append({"em": exact_match_extracted(pred, gold), "f1": f1_ext(pred, gold), "tok": len(pred.split())})

            # Sentence
            pred = query_ollama(f"Question: {q}\n\n{sent}", model)
            scores["sentence"].append({"em": exact_match_extracted(pred, gold), "f1": f1_ext(pred, gold), "tok": len(pred.split())})

            # Sentence + passage
            pred = query_ollama(f"Question: {q}\n\n{sent}\n\nContext: {passage}", model)
            scores["sentence_passage"].append({"em": exact_match_extracted(pred, gold), "f1": f1_ext(pred, gold), "tok": len(pred.split())})

        # Progress
        if (i + 1) % 10 == 0:
            n = i + 1
            line = f"  [{n}/{N}]"
            for name in scores:
                avg_f1 = sum(r["f1"] for r in scores[name]) / n
                line += f"  {name[:8]}={avg_f1:.3f}"
            print(line)

    return scores


def main():
    print("Loading dataset...")
    dataset = build_dataset()

    random.seed(SEED)
    items = random.sample(dataset, N)
    print(f"Testing {len(items)} random questions (seed={SEED})")
    print(f"3 models × 6 conditions × {N} = {3 * 6 * N} API calls\n")

    all_results = {}

    for model in MODELS:
        is_base = (model == "llama3:text")
        print(f"\n{'='*70}")
        print(f"MODEL: {model} {'(BASE - raw mode)' if is_base else '(instruct)'}")
        print(f"{'='*70}")

        scores = run_model(model, items, use_raw=is_base)
        all_results[model] = scores

        # Print summary for this model
        print(f"\n  {'Condition':<20s} {'EM_ext':>8s} {'F1_ext':>8s} {'Tokens':>8s}")
        print(f"  {'-'*50}")
        for name, res in scores.items():
            n = len(res)
            avg_em = sum(r["em"] for r in res) / n
            avg_f1 = sum(r["f1"] for r in res) / n
            avg_tok = sum(r["tok"] for r in res) / n
            print(f"  {name:<20s} {avg_em:>8.4f} {avg_f1:>8.4f} {avg_tok:>8.1f}")

    # Cross-model comparison
    print(f"\n\n{'='*70}")
    print(f"CROSS-MODEL COMPARISON (F1_ext)")
    print(f"{'='*70}")
    print(f"{'Condition':<20s}", end="")
    for model in MODELS:
        print(f" {model:>14s}", end="")
    print()
    print("-" * 65)

    for cond in ["baseline", "passage", "flat", "flat_passage", "sentence", "sentence_passage"]:
        print(f"{cond:<20s}", end="")
        for model in MODELS:
            scores = all_results[model]
            n = len(scores[cond])
            avg_f1 = sum(r["f1"] for r in scores[cond]) / n
            print(f" {avg_f1:>14.4f}", end="")
        print()

    # Does scaffold help MORE on smaller/base models?
    print(f"\n{'='*70}")
    print(f"SCAFFOLD DELTA (scaffold - baseline, no passage)")
    print(f"{'='*70}")
    print(f"{'Model':<15s} {'flat-base':>10s} {'sent-base':>10s}")
    print("-" * 40)
    for model in MODELS:
        s = all_results[model]
        n = N
        base_f1 = sum(r["f1"] for r in s["baseline"]) / n
        flat_f1 = sum(r["f1"] for r in s["flat"]) / n
        sent_f1 = sum(r["f1"] for r in s["sentence"]) / n
        d_flat = flat_f1 - base_f1
        d_sent = sent_f1 - base_f1
        print(f"{model:<15s} {d_flat:>+10.4f} {d_sent:>+10.4f}")

    # Save
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "sentence_and_base_test.json"
    summary = {}
    for model in MODELS:
        summary[model] = {}
        for cond, res in all_results[model].items():
            n = len(res)
            summary[model][cond] = {
                "n": n,
                "em_ext": round(sum(r["em"] for r in res) / n, 4),
                "f1_ext": round(sum(r["f1"] for r in res) / n, 4),
                "avg_tokens": round(sum(r["tok"] for r in res) / n, 1),
            }
    with open(output_path, "w") as f:
        json.dump({"models": MODELS, "n": N, "seed": SEED, "summary": summary}, f, indent=2)
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
