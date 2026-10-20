"""
Evaluation pipeline for taxonomy-guided question answering.

Runs SQuAD questions through Ollama with scaffold prompts across
8 experimental conditions, computes EM/F1 scores.

Usage:
  python3 src/eval_pipeline.py --model llama3.2 --conditions 1 2 3 4 --limit 50
  (run from the repository root)

Requirements:
  - Ollama running locally (default: http://localhost:11434)
  - Model already pulled (e.g. ollama pull llama3.2)
"""

import argparse
import json
import re
import string
import time
from collections import defaultdict
from pathlib import Path
from typing import Optional

import requests

from scaffold_builder import build_scaffold, condition_name

# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).parent.parent
SQUAD_PATH = PROJECT_ROOT / "data" / "squad_dev.json"
CLASSIFIED_PATH = PROJECT_ROOT / "taxonomy" / "all_results.json"
RESULTS_DIR = PROJECT_ROOT / "study1_main" / "results"

# ============================================================
# FEATURE → 10-CLASS MAPPING
# ============================================================

# Mapping logic derived from taxonomy_final.md:
# - Class 3 (Multipart) captures ALL multipart cardinality questions
# - For singular questions, relational_context is the primary discriminator
# - identificatory splits by entity_type:
#     thing → Class 1 (Object), concept/person → Class 2, place → Class 6,
#     number → Class 4, time → Class 5
# - Rare relational_context values (instrumental, role, procedural) are absorbed
#   into nearest neighbor classes per taxonomy design rationale.

# Direct relational_context → class_id (for singular cardinality)
_RC_TO_CLASS = {
    "quantitative": 4,
    "temporal": 5,
    "locative": 6,
    "agent": 7,
    "descriptive": 8,
    "causal": 9,
    "resultative": 10,
    # Absorbed rare classes — mapped to nearest neighbor:
    "instrumental": 1,   # answers a "what was used" → Object Identification
    "role": 2,           # answers "what role/function" → Concept/Person ID
    "procedural": 8,     # answers "how does X work" → Descriptive (quality/process)
}

# identificatory splits by entity_type
_IDENT_ENTITY_TO_CLASS = {
    "thing": 1,      # Object Identification
    "concept": 2,    # Concept/Person Identification
    "person": 2,     # Concept/Person Identification
    "place": 6,      # Place
    "number": 4,     # Quantitative
    "time": 5,       # Temporal
}


def map_to_class(item: dict) -> int:
    """
    Map a classified question (5-feature dict) to a final 10-class taxonomy ID.

    Parameters
    ----------
    item : dict
        Must have keys: cardinality, relational_context, entity_type

    Returns
    -------
    int
        Class ID (1-10)
    """
    cardinality = item.get("cardinality", "singular")
    relational_context = item.get("relational_context", "identificatory")
    entity_type = item.get("entity_type", "thing")

    # Multipart always → Class 3
    if cardinality == "multipart":
        return 3

    # Identificatory splits by entity type
    if relational_context == "identificatory":
        return _IDENT_ENTITY_TO_CLASS.get(entity_type, 1)  # default to Object

    # All other relational_context values
    return _RC_TO_CLASS.get(relational_context, 8)  # default to Descriptive


# ============================================================
# DATA LOADING
# ============================================================


def load_squad_passages() -> dict:
    """
    Load SQuAD dev set, return dict mapping question_id → {passage, answers}.

    Returns
    -------
    dict
        {qid: {"passage": str, "answers": [str, ...]}}
    """
    with open(SQUAD_PATH) as f:
        data = json.load(f)

    qa_map = {}
    for article in data["data"]:
        for para in article["paragraphs"]:
            context = para["context"]
            for qa in para["qas"]:
                if not qa.get("is_impossible", False):
                    answers = [a["text"] for a in qa.get("answers", [])]
                    if answers:
                        qa_map[qa["id"]] = {
                            "passage": context,
                            "answers": answers,
                        }
    return qa_map


