# Answer Structure Taxonomy v1

19 classes derived from SQuAD dev set (1000-question sample).
Pending validation against full 5,928-question classification.

---

## Identification Family

### 1. Thing — Label/Name
**Features:** what / singular / thing / noun / identificatory (sub: label)
**Description:** The answer names or labels a concrete thing.
**Example:** "What is the conventional method to measure the Rhine?" → "Rhine-kilometers"
**Schema:**
```json
{
  "answer_type": "thing",
  "relation": "label",
  "subject": "",
  "name": "",
  "context": ""
}
```
**Est. count:** ~80

---

### 2. Thing — Functional
**Features:** what / singular / thing / noun / identificatory (sub: functional)
**Description:** The answer identifies a thing by the function it serves.
**Example:** "What co-receptor recruits molecules inside the T cell?" → "CD4 co-receptor"
**Schema:**
```json
{
  "answer_type": "thing",
  "relation": "functional",
  "function": "",
  "thing": "",
  "operational_context": ""
}
```
**Est. count:** ~48

---

### 3. Concept — Definition
**Features:** what / singular / concept / noun / identificatory (sub: definition)
**Description:** The answer defines or identifies an abstract concept.
**Example:** "What are both Branko Milanovic and Joseph Stiglitz?" → "Economist"
**Schema:**
```json
{
  "answer_type": "concept",
  "relation": "definition",
  "subject": "",
  "definition": "",
  "category": ""
}
```
**Est. count:** ~75

---

### 4. Concept — Attribute
**Features:** what / singular / concept / noun / identificatory (sub: attribute)
**Description:** The answer identifies a specific property or attribute of a concept.
**Example:** "The house is a notable example of what type of architecture?" → "Renaissance"
**Schema:**
```json
{
  "answer_type": "concept",
  "relation": "attribute",
  "subject": "",
  "attribute": "",
  "attribute_domain": ""
}
```
**Est. count:** ~60

---

### 5. Person — Identificatory
**Features:** who / singular / person / noun / identificatory
**Description:** The answer identifies a person by a defining property (not by an action they performed).
**Example:** "What is the name of the Pulitzer Prize novelist who was also a university alumni?" → "Philip Roth"
**Schema:**
```json
{
  "answer_type": "person",
  "relation": "identificatory",
  "person": "",
  "identifying_property": "",
  "context": ""
}
```
**Est. count:** ~11

---

### 6. Multipart Identificatory
**Features:** what / multipart / (thing|concept) / noun / identificatory
**Description:** The answer requires identifying multiple distinct components.
**Example:** "What does Warsaw host many of?" → "events and festivals"
**Schema:**
```json
{
  "answer_type": "composite",
  "relation": "identificatory",
  "cardinality": "multipart",
  "subject": "",
  "components": [],
  "relationship_between_components": ""
}
```
**Est. count:** ~34

---

## Quantitative Family

### 7. Quantitative — Count/Measurement
**Features:** how / singular / number / noun / quantitative (sub: count or measurement)
**Description:** The answer is a discrete count or a scalar measurement derived from context.
**Example:** "How many volumes does the University of Chicago Library system hold?" → "9.8 million"
**Example:** "How far is it from X to Y?" → "200 km"
**Schema:**
```json
{
  "answer_type": "number",
  "relation": "count_measurement",
  "subject": "",
  "quantity": "",
  "unit": "",
  "counted_thing": ""
}
```
**Est. count:** ~63

---

### 8. Quantitative — Proportion
**Features:** how / singular / number / noun / quantitative (sub: proportion)
**Description:** The answer is a part-of-whole relationship (fraction, percentage).
**Example:** "How much of the carbon is stored in the Amazon?" → "10%"
**Schema:**
```json
{
  "answer_type": "number",
  "relation": "proportion",
  "whole": "",
  "part": "",
  "proportion": "",
  "unit": ""
}
```
**Est. count:** ~25

---

### 9. Quantitative — Statistic
**Features:** what / singular / number / noun / quantitative
**Description:** The answer is a known recorded value — a fixed attribute/fact about a subject.
**Example:** "What is the lowest recorded temperature in Victoria?" → "−11.7 °C"
**Schema:**
```json
{
  "answer_type": "number",
  "relation": "statistic",
  "subject": "",
  "value": "",
  "unit": "",
  "qualifier": "",
  "attribute_of": ""
}
```
**Est. count:** ~19

---

## Temporal Family

### 10. Temporal — Point
**Features:** when / singular / time / noun / temporal (sub: point)
**Description:** The answer is a specific moment or date.
**Example:** "What year was Setanta Sports awarded Premier League rights?" → "2006"
**Schema:**
```json
{
  "answer_type": "time",
  "relation": "temporal_point",
  "event": "",
  "time_expression": "",
  "precision": ""
}
```
**Est. count:** ~60

---

### 11. Temporal — Duration/Range
**Features:** when / singular / time / noun / temporal (sub: duration or range)
**Description:** The answer is a span of time (how long) or a bounded period (between X and Y).
**Example:** "For how long did the plague stick around?" → "3 years"
**Example:** "Between what years did the uprising occur?" → "1702–1715"
**Schema:**
```json
{
  "answer_type": "time",
  "relation": "temporal_span",
  "event": "",
  "start": "",
  "end": "",
  "duration": ""
}
```
**Est. count:** ~27

---

## Spatial Family

