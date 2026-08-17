# Taxonomy Classification Task

You are classifying SQuAD questions according to 5 features that define answer structure types.

## Features

1. **interrogative** — The primary interrogative of the question.
   Values: `who`, `what`, `when`, `where`, `why`, `how`

2. **cardinality** — Whether the answer requires one piece of information or multiple distinct pieces.
   Values: `singular`, `multipart`

3. **entity_type** — The type of entity the answer represents.
   Values: `person`, `place`, `thing`, `time`, `number`, `concept`
   - person: a named individual or group of people
   - place: a geographic location, region, or spatial reference
   - thing: a concrete object, substance, document, organization, technology
   - time: a date, era, duration, or temporal expression
   - number: a quantity, measurement, percentage, or count
   - concept: an abstract idea, quality, relationship, or process description

4. **answer_form** — The grammatical form of the answer span.
   Values: `noun`, `verb`, `adjective`, `clause`
   - noun: a noun phrase (single word or multi-word)
   - verb: an action word or verb phrase
   - adjective: a descriptive word or quality
   - clause: a full or partial clause (subject+verb or longer)

5. **relational_context** — What role the answer plays relative to the question's action/framing. This is the most important differentiator.
   Values: `identificatory`, `agent`, `resultative`, `instrumental`, `role`, `locative`, `temporal`, `descriptive`, `quantitative`, `causal`, `procedural`
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

## Instructions

For each question below, provide a JSON object with the 5 features. Also include the question ID and the answer (provided for reference to help you classify accurately).

## Output Format

A JSON array. Each element should be:
```json
{
  "id": "<question_id>",
  "question": "<the question text>",
  "answer": "<the answer text>",
  "interrogative": "<value>",
  "cardinality": "<value>",
  "entity_type": "<value>",
  "answer_form": "<value>",
  "relational_context": "<value>"
}
```

## Important: File Output

Do NOT return the JSON in chat. Instead, write the JSON array directly to a file:

- For batch 1: write to `/Users/core/Documents/GradSchool/CS699/rational-thinking/taxonomy_classification/batch_01_results.json`
- For batch 2: write to `/Users/core/Documents/GradSchool/CS699/rational-thinking/taxonomy_classification/batch_02_results.json`
- ...and so on for each batch number.

After writing the file, just confirm it's done.

---

## Questions to Classify