def load_classified_questions() -> list:
    """
    Load classified questions with 5-feature annotations.

    Returns
    -------
    list of dict
        Each has: id, question, answer, interrogative, cardinality,
        entity_type, answer_form, relational_context
    """
    with open(CLASSIFIED_PATH) as f:
        return json.load(f)


def build_dataset() -> list:
    """
    Join classified questions with SQuAD passages and compute class IDs.

    Returns
    -------
    list of dict
        Each has: id, question, passage, gold_answers, class_id, features
    """
    classified = load_classified_questions()
    passages = load_squad_passages()

    dataset = []
    missing_passage = 0

    for item in classified:
        qid = item["id"]
        if qid not in passages:
            missing_passage += 1
            continue

        squad_entry = passages[qid]
        class_id = map_to_class(item)

        dataset.append({
            "id": qid,
            "question": item["question"],
            "passage": squad_entry["passage"],
            "gold_answers": squad_entry["answers"],
            "class_id": class_id,
            "features": {
                "interrogative": item.get("interrogative"),
                "cardinality": item.get("cardinality"),
                "entity_type": item.get("entity_type"),
                "answer_form": item.get("answer_form"),
                "relational_context": item.get("relational_context"),
            },
        })

    if missing_passage > 0:
        print(f"  Warning: {missing_passage} questions missing passage (skipped)")

    return dataset


# ============================================================
# METRICS (SQuAD-standard EM / F1)
# ============================================================


def normalize_answer(text: str) -> str:
    """Lower, strip articles/punctuation/whitespace for SQuAD evaluation."""
    text = text.lower()
    # Remove articles
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Collapse whitespace
    text = " ".join(text.split())
    return text


def _token_f1(pred_tokens: list, gold_tokens: list) -> float:
    """Compute token-level F1 between two token lists."""
    if not pred_tokens or not gold_tokens:
        return 0.0
    common = set(pred_tokens) & set(gold_tokens)
    num_common = sum(min(pred_tokens.count(t), gold_tokens.count(t)) for t in common)
    if num_common == 0:
        return 0.0
    precision = num_common / len(pred_tokens)
    recall = num_common / len(gold_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def best_span_extraction(prediction: str, gold_answers: list) -> str:
    """
    Extract the contiguous token span from prediction that maximizes F1
    against the best-matching gold answer.

    This is the max-F1 substring extraction method: for every possible
    contiguous subsequence of tokens in the (normalized) prediction, compute
    F1 against each gold answer and return the span with the highest score.

    For efficiency, limits the search window to 2x the length of the longest
    gold answer (since the optimal span is unlikely to be much longer).
    """
    pred_tokens = normalize_answer(prediction).split()
    if not pred_tokens:
        return ""

    # Determine max span length to search (2x longest gold, minimum 1)
    gold_token_lists = [normalize_answer(g).split() for g in gold_answers]
    max_gold_len = max(len(g) for g in gold_token_lists) if gold_token_lists else 1
    max_span_len = min(len(pred_tokens), max_gold_len * 2)

    best_f1 = 0.0
    best_span_tokens = pred_tokens  # fallback: full prediction

    for start in range(len(pred_tokens)):
        for end in range(start + 1, min(start + max_span_len + 1, len(pred_tokens) + 1)):
            span = pred_tokens[start:end]
            for gold_tokens in gold_token_lists:
                f1 = _token_f1(span, gold_tokens)
                if f1 > best_f1:
                    best_f1 = f1
                    best_span_tokens = span

    return " ".join(best_span_tokens)


def exact_match(prediction: str, gold_answers: list) -> float:
    """1.0 if normalized prediction matches any gold answer, else 0.0."""
    pred_norm = normalize_answer(prediction)
    for gold in gold_answers:
        if pred_norm == normalize_answer(gold):
            return 1.0
    return 0.0


def exact_match_extracted(prediction: str, gold_answers: list) -> float:
    """
    EM after max-F1 span extraction.

    Extracts the best contiguous span from the prediction, then checks
    if it exactly matches any gold answer (after normalization).
    """
    extracted = best_span_extraction(prediction, gold_answers)
    for gold in gold_answers:
        if extracted == normalize_answer(gold):
            return 1.0
    return 0.0


def f1_score(prediction: str, gold_answers: list) -> float:
    """Token-level F1, max over all gold answers."""
    pred_tokens = normalize_answer(prediction).split()
    best_f1 = 0.0

    for gold in gold_answers:
        gold_tokens = normalize_answer(gold).split()
        f1 = _token_f1(pred_tokens, gold_tokens)
        best_f1 = max(best_f1, f1)

    return best_f1


# ============================================================
# OLLAMA INFERENCE
# ============================================================


def query_ollama(
    prompt: str,
    model: str,
    base_url: str = "http://localhost:11434",
    temperature: float = 0.0,
    max_tokens: int = 512,
) -> str:
    """
    Send a prompt to Ollama and return the response text.

    Uses the /api/generate endpoint for raw completion.
    """
    url = f"{base_url}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }

    try:
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            f"Cannot connect to Ollama at {base_url}. "
            "Make sure Ollama is running (ollama serve)."
        )
    except requests.exceptions.Timeout:
        return ""  # treat timeout as empty response
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Ollama HTTP error: {e}")


