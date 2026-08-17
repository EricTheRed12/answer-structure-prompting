"""
Scaffold prompt construction for the evaluation pipeline.

Assembles JSON prompts for each experimental condition by combining:
- question (always present)
- answer_structure (conditions 3-8)
- context_passage (conditions 2, 4, 6, 8)

The scaffold IS the prompt. No additional instruction tokens.
"""

import json
import random
from pathlib import Path
from typing import Optional

SCHEMAS_PATH = Path(__file__).parent.parent / "taxonomy_classification" / "schemas.json"


def load_schemas(path: Optional[Path] = None) -> dict:
    """Load taxonomy schemas from JSON file."""
    path = path or SCHEMAS_PATH
    with open(path, "r") as f:
        data = json.load(f)
    # Index by class ID for fast lookup
    return {cls["id"]: cls for cls in data["classes"]}


# Module-level schema cache
_SCHEMAS = None


def _get_schemas() -> dict:
    global _SCHEMAS
    if _SCHEMAS is None:
        _SCHEMAS = load_schemas()
    return _SCHEMAS


def get_answer_structure(class_id: int) -> dict:
    """Return the answer structure schema for a given class ID."""
    schemas = _get_schemas()
    if class_id not in schemas:
        raise ValueError(f"Unknown class_id: {class_id}. Valid: {list(schemas.keys())}")
    return schemas[class_id]["schema"]


def get_random_class_id(exclude_id: int) -> int:
    """Pick a random class ID that is NOT the given one (for ablation conditions)."""
    schemas = _get_schemas()
    candidates = [cid for cid in schemas.keys() if cid != exclude_id]
    return random.choice(candidates)


def build_scaffold(
    question: str,
    condition: int,
    passage: Optional[str] = None,
    class_id: Optional[int] = None,
    random_seed: Optional[int] = None,
) -> str:
    """
    Build the scaffold prompt as a JSON string.

    Parameters
    ----------
    question : str
        The question text.
    condition : int (1-8)
        1: question only
        2: question + passage
        3: question + matched answer structure
        4: question + passage + matched answer structure
        5: question + random answer structure
        6: question + passage + random answer structure
        7: question + classified answer structure
        8: question + passage + classified answer structure
    passage : str, optional
        Context passage (required for conditions 2, 4, 6, 8).
    class_id : int, optional
        The taxonomy class ID. Required for conditions 3-8.
        For conditions 3-4: used directly (oracle/matched).
        For conditions 5-6: used to exclude from random selection.
        For conditions 7-8: the classifier's predicted class.
    random_seed : int, optional
        Seed for random class selection (conditions 5-6). For reproducibility.

    Returns
    -------
    str
        JSON string representing the complete prompt.
    """
    if condition < 1 or condition > 8:
        raise ValueError(f"Condition must be 1-8, got {condition}")

    needs_passage = condition in (2, 4, 6, 8)
    needs_structure = condition in (3, 4, 5, 6, 7, 8)

    if needs_passage and passage is None:
        raise ValueError(f"Condition {condition} requires a passage.")
    if needs_structure and class_id is None:
        raise ValueError(f"Condition {condition} requires a class_id.")

    # Start building the scaffold
    scaffold = {"question": question}

    # Add answer structure if needed
    if needs_structure:
        if condition in (5, 6):
            # Random/wrong structure (ablation)
            if random_seed is not None:
                random.seed(random_seed)
            wrong_class_id = get_random_class_id(exclude_id=class_id)
            scaffold["answer_structure"] = get_answer_structure(wrong_class_id)
        else:
            # Matched (3, 4) or classified (7, 8)
            scaffold["answer_structure"] = get_answer_structure(class_id)

    # Add passage if needed
    if needs_passage:
        scaffold["context_passage"] = passage

    return json.dumps(scaffold, indent=2)


# Condition metadata for documentation/logging
CONDITIONS = {
    1: "question_only",
    2: "question_passage",
    3: "question_matched",
    4: "question_passage_matched",
    5: "question_random",
    6: "question_passage_random",
    7: "question_classified",
    8: "question_passage_classified",
}


def condition_name(condition: int) -> str:
    """Return the human-readable name for a condition number."""
    return CONDITIONS.get(condition, f"unknown_{condition}")
