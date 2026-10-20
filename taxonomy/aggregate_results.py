"""
Aggregates classification results from batch_XX_results.json files.
Counts feature combinations and identifies viable taxonomy classes.

Run after all 10 batch results are collected:
  python3 aggregate_results.py

Outputs:
  - taxonomy_summary.json: full combination counts
  - taxonomy_report.txt: human-readable summary
"""

import json
import os
from collections import Counter

results_dir = os.path.dirname(os.path.abspath(__file__))

# Load all batch results
all_classified = []

# First try the full API results file
full_results_path = os.path.join(results_dir, 'all_results.json')
if os.path.exists(full_results_path):
    with open(full_results_path) as f:
        all_classified = json.load(f)
    print(f'Loaded all_results.json: {len(all_classified)} items')
else:
    # Fall back to batch files
    for i in range(1, 11):
        filepath = os.path.join(results_dir, f'batch_{i:02d}_results.json')
        if os.path.exists(filepath):
            with open(filepath) as f:
                batch = json.load(f)
                all_classified.extend(batch)
            print(f'Loaded batch_{i:02d}_results.json: {len(batch)} items')
        else:
            print(f'MISSING: batch_{i:02d}_results.json')

print(f'\nTotal classified: {len(all_classified)}')

if not all_classified:
    print('No results to aggregate. Run classification batches first.')
    exit()

# Count individual feature values
print('\n' + '='*60)
print('FEATURE VALUE DISTRIBUTIONS')
print('='*60)

features = ['interrogative', 'cardinality', 'entity_type', 'answer_form', 'relational_context']

feature_counts = {}
for feat in features:
    counts = Counter(item.get(feat, 'MISSING') for item in all_classified)
    feature_counts[feat] = dict(counts.most_common())
    print(f'\n{feat}:')
    for val, count in counts.most_common():
        pct = count / len(all_classified) * 100
        print(f'  {val:20s} {count:4d} ({pct:5.1f}%)')

# Count full 5-feature combinations
print('\n' + '='*60)
print('TAXONOMY CLASSES (5-feature combinations)')
print('='*60)

combo_counter = Counter()
combo_examples = {}

for item in all_classified:
    combo = (
        item.get('interrogative', '?'),
        item.get('cardinality', '?'),
        item.get('entity_type', '?'),
        item.get('answer_form', '?'),
        item.get('relational_context', '?')
    )
    combo_counter[combo] += 1
    if combo not in combo_examples:
        combo_examples[combo] = item

print(f'\nTotal unique combinations: {len(combo_counter)}')
print(f'\nTop 30 classes by frequency:\n')
print(f'{"#":<4} {"Count":<6} {"%":<7} {"Interrogative":<14} {"Card.":<10} {"Entity":<10} {"Form":<10} {"Relational Context":<20}')
print('-' * 90)

for rank, (combo, count) in enumerate(combo_counter.most_common(30), 1):
    pct = count / len(all_classified) * 100
    print(f'{rank:<4} {count:<6} {pct:<7.1f} {combo[0]:<14} {combo[1]:<10} {combo[2]:<10} {combo[3]:<10} {combo[4]:<20}')

# Classes above threshold
threshold = 10  # minimum questions to be a standalone class
viable = [(combo, count) for combo, count in combo_counter.most_common() if count >= threshold]
rare = [(combo, count) for combo, count in combo_counter.most_common() if count < threshold]

print(f'\n\nViable classes (>= {threshold} questions): {len(viable)}')
print(f'Rare classes (< {threshold} questions): {len(rare)}')
print(f'Questions in rare classes: {sum(c for _, c in rare)}')

# Save full results
summary = {
    'total_classified': len(all_classified),
    'feature_distributions': feature_counts,
    'taxonomy_classes': [
        {
            'interrogative': combo[0],
            'cardinality': combo[1],
            'entity_type': combo[2],
            'answer_form': combo[3],
            'relational_context': combo[4],
            'count': count,
            'example_question': combo_examples[combo].get('question', ''),
            'example_answer': combo_examples[combo].get('answer', '')
        }
        for combo, count in combo_counter.most_common()
    ],
    'viable_classes': len(viable),
    'rare_classes': len(rare),
    'threshold': threshold
}

with open(os.path.join(results_dir, 'taxonomy_summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)

print(f'\nSaved taxonomy_summary.json')

# Write human-readable report
report_path = os.path.join(results_dir, 'taxonomy_report.txt')
with open(report_path, 'w') as f:
    f.write('TAXONOMY DERIVATION REPORT\n')
    f.write(f'Based on {len(all_classified)} classified SQuAD questions\n')
    f.write('='*60 + '\n\n')
    
    f.write('VIABLE TAXONOMY CLASSES\n')
    f.write(f'(minimum {threshold} questions per class)\n\n')
    
    for i, (combo, count) in enumerate(viable, 1):
        example = combo_examples[combo]
        f.write(f'Class {i}: {combo[0]}/{combo[1]}/{combo[2]}/{combo[3]}/{combo[4]}\n')
        f.write(f'  Count: {count} ({count/len(all_classified)*100:.1f}%)\n')
        f.write(f'  Example Q: {example.get("question", "")}\n')
        f.write(f'  Example A: {example.get("answer", "")}\n\n')
    
    f.write('\nRARE CLASSES (candidates for merging)\n\n')
    for combo, count in rare:
        example = combo_examples[combo]
        f.write(f'  {combo[0]}/{combo[1]}/{combo[2]}/{combo[3]}/{combo[4]} ({count}x)\n')
        f.write(f'    Ex: {example.get("question", "")}\n')

print(f'Saved {report_path}')
