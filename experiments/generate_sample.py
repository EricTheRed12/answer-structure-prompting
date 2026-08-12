"""
Generate a fixed stratified sample of questions for the experiment.

Produces a sample of N questions (default 1000) stratified by class ID
so that class proportions are preserved. The same sample is used across
all models and conditions for fair comparison.

Output: experiments/sample_1000.json

Run:
  cd /Users/core/Documents/GradSchool/CS699/rational-thinking
  python3 experiments/generate_sample.py --size 1000
"""

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from eval_pipeline import build_dataset

OUTPUT_DIR = Path(__file__).parent


def generate_stratified_sample(dataset: list, size: int, seed: int = 42) -> list:
    """
    Generate a stratified sample preserving class proportions.

    Parameters
    ----------
    dataset : list
        Full dataset from build_dataset()
    size : int
        Target sample size
    seed : int
        Random seed for reproducibility

    Returns
    -------
    list
        Sampled items
    """
    random.seed(seed)

    # Group by class
    by_class = defaultdict(list)
    for item in dataset:
        by_class[item["class_id"]].append(item)

    # Compute proportional allocation
    total = len(dataset)
    sample = []

    for cid in sorted(by_class.keys()):
        class_items = by_class[cid]
        # Proportional count, at least 1
        n_for_class = max(1, round(len(class_items) / total * size))
        # Don't exceed available
        n_for_class = min(n_for_class, len(class_items))
        sampled = random.sample(class_items, n_for_class)
        sample.extend(sampled)

    # Trim or pad to exact size if rounding caused mismatch
    if len(sample) > size:
        random.shuffle(sample)
        sample = sample[:size]
    elif len(sample) < size:
        # Add more from underrepresented classes
        used_ids = {item["id"] for item in sample}
        remaining = [item for item in dataset if item["id"] not in used_ids]
        random.shuffle(remaining)
        sample.extend(remaining[: size - len(sample)])

    # Shuffle final order
    random.shuffle(sample)
    return sample


def main():
    parser = argparse.ArgumentParser(description="Generate stratified experiment sample")
    parser.add_argument("--size", type=int, default=1000, help="Sample size (default 1000)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    print("Loading full dataset...")
    dataset = build_dataset()
    print(f"  Full dataset: {len(dataset)} questions")

    print(f"Generating stratified sample of {args.size}...")
    sample = generate_stratified_sample(dataset, args.size, args.seed)

    # Report class distribution
    class_dist = defaultdict(int)
    for item in sample:
        class_dist[item["class_id"]] += 1

    print(f"  Sample size: {len(sample)}")
    print(f"  Class distribution:")
    for cid in sorted(class_dist.keys()):
        full_count = sum(1 for d in dataset if d["class_id"] == cid)
        print(f"    Class {cid:2d}: {class_dist[cid]:4d} (full: {full_count})")

    # Save
    output_path = OUTPUT_DIR / f"sample_{args.size}.json"
    output = {
        "description": f"Stratified sample of {len(sample)} questions for experiment",
        "size": len(sample),
        "seed": args.seed,
        "full_dataset_size": len(dataset),
        "class_distribution": {str(k): v for k, v in sorted(class_dist.items())},
        "questions": sample,
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
