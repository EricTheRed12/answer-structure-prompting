import json
from pathlib import Path

R = Path(__file__).parent / "results"

# five original models + fixed qwen
models = {
    "Llama 3.2 1B": "llama3.2_1b",
    "Gemma 2 2B": "gemma2_2b",
    "Llama 3.2 3B": "llama3.2_3b",
    "Phi-3 Mini": "phi3_mini",
    "Llama 3 8B": "llama3_8b",
    "Qwen 3 8B": "qwen3_8b_fixed",
}

def f1(prefix, cond):
    a = json.load(open(R / f"{prefix}_{cond}.json"))["aggregates"]
    return a.get("f1_extracted") or a.get("f1_ext")

print("Model            C1     C2     C3     C4     C5     C6   | C3-C1  C4-C2  C4vsC6")
print("-" * 88)
c2vals = []
for name, p in models.items():
    c1 = f1(p, "question_only"); c2 = f1(p, "question_passage")
    c3 = f1(p, "question_matched"); c4 = f1(p, "question_passage_matched")
    c5 = f1(p, "question_random"); c6 = f1(p, "question_passage_random")
    c2vals.append(c2)
    print(f"{name:15s} {c1:.3f}  {c2:.3f}  {c3:.3f}  {c4:.3f}  {c5:.3f}  {c6:.3f} | {c3-c1:+.3f} {c4-c2:+.3f} {c4-c6:+.3f}")

print()
print(f"C2 (passage) range across models: {min(c2vals):.3f} to {max(c2vals):.3f}")
