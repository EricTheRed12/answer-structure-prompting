"""Deep analysis of experiment results."""
import json
from collections import defaultdict
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"

# Load all results for a model
def load_model_results(model_prefix):
    """Load all conditions for a model.

    Only accept files named exactly ``{model_prefix}_{condition_name}.json``.
    A plain glob of ``{model_prefix}_*`` would also match sibling variants whose
    names start with the same prefix (e.g. ``llama3_8b`` matching the base-model
    ``llama3_8b_raw_*`` files), which would overwrite the real entries with
    differently-processed runs. Anchoring on the condition name keeps each model's
    runs separate.
    """
    conditions = {}
    for f in sorted(RESULTS_DIR.glob(f"{model_prefix}_*.json")):
        with open(f) as fh:
            data = json.load(fh)
        cond_name = data["condition_name"]
        # Reject prefix collisions: the stem must be exactly prefix + condition.
        if f.stem != f"{model_prefix}_{cond_name}":
            continue
        conditions[cond_name] = data
    return conditions

models = ["llama3.2_1b", "gemma2_2b", "llama3.2_3b", "phi3_mini", "llama3_8b", "qwen3_8b"]

print("=" * 80)
print("KEY COMPARISON: matched vs random vs baseline")
print("(Testing: does the CORRECT structure differentiate from WRONG structure?)")
print("=" * 80)

print(f"\n{'Model':<15s} {'Metric':<8s} {'C1 base':>8s} {'C3 match':>8s} {'C5 rand':>8s} {'C3>C5?':>7s} {'C3>C1?':>7s}")
print("-" * 70)

for model in models:
    data = load_model_results(model)
    if "question_only" not in data:
        continue
    c1 = data["question_only"]["aggregates"]
    c3 = data.get("question_matched", {}).get("aggregates", {})
    c5 = data.get("question_random", {}).get("aggregates", {})
    if not c3 or not c5:
        continue
    
    # F1_ext
    print(f"{model:<15s} {'F1_ext':<8s} {c1['f1_extracted']:>8.4f} {c3['f1_extracted']:>8.4f} {c5['f1_extracted']:>8.4f} {'YES' if c3['f1_extracted'] > c5['f1_extracted'] else 'no':>7s} {'YES' if c3['f1_extracted'] > c1['f1_extracted'] else 'no':>7s}")
    # EM_ext
    print(f"{'':15s} {'EM_ext':<8s} {c1['em_extracted']:>8.4f} {c3['em_extracted']:>8.4f} {c5['em_extracted']:>8.4f} {'YES' if c3['em_extracted'] > c5['em_extracted'] else 'no':>7s} {'YES' if c3['em_extracted'] > c1['em_extracted'] else 'no':>7s}")
    # Tokens (verbosity)
    print(f"{'':15s} {'tokens':<8s} {c1['avg_prediction_tokens']:>8.1f} {c3['avg_prediction_tokens']:>8.1f} {c5['avg_prediction_tokens']:>8.1f}")
    print()

print("\n" + "=" * 80)
print("WITH PASSAGE: matched vs random vs baseline")
print("=" * 80)

print(f"\n{'Model':<15s} {'Metric':<8s} {'C2 pass':>8s} {'C4 p+m':>8s} {'C6 p+r':>8s} {'C4>C6?':>7s} {'C4>C2?':>7s}")
print("-" * 70)

