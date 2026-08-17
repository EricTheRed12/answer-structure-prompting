import json

with open('/Users/core/Documents/GradSchool/CS699/rational-thinking/squad_dev.json') as f:
    data = json.load(f)

print(f'Version: {data["version"]}')
print(f'Number of articles: {len(data["data"])}')

total_q = sum(len(p['qas']) for article in data['data'] for p in article['paragraphs'])
print(f'Total questions: {total_q}')

print(f'\nFirst 5 articles: {[a["title"] for a in data["data"][:5]]}')

# Pull first 50 questions with their answers
print('\n--- FIRST 50 QUESTIONS WITH ANSWERS ---\n')
count = 0
for article in data['data']:
    for para in article['paragraphs']:
        for qa in para['qas']:
            if count >= 50:
                break
            question = qa['question']
            if qa.get('is_impossible', False):
                answer = '[UNANSWERABLE]'
            else:
                answers = qa.get('answers', [])
                answer = answers[0]['text'] if answers else '[NO ANSWER]'
            print(f'{count+1}. Q: {question}')
            print(f'   A: {answer}')
            print()
            count += 1
        if count >= 50:
            break
    if count >= 50:
        break
