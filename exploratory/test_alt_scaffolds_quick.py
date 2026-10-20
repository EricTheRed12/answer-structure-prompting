"""
Quick test: 4 scaffold formats × 50 questions, no passage, llama3:8b.
Then 4 × 50 with passage.
Prints results incrementally.
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

NL_HINTS = {
    1: "Answer with the name of the specific object, entity, or thing.",
    2: "Answer with the person or concept identified by their defining property.",
    3: "Answer with a list of the multiple components.",
    4: "Answer with the specific number or measurement.",
    5: "Answer with the date, year, or time period.",
    6: "Answer with the specific place or location.",
    7: "Answer with who or what performed the action.",
    8: "Answer with the quality or characteristic being described.",
    9: "Answer with the cause or reason why.",
    10: "Answer with the outcome or result.",
}


def query_ollama(prompt, model="llama3:8b"):
    try:
        resp = requests.post("http://localhost:11434/api/generate", json={
            "model": model, "prompt": prompt, "stream": False,
            "options": {"temperature": 0, "num_predict": 512}
        }, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except:
        return ""


def f1_ext(prediction, gold_answers):
    extracted = best_span_extraction(prediction, gold_answers)
    best = 0.0
    for gold in gold_answers:
        f1 = _token_f1(extracted.split(), normalize_answer(gold).split())
        best = max(best, f1)
    return best


def main():
    print("Loading data...")
    dataset = build_dataset()
    with open(Path(__file__).parent / "sample_1000.json") as f:
        sample = json.load(f)
    ids = [q["id"] for q in sample["questions"][:50]]
    items = [d for d in dataset if d["id"] in ids][:50]
    print(f"Running 4 formats × {len(items)} questions\n")

    # ---- NO PASSAGE ----
    print("=" * 60)
    print("WITHOUT PASSAGE")
    print("=" * 60)

    scores = {"baseline": [], "json": [], "nl_hint": [], "instr_json": []}

    for i, item in enumerate(items):
        q = item["question"]
        cid = item["class_id"]
        gold = item["gold_answers"]
        schema = get_answer_structure(cid)

        prompts = {
            "baseline": q,
            "json": json.dumps({"question": q, "answer_structure": schema}, indent=2),
            "nl_hint": f"Question: {q}\n\n{NL_HINTS.get(cid, 'Answer concisely.')}",
            "instr_json": f"Use the following answer structure to guide your response. Respond with only the answer, no explanation.\n\n{json.dumps({'question': q, 'answer_structure': schema}, indent=2)}",
        }

        for name, prompt in prompts.items():
            pred = query_ollama(prompt)
            em = exact_match_extracted(pred, gold)
            f1 = f1_ext(pred, gold)
            scores[name].append({"em": em, "f1": f1, "tok": len(pred.split())})

        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/50]", end="")
            for name in scores:
                avg_f1 = sum(r["f1"] for r in scores[name]) / len(scores[name])
                print(f"  {name}={avg_f1:.3f}", end="")
            print()

    print(f"\n{'Format':<20s} {'EM_ext':>8s} {'F1_ext':>8s} {'Tokens':>8s}")
    print("-" * 45)
    for name, res in scores.items():
        n = len(res)
        print(f"{name:<20s} {sum(r['em'] for r in res)/n:>8.4f} {sum(r['f1'] for r in res)/n:>8.4f} {sum(r['tok'] for r in res)/n:>8.1f}")

    # ---- WITH PASSAGE ----
    print(f"\n{'=' * 60}")
    print("WITH PASSAGE")
    print("=" * 60)

    scores_p = {"baseline": [], "json": [], "nl_hint": [], "instr_json": []}

    for i, item in enumerate(items):
        q = item["question"]
        cid = item["class_id"]
        gold = item["gold_answers"]
        passage = item["passage"]
        schema = get_answer_structure(cid)

        prompts = {
            "baseline": f"Question: {q}\n\nContext: {passage}",
            "json": json.dumps({"question": q, "answer_structure": schema, "context_passage": passage}, indent=2),
            "nl_hint": f"Question: {q}\n\nContext: {passage}\n\n{NL_HINTS.get(cid, 'Answer concisely.')}",
            "instr_json": f"Use the following answer structure to guide your response. Respond with only the answer, no explanation.\n\n{json.dumps({'question': q, 'answer_structure': schema, 'context_passage': passage}, indent=2)}",
        }

        for name, prompt in prompts.items():
            pred = query_ollama(prompt)
            em = exact_match_extracted(pred, gold)
            f1 = f1_ext(pred, gold)
            scores_p[name].append({"em": em, "f1": f1, "tok": len(pred.split())})

        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/50]", end="")
            for name in scores_p:
                avg_f1 = sum(r["f1"] for r in scores_p[name]) / len(scores_p[name])
                print(f"  {name}={avg_f1:.3f}", end="")
            print()

    print(f"\n{'Format':<20s} {'EM_ext':>8s} {'F1_ext':>8s} {'Tokens':>8s}")
    print("-" * 45)
    for name, res in scores_p.items():
        n = len(res)
        print(f"{name:<20s} {sum(r['em'] for r in res)/n:>8.4f} {sum(r['f1'] for r in res)/n:>8.4f} {sum(r['tok'] for r in res)/n:>8.1f}")


if __name__ == "__main__":
    main()
