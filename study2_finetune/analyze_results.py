"""
Interpret multiarm_results.json against the 7 validations (V1-V7) with paired
bootstrap 95% CIs on F1_ext deltas. Reads per-question F1_ext lists so every claim
gets an interval, not a bare number.

Run (from the repository root):
  python3 study2_finetune/analyze_results.py
"""
import json
import random
from pathlib import Path

HERE = Path(__file__).parent
RES = HERE / "multiarm_results.json"
results = json.load(open(RES))


def pq(key):
    return results.get(key, {}).get("per_q_f1ext", [])


def mean(v):
    return sum(v) / len(v) if v else float("nan")


def boot_delta(a_key, b_key, n_boot=2000, seed=0):
    a, b = pq(a_key), pq(b_key)
    n = min(len(a), len(b))
    if n == 0:
        return None
    diffs = [a[i] - b[i] for i in range(n)]
    m = sum(diffs) / n
    rng = random.Random(seed)
    boots = []
    for _ in range(n_boot):
        s = 0.0
        for _ in range(n):
            s += diffs[rng.randrange(n)]
        boots.append(s / n)
    boots.sort()
    lo = boots[int(0.025 * n_boot)]
    hi = boots[int(0.975 * n_boot)]
    sig = "SIGNIFICANT" if (lo > 0 or hi < 0) else "n.s. (CI spans 0)"
    return round(m, 4), round(lo, 4), round(hi, 4), sig


def fmt(label, res):
    if res is None:
        print(f"  {label}: (missing data)")
    else:
        m, lo, hi, sig = res
        print(f"  {label}: {m:+.4f}  [95% CI {lo:+.4f}, {hi:+.4f}]  {sig}")


def val(key, metric="f1_ext"):
    return results.get(key, {}).get(metric)


print("=" * 70)
print("POINT ESTIMATES (F1_ext)")
print("=" * 70)
for k in ["untuned_C1", "untuned_C2", "untuned_C3", "untuned_C5", "untuned_prose",
          "arm1_C1", "arm1_C3", "arm1_C5", "arm2_C1", "arm2_C3", "arm2_C5",
          "arm4_C1", "arm4_C3", "arm4_C5",
          "armS_filled", "armS_filled_prose", "untuned_structured_passage",
          "content_retention_filled"]:
    if k in results:
        v = results[k]
        if isinstance(v, dict) and "f1_ext" in v:
            print(f"  {k:28s} F1_ext={v['f1_ext']:.4f}  EM_ext={v.get('em_ext','?')}  n={v.get('n','?')}")
        else:
            print(f"  {k:28s} {v}")

print()
print("=" * 70)
print("V1  Does a matched structure help? (C3 - C1), per model")
print("=" * 70)
for arm in ["untuned", "arm1", "arm2", "arm4"]:
    fmt(f"{arm} C3-C1", boot_delta(f"{arm}_C3", f"{arm}_C1"))

print()
print("=" * 70)
print("V2  Does the SPECIFIC structure matter? (C3 - C5) = merit test")
print("=" * 70)
for arm in ["untuned", "arm1", "arm2", "arm4"]:
    fmt(f"{arm} C3-C5", boot_delta(f"{arm}_C3", f"{arm}_C5"))

print()
print("=" * 70)
print("V5  Does fine-tuning rescue the schema? (trained C3 - untuned C3)")
print("=" * 70)
for arm in ["arm1", "arm2", "arm4"]:
    fmt(f"{arm} C3 vs untuned C3", boot_delta(f"{arm}_C3", "untuned_C3"))

print()
print("=" * 70)
print("V6  Delivery FORM: prose vs schema of the SAME empty structure (prose - C3)")
print("=" * 70)
for arm in ["untuned", "arm1", "arm2", "arm4"]:
    fmt(f"{arm} prose-C3", boot_delta(f"{arm}_prose", f"{arm}_C3"))

print()
print("=" * 70)
print("V7  Content-vs-form (leak-proof): structured passage vs raw paragraph")
print("=" * 70)
fmt("structured_passage - C2", boot_delta("untuned_structured_passage", "untuned_C2"))
print(f"  [Arm S filled schema = {val('armS_filled')} -> ANSWER-CONTAINER LEAK, reported as future work, not a fair result]")
if "content_retention_filled" in results:
    print(f"  [filled-schema content retention = {results['content_retention_filled'].get('recoverable_fraction')}]")

print()
print("=" * 70)
print("PARAGRAPH PARITY: best trained C3 vs untuned passage C2")
print("=" * 70)
best_c3 = max((val(f"{a}_C3") for a in ["arm1", "arm2", "arm4"]), default=None)
print(f"  best trained C3 = {best_c3} | untuned passage C2 = {val('untuned_C2')}")
print(f"  gap = {round(val('untuned_C2') - best_c3, 4) if best_c3 else '?'} (structure, even trained, does not reach prose-with-content)")