# ============================================================
# PIPELINE
# ============================================================


def run_condition(
    dataset: list,
    condition: int,
    model: str,
    base_url: str = "http://localhost:11434",
    limit: Optional[int] = None,
    random_seed: int = 42,
) -> list:
    """
    Run a single experimental condition across the dataset.

    Returns list of per-question result dicts.
    """
    results = []
    items = dataset[:limit] if limit else dataset
    total = len(items)
    cond_label = condition_name(condition)

    print(f"\n{'='*60}")
    print(f"Condition {condition}: {cond_label}")
    print(f"Model: {model} | Questions: {total}")
    print(f"{'='*60}")

    for i, item in enumerate(items):
        # Build scaffold prompt
        scaffold = build_scaffold(
            question=item["question"],
            condition=condition,
            passage=item["passage"] if condition in (2, 4, 6, 8) else None,
            class_id=item["class_id"] if condition >= 3 else None,
            random_seed=random_seed + i if condition in (5, 6) else None,
        )

        # Query model
        t0 = time.time()
        prediction = query_ollama(scaffold, model=model, base_url=base_url)
        latency = time.time() - t0

        # Score
        em = exact_match(prediction, item["gold_answers"])
        em_extracted = exact_match_extracted(prediction, item["gold_answers"])
        f1 = f1_score(prediction, item["gold_answers"])

        result = {
            "id": item["id"],
            "question": item["question"],
            "gold_answers": item["gold_answers"],
            "prediction": prediction,
            "class_id": item["class_id"],
            "exact_match": em,
            "exact_match_extracted": em_extracted,
            "f1": f1,
            "latency_s": round(latency, 2),
        }
        results.append(result)

        # Progress
        if (i + 1) % 10 == 0 or (i + 1) == total:
            avg_em = sum(r["exact_match"] for r in results) / len(results)
            avg_em_ext = sum(r["exact_match_extracted"] for r in results) / len(results)
            avg_f1 = sum(r["f1"] for r in results) / len(results)
            print(f"  [{i+1}/{total}] EM={avg_em:.3f} EM_ext={avg_em_ext:.3f} F1={avg_f1:.3f}")

    return results


