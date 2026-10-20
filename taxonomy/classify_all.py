"""
Classifies all answerable SQuAD questions using the Anthropic API.

Setup:
  pip install anthropic
  export ANTHROPIC_API_KEY="sk-ant-..."

Run (from the repository root):
  python3 taxonomy/classify_all.py

Outputs:
  - all_results.json: full classification results for all questions
  - Progress saves every 50 questions to all_results_partial.json

Estimated cost: ~$1.50 using Haiku for 5,928 questions
Estimated time: ~20-30 minutes
"""

import json
import os
import time
import anthropic

# ============================================================
# CONFIG
# ============================================================

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
SQUAD_PATH = os.path.join(_ROOT, 'data', 'squad_dev.json')
OUTPUT_DIR = _HERE
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'all_results.json')
PARTIAL_FILE = os.path.join(OUTPUT_DIR, 'all_results_partial.json')

MODEL = 'claude-haiku-4-5-20251001'  # cheapest option, sufficient for structured classification
BATCH_SIZE = 20  # questions per API call (keeps responses manageable)
DELAY = 0.5  # seconds between API calls to avoid rate limits

# ============================================================
# CLASSIFICATION PROMPT
# ============================================================

SYSTEM_PROMPT = """You are classifying SQuAD questions according to 5 features that define answer structure types.

## Features

1. **interrogative** — The primary interrogative of the question.
   Values: who, what, when, where, why, how

2. **cardinality** — Whether the answer requires one piece of information or multiple distinct pieces.
   Values: singular, multipart

3. **entity_type** — The type of entity the answer represents.
   Values: person, place, thing, time, number, concept
   - person: a named individual or group of people
   - place: a geographic location, region, or spatial reference
   - thing: a concrete object, substance, document, organization, technology
   - time: a date, era, duration, or temporal expression
   - number: a quantity, measurement, percentage, or count
   - concept: an abstract idea, quality, relationship, or process description

4. **answer_form** — The grammatical form of the answer span.
   Values: noun, verb, adjective, clause
   - noun: a noun phrase (single word or multi-word)
   - verb: an action word or verb phrase
   - adjective: a descriptive word or quality
   - clause: a full or partial clause (subject+verb or longer)

5. **relational_context** — What role the answer plays relative to the question's action/framing. This is the most important differentiator.
   Values: identificatory, agent, resultative, instrumental, role, locative, temporal, descriptive, quantitative, causal, procedural
   - identificatory: the answer simply IS the thing asked about ("What is X?" → X is Y)
   - agent: the answer performed the action in the question ("Who founded X?" → person did it)
   - resultative: the answer is the outcome/effect of something ("What effect did X have?" → the effect)
   - instrumental: the answer was used/needed to do something ("What was used to...?" → the tool/means)
   - role: the answer served a function or position ("What city served as capital?" → the city in that role)
   - locative: the answer is where something is/was ("Where is X?" → the place)
   - temporal: the answer is when something happened ("When did X occur?" → the time)
   - descriptive: the answer describes a quality/property ("What is X described as?" → the description)
   - quantitative: the answer is a quantity ("How many X?" → the number)
   - causal: the answer explains why something happened ("Why did X?" → the cause)
   - procedural: the answer explains how a process works ("How does X work?" → the process)

## Output Format

Return ONLY a JSON array. Each element:
{"id":"<id>","interrogative":"<val>","cardinality":"<val>","entity_type":"<val>","answer_form":"<val>","relational_context":"<val>"}

No explanations, no markdown formatting, just the raw JSON array."""


def build_user_prompt(questions):
    """Build the user prompt for a batch of questions."""
    lines = ["Classify these questions:\n"]
    for q in questions:
        lines.append(f'ID: {q["id"]}')
        lines.append(f'Q: {q["question"]}')
        lines.append(f'A: {q["answer"]}')
        lines.append('')
    return '\n'.join(lines)


