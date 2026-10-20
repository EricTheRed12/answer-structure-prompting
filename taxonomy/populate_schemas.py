"""
Populate answer-structure schemas from the passage using the Anthropic API (Arm S).

Arm S tests whether the answer structure, when it CARRIES the content, is a form the
model can use as well as prose. Each schema's reasoning dimensions are filled with
content drawn FROM THE PASSAGE, and the gold answer is placed in a dedicated
`answer_value` field (the answer is its own field, per author decision).

At inference the model is given {question, filled schema} with NO raw passage, so the
information reaches it only through the structured schema. NOTE: because the fields are
passage-derived, this is a "restructured passage" test, not strictly context-free
(documented in finetuning-experiment-plan.md).

Design mirrors taxonomy_classification/classify_all.py (batching, resume, md-stripping).

Setup:
  pip install anthropic
  export ANTHROPIC_API_KEY="sk-ant-..."

Run (from the repository root):
  python3 taxonomy/populate_schemas.py            # both splits
  python3 taxonomy/populate_schemas.py --split eval   # just the eval sample

Outputs (experiments/finetune/):
  filled_train_pairs.jsonl   filled-schema pairs, training pool (excludes eval sample)
  filled_eval_pairs.jsonl    filled-schema pairs, the 1,000 eval sample
  filled_<split>_partial.json  progress checkpoints
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import anthropic

PROJECT_ROOT = Path(__file__).parent.parent
# scaffold_builder / eval_pipeline live in src/
sys.path.insert(0, str(PROJECT_ROOT / "src"))
from scaffold_builder import get_answer_structure  # noqa: E402
from eval_pipeline import map_to_class  # noqa: E402

ALL_RESULTS = PROJECT_ROOT / "taxonomy" / "all_results.json"
SAMPLE_1000 = PROJECT_ROOT / "data" / "sample_1000.json"
SQUAD = PROJECT_ROOT / "data" / "squad_dev.json"
OUT_DIR = PROJECT_ROOT / "study2_finetune"

MODEL = "claude-haiku-4-5-20251001"
BATCH_SIZE = 10          # smaller than classify: each item carries a passage
DELAY = 0.5

SYSTEM_PROMPT = """You populate an "answer structure" schema for a question, using ONLY the provided passage.

You are given, for each item: an ID, a question, the source passage, an empty JSON schema, and the GOLD ANSWER.

Your job:
1. Fill each EMPTY field in the schema with concise content drawn from the passage that fits that field's role. Use short phrases, not sentences. If the passage does not support a field, use an empty string "".
2. Do NOT change the pre-filled fields `answer_type` and `answer` (they are type hints, leave them as given).
3. Add a field `answer_value` set to the GOLD ANSWER exactly as provided. This is the answer as its own field.
4. Keep list-valued fields (e.g. `components`) as JSON arrays of short strings.

Populate the reasoning dimensions so the schema, on its own, carries the information needed to reach the answer. Do not invent facts not in the passage.