def compute_aggregates(results: list) -> dict:
    """Compute aggregate metrics from per-question results."""
    if not results:
        return {"em": 0.0, "em_extracted": 0.0, "f1": 0.0, "n": 0}

    n = len(results)
    avg_em = sum(r["exact_match"] for r in results) / n
    avg_em_ext = sum(r["exact_match_extracted"] for r in results) / n
    avg_f1 = sum(r["f1"] for r in results) / n
    avg_latency = sum(r["latency_s"] for r in results) / n

    # Per-class breakdown
    by_class = defaultdict(list)
    for r in results:
        by_class[r["class_id"]].append(r)

    class_metrics = {}
    for cid, class_results in sorted(by_class.items()):
        cn = len(class_results)
        class_metrics[cid] = {
            "n": cn,
            "em": sum(r["exact_match"] for r in class_results) / cn,
            "em_extracted": sum(r["exact_match_extracted"] for r in class_results) / cn,
            "f1": sum(r["f1"] for r in class_results) / cn,
        }

    return {
        "n": n,
        "em": round(avg_em, 4),
        "em_extracted": round(avg_em_ext, 4),
        "f1": round(avg_f1, 4),
        "avg_latency_s": round(avg_latency, 2),
        "by_class": class_metrics,
    }


def run_pipeline(args):
    """Main pipeline: load data, run conditions, save results."""
    print("Loading dataset...")
    dataset = build_dataset()
    print(f"  Loaded {len(dataset)} questions with passages and class IDs")

    # Class distribution
    class_dist = defaultdict(int)
    for item in dataset:
        class_dist[item["class_id"]] += 1
    print("  Class distribution:")
    for cid in sorted(class_dist.keys()):
        print(f"    Class {cid:2d}: {class_dist[cid]:5d}")

    # Ensure results directory
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Run each condition
    all_aggregates = {}
    for condition in args.conditions:
        results = run_condition(
            dataset=dataset,
            condition=condition,
            model=args.model,
            base_url=args.base_url,
            limit=args.limit,
            random_seed=args.seed,
        )

        aggregates = compute_aggregates(results)
        cond_label = condition_name(condition)
        all_aggregates[cond_label] = aggregates

        # Save per-question results
        per_q_file = RESULTS_DIR / f"{args.model}_{cond_label}.json"
        with open(per_q_file, "w") as f:
            json.dump(
                {"model": args.model, "condition": condition,
                 "condition_name": cond_label, "aggregates": aggregates,
                 "results": results},
                f, indent=2,
            )
        print(f"\n  Saved: {per_q_file.name}")
        print(f"  EM={aggregates['em']:.4f}  EM_ext={aggregates['em_extracted']:.4f}  F1={aggregates['f1']:.4f}  n={aggregates['n']}")

    # Save aggregate summary
    summary_file = RESULTS_DIR / f"{args.model}_summary.json"
    with open(summary_file, "w") as f:
        json.dump(
            {"model": args.model, "conditions": all_aggregates,
             "limit": args.limit, "seed": args.seed},
            f, indent=2,
        )
    print(f"\n{'='*60}")
    print(f"SUMMARY saved to: {summary_file.name}")
    print(f"{'='*60}")
    for cond_label, agg in all_aggregates.items():
        print(f"  {cond_label:30s}  EM={agg['em']:.4f}  EM_ext={agg['em_extracted']:.4f}  F1={agg['f1']:.4f}  (n={agg['n']})")


# ============================================================
# CLI
# ============================================================


def main():
    parser = argparse.ArgumentParser(
        description="Run evaluation pipeline for taxonomy-guided QA"
    )
    parser.add_argument(
        "--model", type=str, required=True,
        help="Ollama model name (e.g. llama3.2, mistral, phi3)"
    )
    parser.add_argument(
        "--conditions", type=int, nargs="+", default=[1, 2, 3, 4, 5, 6, 7, 8],
        help="Which conditions to run (1-8). Default: all."
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Limit number of questions per condition (for testing)"
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for reproducibility (conditions 5-6)"
    )
    parser.add_argument(
        "--base-url", type=str, default="http://localhost:11434",
        help="Ollama API base URL"
    )

    args = parser.parse_args()
    run_pipeline(args)


if __name__ == "__main__":
    main()
