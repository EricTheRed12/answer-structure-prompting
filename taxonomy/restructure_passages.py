"""
Restructure SQuAD passages into organized prose (Meaning 2 / V7 fair test).

Purpose: test paragraph vs STRUCTURED PROSE while holding CONTENT constant. The
structured passage is the RAW passage rewritten into organized, labeled statements
that preserve ALL information, WITHOUT summarizing, omitting, or answering anything.

LEAK-PROOF BY CONSTRUCTION: Claude is given ONLY the passage text. It never sees the
question or the gold answer, so it cannot pre-extract or pre-locate the answer. The
answer stays embedded in the reorganized prose exactly as hard to find as in the
original — only the organization changes. Any accuracy difference vs the paragraph is
therefore attributable to FORM, not content.

Scope: only the passages needed for the 1,000-question eval sample. Passages are shared
across questions, so we restructure each UNIQUE passage once and map back by passage text.

This is an inference-time delivery-form test on the UNTUNED model only (do not use for
training; the fine-tuning arms trained no-passage).

Setup:
  pip install anthropic
  export ANTHROPIC_API_KEY="sk-ant-..."

Run (from the repository root):
  python3 taxonomy/restructure_passages.py

Output (experiments/finetune/):
  restructured_passages.json   {passage_hash: {"original": ..., "structured": ...}}
  restructured_passages_partial.json   progress checkpoint
"""

import hashlib
import json
import os
import time
from pathlib import Path

import anthropic

PROJECT_ROOT = Path(__file__).parent.parent
SAMPLE_1000 = PROJECT_ROOT / "data" / "sample_1000.json"
OUT_DIR = PROJECT_ROOT / "study2_finetune"
OUT_FILE = OUT_DIR / "restructured_passages.json"
PARTIAL_FILE = OUT_DIR / "restructured_passages_partial.json"

MODEL = "claude-haiku-4-5-20251001"
DELAY = 0.4

# NOTE: no question, no answer in the prompt. Passage only.
SYSTEM_PROMPT = """You reorganize a passage of text into a structured, labeled form.

You are given ONLY a passage. Rewrite it as a sequence of short labeled statements that
organize its content (for example: Subject, Time, Origin, Cause, Sequence, Outcome, or
whatever labels fit the passage's content).

Strict rules:
1. PRESERVE ALL INFORMATION in the passage. Do not summarize, shorten, generalize, or omit any fact, name, number, date, or detail.
2. Do NOT add information that is not in the passage.
3. Do NOT answer any question or highlight any fact as an "answer" — you are not told what will be asked. Treat every fact as equally important.
4. Keep the original wording of facts where possible; you are reorganizing, not paraphrasing away detail.

Return ONLY the reorganized text as labeled lines. No preamble, no explanation."""


def passage_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def load_unique_passages():
    sample = json.load(open(SAMPLE_1000))["questions"]
    uniq = {}
    for q in sample:
        p = q["passage"]
        h = passage_hash(p)
        if h not in uniq:
            uniq[h] = p
    return uniq


def load_partial():
    if PARTIAL_FILE.exists():
        return json.load(open(PARTIAL_FILE))
    return {}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    uniq = load_unique_passages()
    print(f"unique passages to restructure: {len(uniq)}")

    results = load_partial()
    done = set(results.keys())
    todo = [(h, p) for h, p in uniq.items() if h not in done]
    print(f"already done: {len(done)} | remaining: {len(todo)}")

    client = anthropic.Anthropic()
    errors = []

    for i, (h, passage) in enumerate(todo):
        try:
            resp = client.messages.create(
                model=MODEL, max_tokens=2048, system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": passage}],
            )
            structured = resp.content[0].text.strip()
            results[h] = {"original": passage, "structured": structured}
            if (i + 1) % 25 == 0:
                print(f"  [{i+1}/{len(todo)}] restructured")
        except anthropic.APIError as e:
            print(f"  API ERROR on {h[:8]}: {e}")
            errors.append({"hash": h, "error": str(e)})
            if "rate" in str(e).lower():
                time.sleep(30)

        if (i + 1) % 25 == 0 or i + 1 == len(todo):
            json.dump(results, open(PARTIAL_FILE, "w"), indent=2)
        time.sleep(DELAY)

    json.dump(results, open(OUT_FILE, "w"), indent=2)
    print(f"\nDONE: {len(results)} passages -> {OUT_FILE}  errors={len(errors)}")

    # Leak sanity check: warn if a structured passage looks suspiciously short vs original
    short = sum(1 for v in results.values() if len(v["structured"]) < 0.4 * len(v["original"]))
    print(f"passages where structured < 40% of original length (possible info loss): {short}")
    if errors:
        json.dump(errors, open(OUT_DIR / "restructured_passages_errors.json", "w"), indent=2)
        print("errors saved; re-run to resume")


if __name__ == "__main__":
    main()
