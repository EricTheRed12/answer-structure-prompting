# Answer Structure Taxonomy — Final (10 Classes)

Derived from SQuAD dev set (5,928 answerable questions).
Each class maps to a unique answer structure schema.
Schemas use two common pre-filled fields (answer_type, answer) + class-specific empty dimensions.

---

## Class 1: Object Identification
**Description:** The answer names or identifies a concrete object, entity, document, technology, or substance.
**Example Q:** "What is the name of the CBS affiliate in Fresno?" → "KGPE"
**Schema:**
```json
{
  "answer_type": "single",
  "answer": "object",
  "object": "",
  "relation": ""
}
```
**Est. count:** ~1000

---

## Class 2: Concept/Person Identification
**Description:** The answer identifies an abstract concept, classification, or person by a defining property.
**Example Q:** "What are both Branko Milanovic and Joseph Stiglitz?" → "Economist"
**Schema:**
```json
{
  "answer_type": "single",
  "answer": "concept or person",
  "identity": "",
  "defining_property": ""
}
```
**Est. count:** ~500

---

## Class 3: Multipart Identification
**Description:** The answer requires identifying multiple distinct components.
**Example Q:** "What does Warsaw host many of?" → "events and festivals"
**Schema:**
```json
{
  "answer_type": "multiple",
  "answer": "list",
  "components": [],
  "shared_category": ""
}
```
**Est. count:** ~370

---

## Class 4: Quantitative
**Description:** The answer is a number: a count, measurement, proportion, or recorded statistic.
**Example Q:** "How many volumes does the University of Chicago Library hold?" → "9.8 million"
**Schema:**
```json
{
  "answer_type": "single",
  "answer": "quantity",
  "quantity": "",
  "unit": "",
  "measurement_context": ""
}
```
**Est. count:** ~635

---

## Class 5: Temporal
**Description:** The answer is a time expression: a date, year, era, duration, or range.
**Example Q:** "What year was Setanta Sports awarded Premier League rights?" → "2006"
**Schema:**
```json
{
  "answer_type": "single",
  "answer": "time",
  "event": "",
  "time_expression": "",
  "temporal_type": ""
}
```
**Est. count:** ~595

---

## Class 6: Place
**Description:** The answer is a geographic location or spatial reference.
**Example Q:** "Where does the Rhine river's measurement begin?" → "Old Rhine Bridge at Constance"
**Schema:**
```json
{
  "answer_type": "single",
  "answer": "location",
  "location": "",
  "relation": ""
}
```
**Est. count:** ~505

---

## Class 7: Agent
**Description:** The answer is who or what performed an action.
**Example Q:** "Who challenged Kublai Khan's right to succeed?" → "Ariq Böke"
**Schema:**
```json
{
  "answer_type": "single",
  "answer": "agent",
  "agent": "",
  "action_performed": "",
  "object_of_action": ""
}
```
**Est. count:** ~540

---

## Class 8: Descriptive
**Description:** The answer describes a quality, property, or characteristic of something.
**Example Q:** "What kind of university is the California Institute of Technology?" → "private"
**Schema:**
```json
{
  "answer_type": "single",
  "answer": "quality",
  "quality": "",
  "description_domain": ""
}
```
**Est. count:** ~680

---

## Class 9: Causal
**Description:** The answer explains why something happened: the cause, reason, or enabling mechanism.
**Example Q:** "Why did Berlin Huguenots switch to German?" → "in protest against the occupation of Prussia by Napoleon"
**Schema:**
```json
{
  "answer_type": "single",
  "answer": "cause",
  "effect": "",
  "cause": "",
  "mechanism": ""
}
```
**Est. count:** ~330

---

## Class 10: Resultative
**Description:** The answer is the outcome, effect, or product of an action or event.
**Example Q:** "What did the use of steam engines in farming lead to?" → "increase in the land available for cultivation"
**Schema:**
```json
{
  "answer_type": "single",
  "answer": "outcome",
  "action": "",
  "actor": "",
  "outcome": ""
}
```
**Est. count:** ~400

---

## Summary

| # | Class | Est. Count | Ratio to Avg |
|---|---|---|---|
| 1 | Object Identification | ~1000 | 1.8x |
| 2 | Concept/Person Identification | ~500 | 0.9x |
| 3 | Multipart Identification | ~370 | 0.7x |
| 4 | Quantitative | ~635 | 1.1x |
| 5 | Temporal | ~595 | 1.1x |
| 6 | Place | ~505 | 0.9x |
| 7 | Agent | ~540 | 1.0x |
| 8 | Descriptive | ~680 | 1.2x |
| 9 | Causal | ~330 | 0.6x |
| 10 | Resultative | ~400 | 0.7x |

**Total:** ~5,555 (+ ~373 from rare classes absorbed into nearest neighbor = 5,928)
**Average:** ~555 per class
**Ratio (largest/smallest):** 3.0x
**Classes:** 10
**Classifier target:** BERT-style encoder, single-label classification

---

## Design Rationale

- Each class produces a structurally distinct schema — the model receives different dimensional guidance for each.
- Schemas contain two common pre-filled fields (answer_type, answer) that provide immediate signal about what kind of answer is expected. Remaining fields are class-specific and empty.
- Classes are defined by the relational role the answer plays, not by interrogative or surface form.
- The taxonomy is static and predefined prior to inference.
- Derived from 5,928 SQuAD questions classified by 5 features (interrogative, cardinality, entity type, answer form, relational context). Features were used for derivation; the final taxonomy is the 10 resulting classes.
- The framework is domain-agnostic; this taxonomy is scoped to extractive QA on SQuAD. Extension to other domains requires re-derivation.
