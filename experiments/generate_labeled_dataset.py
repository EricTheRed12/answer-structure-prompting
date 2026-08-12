"""
Generate the labeled dataset: question → features → class_id.

This persists the full mapping from classified questions (all_results.json)
to final 10-class taxonomy IDs for use in BERT classifier training and
experiment reproducibility.

Output: taxonomy_classification/labeled_dataset.json

Run:
  cd /Users/core/Documents/GradSchool/CS699/rational-thinking
  python3 experiments/generate_labeled_dataset.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from eval_pipeline import map_to_class, load_classified_questions, load_squad_passages

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_PATH = PROJECT_ROOT / "taxonomy_classification" / "labeled_dataset.json"
SCHEMAS_PATH = PROJECT_ROOT / "taxonomy_classification" / "schemas.json"


def _get_question_from_squad(qid: str) -> str:
    """Look up question text directly from squad_dev.json by ID."""
    squad_path = PROJECT_ROOT / "squad_dev.json"
    with open(squad_path) as f:
        data = json.load(f)
    for article in data["data"]:
        for para in article["paragraphs"]:
            for qa in para["qas"]:
                if qa["id"] == qid:
                    return qa["question"]
    return ""


def main():
    # Load schemas for class names
    with open(SCHEMAS_PATH) as f:
        schemas = json.load(f)
    class_names = {cls["id"]: cls["name"] for cls in schemas["classes"]}

    # Load classified questions
    classified = load_classified_questions()
    print(f"Loaded {len(classified)} classified questions")

    # Load passages for completeness
    passages = load_squad_passages()
    print(f"Loaded {len(passages)} passages from SQuAD")

    # Build labeled dataset
    dataset = []
    for item in classified:
        class_id = map_to_class(item)
        qid = item["id"]

        # Get question/answer text — prefer all_results.json, fall back to SQuAD
        question = item.get("question")
        answer = item.get("answer")
        if (not question) and qid in passages:
            # Reconstruct from SQuAD data
            question = ""  # SQuAD passages dict doesn't store question text
            answer = passages[qid]["answers"][0] if passages[qid]["answers"] else ""

        # Skip if we truly have no question text and can't recover it
        if not question:
            # Pull from SQuAD source directly
            question = _get_question_from_squad(qid)

        entry = {
            "id": qid,
            "question": question or "",
            "answer": answer or "",
            "class_id": class_id,
            "class_name": class_names[class_id],
            "features": {
                "interrogative": item.get("interrogative"),
                "cardinality": item.get("cardinality"),
                "entity_type": item.get("entity_type"),
                "answer_form": item.get("answer_form"),
                "relational_context": item.get("relational_context"),
            },
        }
        # Include passage if available
        if qid in passages:
            entry["passage"] = passages[qid]["passage"]
            entry["gold_answers"] = passages[qid]["answers"]

        dataset.append(entry)

    # Summary
    class_dist = Counter(d["class_id"] for d in dataset)
    print(f"\nGenerated {len(dataset)} labeled examples")
    print(f"Class distribution:")
    for cid in sorted(class_dist.keys()):
        print(f"  {cid:2d} ({class_names[cid]:30s}): {class_dist[cid]:5d}")

    # Save
    output = {
        "description": "SQuAD questions labeled with final 10-class taxonomy IDs",
        "taxonomy_version": "final_10_class",
        "total": len(dataset),
        "class_distribution": {str(k): v for k, v in sorted(class_dist.items())},
        "class_names": {str(k): v for k, v in sorted(class_names.items())},
        "data": dataset,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
