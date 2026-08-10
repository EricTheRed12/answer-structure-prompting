import json
import random

with open('/Users/core/Documents/GradSchool/CS699/rational-thinking/squad_dev.json') as f:
    data = json.load(f)

# Collect all answerable questions with their answers
answerable = []
for article in data['data']:
    for para in article['paragraphs']:
        for qa in para['qas']:
            if not qa.get('is_impossible', False):
                answers = qa.get('answers', [])
                if answers:
                    answerable.append({
                        'question': qa['question'],
                        'answer': answers[0]['text'],
                        'article': article['title']
                    })

print(f'Total answerable questions: {len(answerable)}')
print(f'From {len(data["data"])} articles')

# Sample 100 from across articles
random.seed(42)
sample = random.sample(answerable, 100)

print('\n--- 100 SAMPLED QUESTIONS WITH ANSWERS ---\n')
for i, item in enumerate(sample):
    print(f'{i+1}. [{item["article"]}]')
    print(f'   Q: {item["question"]}')
    print(f'   A: {item["answer"]}')
    print()
