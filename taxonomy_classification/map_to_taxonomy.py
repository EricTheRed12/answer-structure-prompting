"""
Maps the full 5,928-question classification results into our proposed 19-class taxonomy.
Shows the distribution to identify imbalances.
"""

import json
from collections import Counter

# Load results
with open('/Users/core/Documents/GradSchool/CS699/rational-thinking/taxonomy_classification/all_results.json') as f:
    data = json.load(f)

print(f'Total questions: {len(data)}')

# Define mapping rules for 19-class taxonomy
# Each rule: (conditions_dict, class_name)
# Conditions are checked in order; first match wins.

def classify(item):
    interrog = item.get('interrogative', '')
    card = item.get('cardinality', '')
    etype = item.get('entity_type', '')
    form = item.get('answer_form', '')
    rel = item.get('relational_context', '')
    
    # Normalize 'which' -> treat like 'what'
    if interrog == 'which':
        interrog = 'what'
    # Normalize 'whose' -> treat like 'who'
    if interrog == 'whose':
        interrog = 'who'
    if interrog == 'did':
        interrog = 'what'
    
    # Multipart → Class 6
    if card == 'multipart':
        return '6. Multipart Identificatory'
    
    # Agent family
    if rel == 'agent' and etype == 'person':
        return '14. Agent — Person'
    if rel == 'agent' and etype in ('thing', 'concept', 'process'):
        return '15. Agent — Thing'
    if rel == 'agent':
        return '15. Agent — Thing'  # catch-all agent
    
    # Temporal family
    if rel == 'temporal' and etype == 'time':
        # We split into point vs duration/range but can't distinguish from current features
        return '10/11. Temporal (unsplit)'
    if rel == 'temporal':
        return '10/11. Temporal (unsplit)'
    
    # Spatial family
    if rel == 'locative' and interrog == 'where':
        return '12. Place — Spatial'
    if rel == 'locative' and etype == 'place':
        return '13. Place — Contextual'
    if rel == 'locative':
        return '13. Place — Contextual'  # catch-all locative
    
    # Quantitative family
    if rel == 'quantitative' and interrog == 'how':
        # Split into count/measurement vs proportion — can't distinguish yet
        return '7/8. Quantitative — How (unsplit)'
    if rel == 'quantitative' and interrog in ('what', 'which'):
        return '9. Quantitative — Statistic'
    if rel == 'quantitative':
        return '7/8. Quantitative — How (unsplit)'
    
    # Causal
    if rel == 'causal':
        return '18. Causal'
    
    # Instrumental
    if rel == 'instrumental':
        return '17. Instrumental'
    
    # Resultative
    if rel == 'resultative':
        return '19. Resultative'
    
    # Descriptive
    if rel == 'descriptive':
        return '16. Descriptive'
    
    # Role — not in our 19, needs to go somewhere
    if rel == 'role':
        return 'UNMAPPED: Role'
    
    # Procedural — not in our 19 as standalone
    if rel == 'procedural':
        return 'UNMAPPED: Procedural'
    
    # Identificatory family — the big ones
    if rel == 'identificatory':
        if etype == 'person':
            return '5. Person — Identificatory'
        if etype == 'place':
            return '13. Place — Contextual'  # place identified by context
        if etype == 'thing':
            # Split: label vs functional — can't distinguish from features
            return '1/2. Thing Identificatory (unsplit)'
        if etype == 'concept':
            # Split: definition vs attribute — can't distinguish from features
            return '3/4. Concept Identificatory (unsplit)'
        if etype == 'number':
            return '9. Quantitative — Statistic'
        if etype == 'time':
            return '10/11. Temporal (unsplit)'
        return '3/4. Concept Identificatory (unsplit)'  # catch-all
    
    # Catch-all
    return f'UNMAPPED: {interrog}/{card}/{etype}/{form}/{rel}'


# Classify all
class_counts = Counter()
unmapped_examples = {}

for item in data:
    cls = classify(item)
    class_counts[cls] += 1
    if cls.startswith('UNMAPPED') and cls not in unmapped_examples:
        unmapped_examples[cls] = item.get('question', '')

# Print results
print('\n' + '='*70)
print('TAXONOMY CLASS DISTRIBUTION (19-class mapping)')
print('='*70 + '\n')

total = len(data)
print(f'{"Class":<45} {"Count":>6} {"Pct":>7}')
print('-'*60)

for cls, count in class_counts.most_common():
    pct = count / total * 100
    bar = '█' * int(pct)
    print(f'{cls:<45} {count:>6} {pct:>6.1f}% {bar}')

print(f'\n{"TOTAL":<45} {total:>6}')

# Show unmapped
if unmapped_examples:
    print('\n\nUNMAPPED CLASSES (need homes):')
    for cls, example in unmapped_examples.items():
        count = class_counts[cls]
        print(f'  {cls} ({count}x)')
        print(f'    Example: {example}')

# Summary stats
print('\n\n' + '='*70)
print('BALANCE ANALYSIS')
print('='*70)

mapped = [(cls, c) for cls, c in class_counts.items() if not cls.startswith('UNMAPPED')]
counts_only = [c for _, c in mapped]

if counts_only:
    avg = sum(counts_only) / len(counts_only)
    print(f'\nMapped classes: {len(mapped)}')
    print(f'Average per class: {avg:.0f}')
    print(f'Largest: {max(counts_only)}')
    print(f'Smallest: {min(counts_only)}')
    print(f'Ratio largest/smallest: {max(counts_only)/min(counts_only):.1f}x')
    
    print('\nClasses > 2x average (too heavy):')
    for cls, c in class_counts.most_common():
        if not cls.startswith('UNMAPPED') and c > 2 * avg:
            print(f'  {cls}: {c} ({c/avg:.1f}x avg)')
    
    print('\nClasses < 0.5x average (too light):')
    for cls, c in class_counts.most_common():
        if not cls.startswith('UNMAPPED') and c < 0.5 * avg:
            print(f'  {cls}: {c} ({c/avg:.1f}x avg)')