### 12. Place — Spatial
**Features:** where / singular / place / noun / locative (sub: spatial)
**Description:** The answer is a location in pure spatial terms — where something physically is.
**Example:** "Where does the Rhine river's measurement begin?" → "Old Rhine Bridge at Constance"
**Schema:**
```json
{
  "answer_type": "place",
  "relation": "spatial",
  "subject": "",
  "location": "",
  "spatial_relation": ""
}
```
**Est. count:** ~55

---

### 13. Place — Contextual
**Features:** what / singular / place / noun / (locative|identificatory) (sub: contextual)
**Description:** The answer is a place identified through a contextual or functional relationship, not pure location.
**Example:** "Are there any regions where the Treaty excludes from jurisdiction?" → "the Faroe Islands"
**Schema:**
```json
{
  "answer_type": "place",
  "relation": "contextual",
  "subject": "",
  "location": "",
  "contextual_relation": "",
  "governing_condition": ""
}
```
**Est. count:** ~35

---

## Agent Family

### 14. Agent — Person
**Features:** who / singular / person / noun / agent
**Description:** The answer is a person who performed an action.
**Example:** "Who challenged Kublai Khan's right to succeed?" → "Ariq Böke"
**Schema:**
```json
{
  "answer_type": "person",
  "relation": "agent",
  "agent": "",
  "action_performed": "",
  "object_of_action": ""
}
```
**Est. count:** ~54

---

### 15. Agent — Thing
**Features:** what / singular / thing / noun / agent
**Description:** The answer is a non-human entity that performed or caused an action.
**Example:** "What co-receptor recruits molecules inside the T cell that are responsible for cell activation?" → "CD4 co-receptor"
**Schema:**
```json
{
  "answer_type": "thing",
  "relation": "agent",
  "agent": "",
  "action_performed": "",
  "object_of_action": "",
  "mechanism": ""
}
```
**Est. count:** ~16

---

## Relational Family

### 16. Descriptive
**Features:** what / singular / concept / (adjective|noun) / descriptive
**Description:** The answer describes a quality or property of something.
**Example:** "Southern California's economy can be described as... what other characteristic?" → "diverse"
**Schema:**
```json
{
  "answer_type": "concept",
  "relation": "descriptive",
  "subject": "",
  "quality": "",
  "quality_domain": ""
}
```
**Est. count:** ~39

---

### 17. Instrumental
**Features:** what / singular / (thing|concept) / noun / instrumental
**Description:** The answer is what was used or needed to accomplish something.
**Example:** "What is used to estimate emissions?" → "default emission factors"
**Schema:**
```json
{
  "answer_type": "thing",
  "relation": "instrumental",
  "instrument": "",
  "action_enabled": "",
  "actor": ""
}
```
**Est. count:** ~33

---

### 18. Causal
**Features:** (what|why) / singular / concept / (noun|clause) / causal
**Description:** The answer explains why something happened — the cause or reason.
**Example:** "Messiaen says that composition with prime numbers was inspired by what?" → "the movements of nature"
**Example:** "Why did Berlin Huguenots switch to German?" → "in protest against the occupation of Prussia by Napoleon"
**Schema:**
```json
{
  "answer_type": "concept",
  "relation": "causal",
  "effect": "",
  "cause": "",
  "mechanism": ""
}
```
**Est. count:** ~32

---

### 19. Resultative
**Features:** what / singular / concept / noun / resultative
**Description:** The answer is the outcome or effect of an action or event.
**Example:** "What were early drivers looking to generate when they fastened safety valves down?" → "more power"
**Schema:**
```json
{
  "answer_type": "concept",
  "relation": "resultative",
  "action": "",
  "actor": "",
  "outcome": "",
  "context": ""
}
```
**Est. count:** ~18

---

## Summary

| # | Class | Family | Est. Count (sample) | Est. Count (full) |
|---|---|---|---|---|
| 1 | Thing — Label/Name | Identification | ~80 | ~475 |
| 2 | Thing — Functional | Identification | ~48 | ~285 |
| 3 | Concept — Definition | Identification | ~75 | ~445 |
| 4 | Concept — Attribute | Identification | ~60 | ~356 |
| 5 | Person — Identificatory | Identification | ~11 | ~65 |
| 6 | Multipart Identificatory | Identification | ~34 | ~202 |
| 7 | Quantitative — Count/Measurement | Quantitative | ~63 | ~374 |
| 8 | Quantitative — Proportion | Quantitative | ~25 | ~148 |
| 9 | Quantitative — Statistic | Quantitative | ~19 | ~113 |
| 10 | Temporal — Point | Temporal | ~60 | ~356 |
| 11 | Temporal — Duration/Range | Temporal | ~27 | ~160 |
| 12 | Place — Spatial | Spatial | ~55 | ~326 |
| 13 | Place — Contextual | Spatial | ~35 | ~208 |
| 14 | Agent — Person | Agent | ~54 | ~320 |
| 15 | Agent — Thing | Agent | ~16 | ~95 |
| 16 | Descriptive | Relational | ~39 | ~231 |
| 17 | Instrumental | Relational | ~33 | ~196 |
| 18 | Causal | Relational | ~32 | ~190 |
| 19 | Resultative | Relational | ~18 | ~107 |
| | **TOTAL** | | **~784*** | **~4,652*** |

*Remaining ~216 from rare classes would be absorbed into nearest neighbor.

---

## Notes

- Sub-splits for classes 1–4, 6 are hypothesized from the 1000-sample.
  Pending validation: full 5,928-question run will confirm counts and whether sub-splits hold.
- The 94 rare classes (~216 questions) need to be mapped to their nearest taxonomy class.
- Schemas are STATIC per class. The generator sees the schema as context, not as a template to fill.
- Each class maps to one scaffold (schema + worked examples + question).