def parse_response(text):
    """Extract JSON array from response text."""
    text = text.strip()
    # Handle markdown code blocks
    if text.startswith('```'):
        text = text.split('\n', 1)[1]  # remove first line
        text = text.rsplit('```', 1)[0]  # remove last ```
        text = text.strip()
    return json.loads(text)


def load_existing_results():
    """Load partial results if they exist (for resuming)."""
    if os.path.exists(PARTIAL_FILE):
        with open(PARTIAL_FILE) as f:
            data = json.load(f)
        print(f'Loaded {len(data)} existing results from partial file')
        return data
    return []


def main():
    # Load SQuAD
    print('Loading SQuAD...')
    with open(SQUAD_PATH) as f:
        data = json.load(f)

    # Collect all answerable questions
    answerable = []
    for article in data['data']:
        for para in article['paragraphs']:
            for qa in para['qas']:
                if not qa.get('is_impossible', False):
                    answers = qa.get('answers', [])
                    if answers:
                        answerable.append({
                            'id': qa['id'],
                            'question': qa['question'],
                            'answer': answers[0]['text'],
                            'article': article['title']
                        })

    print(f'Total answerable questions: {len(answerable)}')

    # Load existing results for resuming
    existing = load_existing_results()
    classified_ids = {r['id'] for r in existing}
    remaining = [q for q in answerable if q['id'] not in classified_ids]
    print(f'Already classified: {len(existing)}')
    print(f'Remaining: {len(remaining)}')

    if not remaining:
        print('All questions already classified!')
        # Save final output
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(existing, f, indent=2)
        print(f'Saved to {OUTPUT_FILE}')
        return

    # Initialize client
    client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var

    all_results = existing.copy()
    errors = []

    # Process in batches
    total_batches = (len(remaining) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f'\nProcessing {len(remaining)} questions in {total_batches} batches of {BATCH_SIZE}...\n')

    for batch_idx in range(0, len(remaining), BATCH_SIZE):
        batch = remaining[batch_idx:batch_idx + BATCH_SIZE]
        batch_num = batch_idx // BATCH_SIZE + 1

        print(f'Batch {batch_num}/{total_batches} ({len(batch)} questions)...', end=' ')

        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": build_user_prompt(batch)}
                ]
            )

            result_text = response.content[0].text
            batch_results = parse_response(result_text)

            # Add question/answer text back for reference
            id_to_qa = {q['id']: q for q in batch}
            for r in batch_results:
                if r['id'] in id_to_qa:
                    r['question'] = id_to_qa[r['id']]['question']
                    r['answer'] = id_to_qa[r['id']]['answer']

            all_results.extend(batch_results)
            print(f'OK ({len(batch_results)} classified)')

        except json.JSONDecodeError as e:
            print(f'JSON PARSE ERROR: {e}')
            errors.append({'batch': batch_num, 'error': str(e), 'ids': [q['id'] for q in batch]})
        except anthropic.APIError as e:
            print(f'API ERROR: {e}')
            errors.append({'batch': batch_num, 'error': str(e), 'ids': [q['id'] for q in batch]})
            # On rate limit, wait longer
            if 'rate' in str(e).lower():
                print('  Rate limited, waiting 30s...')
                time.sleep(30)

        # Save progress every 50 questions
        if len(all_results) % 50 == 0 or batch_idx + BATCH_SIZE >= len(remaining):
            with open(PARTIAL_FILE, 'w') as f:
                json.dump(all_results, f, indent=2)

        time.sleep(DELAY)

    # Save final results
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(all_results, f, indent=2)

    print(f'\n{"="*60}')
    print(f'DONE')
    print(f'Total classified: {len(all_results)}')
    print(f'Errors: {len(errors)}')
    print(f'Saved to: {OUTPUT_FILE}')

    if errors:
        error_file = os.path.join(OUTPUT_DIR, 'classification_errors.json')
        with open(error_file, 'w') as f:
            json.dump(errors, f, indent=2)
        print(f'Errors saved to: {error_file}')
        print('Re-run the script to retry failed batches (it resumes from where it left off)')


if __name__ == '__main__':
    main()