## Output Format
Return ONLY a JSON array. Each element:
{"id":"<id>","filled_schema":{<the populated schema object including answer_value>}}
No explanations, no markdown, just the raw JSON array."""


def load_squad() -> dict:
    data = json.load(open(SQUAD))
    out = {}
    for article in data["data"]:
        for para in article["paragraphs"]:
            for qa in para["qas"]:
                if qa.get("is_impossible", False):
                    continue
                answers = [a["text"] for a in qa.get("answers", [])]
                if answers:
                    out[qa["id"]] = {"passage": para["context"], "answers": answers,
                                     "question": qa["question"]}
    return out


def build_items(split: str):
    """Return list of items to populate: {id, question, passage, class_id, empty_schema, gold}."""
    squad = load_squad()
    all_items = json.load(open(ALL_RESULTS))
    eval_ids = {q["id"] for q in json.load(open(SAMPLE_1000))["questions"]}

    items = []
    seen = set()
    for it in all_items:
        qid = it["id"]
        if qid in seen or not it.get("question") or qid not in squad:
            continue
        in_eval = qid in eval_ids
        if split == "train" and in_eval:
            continue
        if split == "eval" and not in_eval:
            continue
        seen.add(qid)
        cid = map_to_class(it)
        gold = squad[qid]["answers"][0].strip()
        if not gold:
            continue
        items.append({
            "id": qid,
            "question": it["question"],
            "passage": squad[qid]["passage"],
            "class_id": cid,
            "empty_schema": get_answer_structure(cid),
            "gold": gold,
        })
    return items


def build_user_prompt(batch):
    lines = ["Populate the schema for each item using only its passage.\n"]
    for it in batch:
        lines.append(f'ID: {it["id"]}')
        lines.append(f'Q: {it["question"]}')
        lines.append(f'PASSAGE: {it["passage"]}')
        lines.append(f'EMPTY SCHEMA: {json.dumps(it["empty_schema"])}')
        lines.append(f'GOLD ANSWER: {it["gold"]}')
        lines.append("")
    return "\n".join(lines)


def parse_response(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


def partial_path(split):
    return OUT_DIR / f"filled_{split}_partial.json"


def out_path(split):
    return OUT_DIR / f"filled_{'train' if split=='train' else 'eval'}_pairs.jsonl"


def load_partial(split):
    p = partial_path(split)
    if p.exists():
        return json.load(open(p))
    return []


def run(split):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    items = build_items(split)
    print(f"[{split}] items to populate: {len(items)}")

    existing = load_partial(split)
    done_ids = {r["id"] for r in existing}
    remaining = [it for it in items if it["id"] not in done_ids]
    print(f"[{split}] already done: {len(existing)} | remaining: {len(remaining)}")

    client = anthropic.Anthropic()
    results = existing[:]
    errors = []
    total_batches = (len(remaining) + BATCH_SIZE - 1) // BATCH_SIZE

    for bi in range(0, len(remaining), BATCH_SIZE):
        batch = remaining[bi:bi + BATCH_SIZE]
        bn = bi // BATCH_SIZE + 1
        print(f"[{split}] batch {bn}/{total_batches} ({len(batch)})...", end=" ")
        try:
            resp = client.messages.create(
                model=MODEL, max_tokens=4096, system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": build_user_prompt(batch)}],
            )
            parsed = parse_response(resp.content[0].text)
            by_id = {it["id"]: it for it in batch}
            for r in parsed:
                qid = r.get("id")
                if qid not in by_id:
                    continue
                src = by_id[qid]
                filled = r.get("filled_schema", {})
                # Force correctness: answer_value must be the gold answer we supplied.
                filled["answer_value"] = src["gold"]
                results.append({
                    "id": qid,
                    "class_id": src["class_id"],
                    "question": src["question"],
                    "filled_schema": filled,
                    "target": src["gold"],
                })
            print(f"OK ({len(parsed)})")
        except json.JSONDecodeError as e:
            print(f"JSON ERROR: {e}")
            errors.append({"batch": bn, "error": str(e), "ids": [it["id"] for it in batch]})
        except anthropic.APIError as e:
            print(f"API ERROR: {e}")
            errors.append({"batch": bn, "error": str(e), "ids": [it["id"] for it in batch]})
            if "rate" in str(e).lower():
                time.sleep(30)

        if len(results) % 50 < BATCH_SIZE or bi + BATCH_SIZE >= len(remaining):
            json.dump(results, open(partial_path(split), "w"), indent=2)
        time.sleep(DELAY)

    # Write final pairs, building the scaffold `input` so the notebook can consume it directly.
    with open(out_path(split), "w") as f:
        for r in results:
            scaffold = json.dumps({"question": r["question"],
                                   "answer_structure": r["filled_schema"]}, indent=2)
            f.write(json.dumps({
                "id": r["id"], "class_id": r["class_id"], "question": r["question"],
                "input": scaffold, "target": r["target"], "condition": "S",
            }) + "\n")

    print(f"[{split}] DONE: {len(results)} pairs -> {out_path(split)}  errors={len(errors)}")
    if errors:
        json.dump(errors, open(OUT_DIR / f"filled_{split}_errors.json", "w"), indent=2)
        print(f"[{split}] errors saved; re-run to resume failed batches")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["train", "eval", "both"], default="both")
    args = ap.parse_args()
    splits = ["train", "eval"] if args.split == "both" else [args.split]
    for s in splits:
        run(s)


if __name__ == "__main__":
    main()
