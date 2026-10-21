"""
Exploratory probe: does an explicit instruction to use the answer structure
change the schema's effect?

The main study supplied the answer-structure schema as context but never told the
model to use it. This probe adds an explicit instruction ("Use the following
answer structure to organize your response.") to the schema conditions and
compares against the same conditions without it, with and without the passage.

Conditions (all on the same 100-question subsample, llama3.2:3b):
  C1   question only                         (no structure; reference)
  C2   question + passage                    (reference)
  C3   question + matched schema             (schema, no instruction)
  C3i  question + instruction + matched schema
  C4   question + passage + matched schema
  C4i  question + passage + instruction + matched schema

The comparison of interest is C3i vs C3 and C4i vs C4: does the instruction make
the schema help where it did not before?

Setup:
  Ollama running locally with llama3.2:3b pulled.

Run (from the repository root):
  python3 exploratory/test_explicit_instruction.py
"""

import json
import sys
import time
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scaffold_builder import build_scaffold  # noqa: E402
from run_condition import (  # noqa: E402
    normalize_answer, _token_f1, best_span_extraction, exact_match_extracted,
)

MODEL = "llama3.2:3b"
BASE_URL = "http://localhost:11434"
SAMPLE_PATH = PROJECT_ROOT / "data" / "sample_1000.json"
RESULTS_DIR = Path(__file__).parent / "results"
N = 100
MAX_TOKENS = 512

INSTRUCTION = "Use the following answer structure to organize your response."


def query_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0, "num_predict": MAX_TOKENS},
    }
    try:
        resp = requests.post(f"{BASE_URL}/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except Exception as e:
        print(f"  ERROR: {e}")
        return ""


def f1_ext(prediction: str, gold_answers: list) -> float:
    extracted = best_span_extraction(prediction, gold_answers)
    return max(
        (_token_f1(extracted.split(), normalize_answer(g).split()) for g in gold_answers),
        default=0.0,
    )


def instructed(scaffold: str) -> str:
    """Prepend the explicit instruction to a scaffold prompt."""
    return f"{INSTRUCTION}\n\n{scaffold}"


def main():
    questions = json.load(open(SAMPLE_PATH))["questions"][:N]
    print(f"Explicit-instruction probe: {MODEL}, n={len(questions)}")
    print(f"6 conditions x {len(questions)} = {6 * len(questions)} calls\n")

    conds = ["C1", "C2", "C3", "C3i", "C4", "C4i"]
    scores = {c: [] for c in conds}

    for i, item in enumerate(questions):
        q, passage, gold, cid = (
            item["question"], item["passage"], item["gold_answers"], item["class_id"]
        )

        # Base scaffolds built by the shared builder, byte-identical to the main study.
        s_c1 = build_scaffold(question=q, condition=1)
        s_c2 = build_scaffold(question=q, condition=2, passage=passage)
        s_c3 = build_scaffold(question=q, condition=3, class_id=cid)
        s_c4 = build_scaffold(question=q, condition=4, passage=passage, class_id=cid)

        prompts = {
            "C1": s_c1,
            "C2": s_c2,
            "C3": s_c3,
            "C3i": instructed(s_c3),
            "C4": s_c4,
            "C4i": instructed(s_c4),
        }
        for c in conds:
            pred = query_ollama(prompts[c])
            scores[c].append({
                "em": exact_match_extracted(pred, gold),
                "f1": f1_ext(pred, gold),
                "tok": len(pred.split()),
            })

        if (i + 1) % 10 == 0:
            n = i + 1
            line = f"  [{n}/{N}]"
            for c in conds:
                line += f"  {c}={sum(r['f1'] for r in scores[c]) / n:.3f}"
            print(line)

    # Summary
    print(f"\n{'='*60}")
    print(f"FINAL (n={len(questions)}, {MODEL})")
    print(f"{'='*60}")
    print(f"{'Condition':<6s} {'EM_ext':>8s} {'F1_ext':>8s} {'Tokens':>8s}")
    print("-" * 34)
    summary = {}
    for c in conds:
        res = scores[c]
        n = len(res)
        summary[c] = {
            "n": n,
            "em_ext": round(sum(r["em"] for r in res) / n, 4),
            "f1_ext": round(sum(r["f1"] for r in res) / n, 4),
            "avg_tokens": round(sum(r["tok"] for r in res) / n, 1),
        }
        print(f"{c:<6s} {summary[c]['em_ext']:>8.4f} {summary[c]['f1_ext']:>8.4f} {summary[c]['avg_tokens']:>8.1f}")

    print(f"\nKEY COMPARISONS (F1_ext): does the instruction help the schema?")
    print(f"  C3  (schema)          {summary['C3']['f1_ext']:.4f}")
    print(f"  C3i (schema+instr)    {summary['C3i']['f1_ext']:.4f}  "
          f"delta {summary['C3i']['f1_ext'] - summary['C3']['f1_ext']:+.4f}")
    print(f"  C4  (pass+schema)     {summary['C4']['f1_ext']:.4f}")
    print(f"  C4i (pass+schema+ins) {summary['C4i']['f1_ext']:.4f}  "
          f"delta {summary['C4i']['f1_ext'] - summary['C4']['f1_ext']:+.4f}")
    print(f"  C1 baseline {summary['C1']['f1_ext']:.4f} | C2 passage {summary['C2']['f1_ext']:.4f}")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = RESULTS_DIR / "explicit_instruction_test.json"
    with open(out, "w") as f:
        json.dump({
            "model": MODEL, "n": len(questions), "instruction": INSTRUCTION,
            "summary": summary,
        }, f, indent=2)
    print(f"\nSaved to: {out}")


if __name__ == "__main__":
    main()
