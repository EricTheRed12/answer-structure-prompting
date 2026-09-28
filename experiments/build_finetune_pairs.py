"""
Build fine-tuning training data for the multi-arm answer-structure experiment (Task 2).

A training example is (input, target):
  input  = a scaffold JSON built by scaffold_builder.build_scaffold (byte-identical to eval)
  target = the gold answer string
NO passage in any training arm here (Arm S / filled-schema is built by a separate
Claude pipeline).

Arms (each gets its own train/val files; the notebook trains one LoRA adapter per arm):

  Arm 1  "empty-schema format"     mix of C1 (question only) and C3 (question + empty
                                    matched schema). Does the bare matched schema help
                                    once the QA format is learned? Trained analog of the
                                    main study.
  Arm 2  "schema-sensitivity"      each question appears TWICE: once C3 (matched empty
                                    schema) and once C5 (mismatched empty schema), SAME
                                    target. Forces the model to attend to which schema it
                                    got. Eval C3 vs C5 = the merit test.
  Arm 4  "answer-only control"     C1 only (question -> answer, no schema). Floor: how far
                                    does adapting the base model to terse QA get with no
                                    structure at all.

Common source record: (id, class_id, question, target). Each arm derives its `input`
from that via build_scaffold with the appropriate condition.

Leakage control: the 1,000-question eval sample (sample_1000.json) is EXCLUDED from all
training arms. Eval is built on the fly in the notebook from sample_1000.json.

Outputs (experiments/finetune/):
  arm1_train.jsonl / arm1_val.jsonl
  arm2_train.jsonl / arm2_val.jsonl
  arm4_train.jsonl / arm4_val.jsonl
  train_pairs.jsonl / val_pairs.jsonl   (kept: the plain C3 empty-schema pairs, == Arm 1's C3 half)
  eval_pairs.jsonl                       (reference: eval sample as C3 pairs)
  build_manifest.json

Run:
  cd /Users/core/Documents/GradSchool/CS699/rational-thinking
  python3 experiments/build_finetune_pairs.py
"""

import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from scaffold_builder import build_scaffold  # noqa: E402
from eval_pipeline import map_to_class  # noqa: E402

PROJECT_ROOT = Path(__file__).parent.parent
ALL_RESULTS = PROJECT_ROOT / "taxonomy_classification" / "all_results.json"
SAMPLE_1000 = PROJECT_ROOT / "experiments" / "sample_1000.json"
SQUAD = PROJECT_ROOT / "squad_dev.json"
OUT_DIR = PROJECT_ROOT / "experiments" / "finetune"

VAL_FRACTION = 0.1
SEED = 42
# Fixed seed base for mismatched-schema selection so builds are reproducible.
RANDOM_SCHEMA_SEED = 1000


def load_squad_gold() -> dict:
    data = json.load(open(SQUAD))
    gold = {}
    for article in data["data"]:
        for para in article["paragraphs"]:
            for qa in para["qas"]:
                if qa.get("is_impossible", False):
                    continue
                answers = [a["text"] for a in qa.get("answers", [])]
                if answers:
                    gold[qa["id"]] = answers
    return gold


def target_answer(item: dict, squad_gold: dict) -> str:
    qid = item["id"]
    if qid in squad_gold and squad_gold[qid]:
        return squad_gold[qid][0].strip()
    return str(item.get("answer", "")).strip()


def source_records(items, squad_gold):
    """Canonical (id, class_id, question, target) records; drops empties."""
    recs = []
    dropped = 0
    for it in items:
        if not it.get("question"):
            dropped += 1
            continue
        tgt = target_answer(it, squad_gold)
        if not tgt:
            dropped += 1
            continue
        recs.append({
            "id": it["id"],
            "class_id": map_to_class(it),
            "question": it["question"],
            "target": tgt,
        })
    return recs, dropped


# ---- per-arm input construction ----

def pair_c1(rec):
    """Question only (C1)."""
    return {**rec, "condition": 1,
            "input": build_scaffold(rec["question"], condition=1)}


def pair_c3(rec):
    """Question + empty matched schema (C3)."""
    return {**rec, "condition": 3,
            "input": build_scaffold(rec["question"], condition=3, class_id=rec["class_id"])}


def pair_c5(rec, idx):
    """Question + empty mismatched schema (C5), reproducible via seed."""
    return {**rec, "condition": 5,
            "input": build_scaffold(rec["question"], condition=5,
                                    class_id=rec["class_id"],
                                    random_seed=RANDOM_SCHEMA_SEED + idx)}


def arm1_pairs(recs):
    """Mix C1 and C3 for every record."""
    out = []
    for r in recs:
        out.append(pair_c1(r))
        out.append(pair_c3(r))
    return out


def arm2_pairs(recs):
    """Each record appears as C3 (matched) and C5 (mismatched), same target."""
    out = []
    for i, r in enumerate(recs):
        out.append(pair_c3(r))
        out.append(pair_c5(r, i))
    return out


def arm4_pairs(recs):
    """C1 only."""
    return [pair_c1(r) for r in recs]


# ---- splitting / io ----