for model in models:
    data = load_model_results(model)
    c2 = data.get("question_passage", {}).get("aggregates", {})
    c4 = data.get("question_passage_matched", {}).get("aggregates", {})
    c6 = data.get("question_passage_random", {}).get("aggregates", {})
    if not c2 or not c4 or not c6:
        continue
    
    print(f"{model:<15s} {'F1_ext':<8s} {c2['f1_extracted']:>8.4f} {c4['f1_extracted']:>8.4f} {c6['f1_extracted']:>8.4f} {'YES' if c4['f1_extracted'] > c6['f1_extracted'] else 'no':>7s} {'YES' if c4['f1_extracted'] > c2['f1_extracted'] else 'no':>7s}")
    print(f"{'':15s} {'EM_ext':<8s} {c2['em_extracted']:>8.4f} {c4['em_extracted']:>8.4f} {c6['em_extracted']:>8.4f} {'YES' if c4['em_extracted'] > c6['em_extracted'] else 'no':>7s} {'YES' if c4['em_extracted'] > c2['em_extracted'] else 'no':>7s}")
    print(f"{'':15s} {'tokens':<8s} {c2['avg_prediction_tokens']:>8.1f} {c4['avg_prediction_tokens']:>8.1f} {c6['avg_prediction_tokens']:>8.1f}")
    print()

# Per-class analysis: which classes benefit?
print("\n" + "=" * 80)
print("PER-CLASS BREAKDOWN (llama3:8b, best-performing model)")
print("Does structure help for SPECIFIC answer types?")
print("=" * 80)

data = load_model_results("llama3_8b")
c1 = data["question_only"]
c3 = data["question_matched"]
c2 = data["question_passage"]
c4 = data["question_passage_matched"]

class_names = {
    "1": "Object ID", "2": "Concept/Person", "3": "Multipart",
    "4": "Quantitative", "5": "Temporal", "6": "Place",
    "7": "Agent", "8": "Descriptive", "9": "Causal", "10": "Resultative"
}

print(f"\n{'Class':<20s} {'C1 F1ext':>9s} {'C3 F1ext':>9s} {'Δ':>7s} {'C2 F1ext':>9s} {'C4 F1ext':>9s} {'Δ':>7s}")
print("-" * 75)

for cid in sorted(class_names.keys(), key=int):
    c1_class = c1["aggregates"]["by_class"].get(cid, {})
    c3_class = c3["aggregates"]["by_class"].get(cid, {})
    c2_class = c2["aggregates"]["by_class"].get(cid, {})
    c4_class = c4["aggregates"]["by_class"].get(cid, {})
    
    if not c1_class or not c3_class:
        continue
    
    d1 = c3_class["f1_extracted"] - c1_class["f1_extracted"]
    d2 = c4_class.get("f1_extracted", 0) - c2_class.get("f1_extracted", 0)
    
    print(f"{class_names[cid]:<20s} {c1_class['f1_extracted']:>9.4f} {c3_class['f1_extracted']:>9.4f} {d1:>+7.4f} {c2_class.get('f1_extracted', 0):>9.4f} {c4_class.get('f1_extracted', 0):>9.4f} {d2:>+7.4f}")

# Verbosity analysis
print("\n" + "=" * 80)
print("VERBOSITY: Does the scaffold make models more concise?")
print("=" * 80)
print(f"\n{'Model':<15s} {'C1 tok':>7s} {'C3 tok':>7s} {'C5 tok':>7s} {'C2 tok':>7s} {'C4 tok':>7s} {'C6 tok':>7s}")
print("-" * 60)

for model in models:
    data = load_model_results(model)
    c1 = data.get("question_only", {}).get("aggregates", {})
    c3 = data.get("question_matched", {}).get("aggregates", {})
    c5 = data.get("question_random", {}).get("aggregates", {})
    c2 = data.get("question_passage", {}).get("aggregates", {})
    c4 = data.get("question_passage_matched", {}).get("aggregates", {})
    c6 = data.get("question_passage_random", {}).get("aggregates", {})
    if not c1:
        continue
    print(f"{model:<15s} {c1.get('avg_prediction_tokens',0):>7.1f} {c3.get('avg_prediction_tokens',0):>7.1f} {c5.get('avg_prediction_tokens',0):>7.1f} {c2.get('avg_prediction_tokens',0):>7.1f} {c4.get('avg_prediction_tokens',0):>7.1f} {c6.get('avg_prediction_tokens',0):>7.1f}")