def stratified_split_records(recs, val_fraction, seed):
    """Split canonical records into (train, val), stratified by class_id.
    Splitting at the RECORD level (not pair level) guarantees a question's
    variants never straddle the train/val boundary."""
    rng = random.Random(seed)
    by_class = defaultdict(list)
    for r in recs:
        by_class[r["class_id"]].append(r)
    train, val = [], []
    for cid, items in by_class.items():
        items = items[:]
        rng.shuffle(items)
        n_val = max(1, int(round(len(items) * val_fraction))) if len(items) > 1 else 0
        val.extend(items[:n_val])
        train.extend(items[n_val:])
    rng.shuffle(train)
    rng.shuffle(val)
    return train, val


def write_jsonl(path, rows):
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    all_items = json.load(open(ALL_RESULTS))
    squad_gold = load_squad_gold()
    sample = json.load(open(SAMPLE_1000))
    eval_ids = {q["id"] for q in sample["questions"]}

    train_pool_items = [it for it in all_items if it["id"] not in eval_ids]
    eval_items = [it for it in all_items if it["id"] in eval_ids]

    train_recs, dropped_train = source_records(train_pool_items, squad_gold)
    eval_recs, dropped_eval = source_records(eval_items, squad_gold)

    # dedupe eval by id
    seen, deduped = set(), []
    for r in eval_recs:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        deduped.append(r)
    eval_recs = deduped

    # Split canonical records once; every arm uses the same train/val partition.
    train_split, val_split = stratified_split_records(train_recs, VAL_FRACTION, SEED)

    # Build each arm from the shared split.
    arms = {
        "arm1": (arm1_pairs(train_split), arm1_pairs(val_split)),
        "arm2": (arm2_pairs(train_split), arm2_pairs(val_split)),
        "arm4": (arm4_pairs(train_split), arm4_pairs(val_split)),
    }
    for name, (tr, va) in arms.items():
        write_jsonl(OUT_DIR / f"{name}_train.jsonl", tr)
        write_jsonl(OUT_DIR / f"{name}_val.jsonl", va)

    # Back-compat: plain C3 empty-schema pairs (== Arm 1's C3 half) and eval reference.
    write_jsonl(OUT_DIR / "train_pairs.jsonl", [pair_c3(r) for r in train_split])
    write_jsonl(OUT_DIR / "val_pairs.jsonl", [pair_c3(r) for r in val_split])
    write_jsonl(OUT_DIR / "eval_pairs.jsonl", [pair_c3(r) for r in eval_recs])

    # Leakage assertion at the record level.
    train_ids = {r["id"] for r in train_split} | {r["id"] for r in val_split}
    leak = train_ids & eval_ids
    assert not leak, f"LEAKAGE: {len(leak)} training ids appear in eval sample"

    manifest = {
        "description": "Multi-arm fine-tuning data (empty-schema arms). No passage. Arm S filled schemas built separately.",
        "seed": SEED,
        "val_fraction": VAL_FRACTION,
        "random_schema_seed_base": RANDOM_SCHEMA_SEED,
        "target_source": "SQuAD gold (first span), fallback annotator answer",
        "record_counts": {
            "total_labeled": len(all_items),
            "eval_sample_size": len(eval_ids),
            "train_records": len(train_split),
            "val_records": len(val_split),
            "eval_records": len(eval_recs),
            "dropped_empty_train": dropped_train,
            "dropped_empty_eval": dropped_eval,
        },
        "arm_pair_counts": {
            "arm1_train": len(arms["arm1"][0]), "arm1_val": len(arms["arm1"][1]),
            "arm2_train": len(arms["arm2"][0]), "arm2_val": len(arms["arm2"][1]),
            "arm4_train": len(arms["arm4"][0]), "arm4_val": len(arms["arm4"][1]),
        },
        "arm_descriptions": {
            "arm1": "mix C1 (question) + C3 (question+empty matched schema)",
            "arm2": "C3 (matched) + C5 (mismatched) per question, same target; schema-sensitivity",
            "arm4": "C1 only (answer-only control / floor)",
        },
        "leakage_check": {"train_val_ids_in_eval_sample": len(leak), "ok": len(leak) == 0},
        "train_class_distribution": {str(k): v for k, v in sorted(Counter(r["class_id"] for r in train_split).items())},
    }
    json.dump(manifest, open(OUT_DIR / "build_manifest.json", "w"), indent=2)

    print("Wrote per-arm training data to", OUT_DIR)
    for name, (tr, va) in arms.items():
        print(f"  {name}: train={len(tr)} val={len(va)}")
    print(f"  (back-compat) train_pairs.jsonl={len([1 for _ in train_split])} val_pairs.jsonl={len(val_split)} eval_pairs.jsonl={len(eval_recs)}")
    print("Leakage check:", "OK" if manifest["leakage_check"]["ok"] else "FAILED")
    print("Records: train=%d val=%d eval=%d" % (len(train_split), len(val_split), len(eval_recs)))
    print("Train class distribution:", manifest["train_class_distribution"])
    print()
    print("Sanity — Arm 2 first two pairs (should be same question, C3 then C5):")
    a2 = arms["arm2"][0]
    for p in a2[:2]:
        print(f"  cond={p['condition']} target={p['target']!r} input={p['input'][:70].replace(chr(10),' ')}...")


if __name__ == "__main__":
    main()
