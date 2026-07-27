---
inclusion: manual
---

# Thesis References & Citation Guide

This document is the canonical source of all papers for the thesis:
**"A Framework for Generative Contextual Reasoning Prompts to Improve Generalization and Accuracy of Few Parameter LLMs"**
— Eric Redman

When writing or editing any thesis section, use these citations. BibTeX keys match the `sample.bib` file. Add new entries to both this document and `sample.bib` when new papers are incorporated.

---

## 1. Large Language Models — Background

| BibTeX Key | Authors | Title | Venue / Year | arXiv / DOI |
|---|---|---|---|---|
| `vaswani2017attention` | Vaswani et al. | Attention Is All You Need | NeurIPS 2017 | [1706.03762](https://arxiv.org/abs/1706.03762) |
| `kaplan2020scaling` | Kaplan, McCandlish et al. (OpenAI) | Scaling Laws for Neural Language Models | arXiv 2020 | [2001.08361](https://arxiv.org/abs/2001.08361) |
| `brown2020gpt3` | Brown et al. (OpenAI) | Language Models are Few-Shot Learners (GPT-3) | NeurIPS 2020 | [2005.14165](https://arxiv.org/abs/2005.14165) |
| `naveed2024llmsurvey` | Naveed et al. | Large Language Models: A Survey | arXiv 2024 | [2402.06196](https://arxiv.org/abs/2402.06196) |
| `zhao2023llmsurvey` | Zhao et al. | A Survey of Large Language Models | arXiv 2023 | [2303.18223](https://arxiv.org/abs/2303.18223) |

**Usage:** Background on what an LLM is — the predictive/token-prediction mechanism, attention, and scale. `vaswani2017attention` is the foundational transformer paper. `kaplan2020scaling` is the scaling law paper needed for the problem statement.

---

## 2. Hallucinations

| BibTeX Key | Authors | Title | Venue / Year | arXiv / DOI |
|---|---|---|---|---|
| `zhang2023hallucination` | Zhang et al. | Siren's Song in the AI Ocean: A Survey on Hallucination in LLMs | arXiv 2023 | [2309.01219](https://arxiv.org/abs/2309.01219) |
| `ji2023hallucination` | Ji et al. | Survey of Hallucination in Natural Language Generation | ACM Computing Surveys 2023 | [2202.03629](https://arxiv.org/abs/2202.03629) |
| `huang2025hallucinationacl` | Huang et al. | (Hallucination findings) | ACL 2025 Findings | [ACL Anthology](https://aclanthology.org/2025.findings-acl.1199.pdf) |
| `rawte2025hallucination` | Rawte et al. | (Hallucination survey) | arXiv 2025 | [2602.06176](https://arxiv.org/pdf/2602.06176) |
| `acl2025hallong` | — | (Hallucination paper) | ACL 2025 Long | [ACL Anthology](https://aclanthology.org/2025.acl-long.1176/) |

**Usage:** For the Hallucinations subsection. Note: no single universally accepted definition exists — `ji2023hallucination` is the most-cited survey and provides the closest thing to a working definition.

---

## 3. Generalization & Scale

| BibTeX Key | Authors | Title | Venue / Year | arXiv / DOI |
|---|---|---|---|---|
| `kaplan2020scaling` | Kaplan et al. | Scaling Laws for Neural Language Models | arXiv 2020 | [2001.08361](https://arxiv.org/abs/2001.08361) |
| `hoffmann2022chinchilla` | Hoffmann et al. (DeepMind) | Training Compute-Optimal Large Language Models (Chinchilla) | NeurIPS 2022 | [2203.15556](https://arxiv.org/abs/2203.15556) |
| `empiricalgeneralization` | — | An Empirical Study on Reasoning and Generalization in Large Language Models | arXiv | [2504.07086](https://arxiv.org/abs/2504.07086) |
| `scalingreasoning` | — | Do Larger Language Models Imply Better Generalization? A Pretraining Scaling Law for Implicit Reasoning | arXiv 2025 | [2504.03635](https://arxiv.org/abs/2504.03635) |

**Usage:** For "Generalization at Scale" and the problem statement — supports the claim that more parameters → better performance, and that this has real costs.

---

## 4. The Cost of Scale (Problem Statement)

| BibTeX Key | Authors | Title | Venue / Year | arXiv / DOI |
|---|---|---|---|---|
| `kaplan2020scaling` | Kaplan et al. | Scaling Laws for Neural Language Models | arXiv 2020 | [2001.08361](https://arxiv.org/abs/2001.08361) |
| `strubell2019energy` | Strubell et al. | Energy and Policy Considerations for Deep Learning in NLP | ACL 2019 | [1906.02629](https://arxiv.org/abs/1906.02629) |
| `patterson2021carbon` | Patterson et al. | Carbon Emissions and Large Neural Network Training | arXiv 2021 | [2104.10350](https://arxiv.org/abs/2104.10350) |

**Usage:** Supports the argument that scale has real costs — compute, energy, accessibility — motivating the need for better small-model methods.

---

## 5. Mixture of Experts

| BibTeX Key | Authors | Title | Venue / Year | arXiv / DOI |
|---|---|---|---|---|
| `shazeer2017moe` | Shazeer et al. (Google) | Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer | ICLR 2017 | [1701.06538](https://arxiv.org/abs/1701.06538) |
| `fedus2022switchtransformer` | Fedus et al. | Switch Transformers: Scaling to Trillion Parameter Models | JMLR 2022 | [2101.03961](https://arxiv.org/abs/2101.03961) |

**Usage:** The foundational MoE papers for the Mixture of Experts subsection. `shazeer2017moe` introduces the gating mechanism. `fedus2022switchtransformer` is the modern large-scale implementation.

---

## 6. Prompt Engineering

| BibTeX Key | Authors | Title | Venue / Year | arXiv / DOI |
|---|---|---|---|---|
| `sahoo2024promptsurvey` | Sahoo et al. | A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications | arXiv 2024 | [2402.07927](https://arxiv.org/abs/2402.07927) |
| `wei2022cot` | Wei et al. (Google) | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models | NeurIPS 2022 | [2201.11903](https://arxiv.org/abs/2201.11903) |
| `yao2023tot` | Yao et al. | Tree of Thoughts: Deliberate Problem Solving with Large Language Models | NeurIPS 2023 | [2305.10601](https://arxiv.org/abs/2305.10601) |
| `wang2023selfconsistency` | Wang et al. | Self-Consistency Improves Chain of Thought Reasoning in Language Models | ICLR 2023 | [2203.11171](https://arxiv.org/abs/2203.11171) |
| `yao2022react` | Yao et al. | ReAct: Synergizing Reasoning and Acting in Language Models | ICLR 2023 | [2210.03629](https://arxiv.org/abs/2210.03629) |
| `brittle2024react` | — | On the Brittle Foundations of ReAct Prompting for Agentic Large Language Models | arXiv 2024 | [2405.13966](https://arxiv.org/abs/2405.13966) |
| `brown2020gpt3` | Brown et al. | Language Models are Few-Shot Learners (few-shot / n-shot) | NeurIPS 2020 | [2005.14165](https://arxiv.org/abs/2005.14165) |

**Usage:** Core section for the paper. `wei2022cot` is the primary CoT reference. `yao2023tot` and `wang2023selfconsistency` are CoT extensions. `yao2022react` + `brittle2024react` form a pair showing ReAct's promise and limitations. `brown2020gpt3` is the canonical few-shot/n-shot paper.

---

## 7. Question Answering & QuSAM

| BibTeX Key | Authors | Title | Venue / Year | arXiv / DOI |
|---|---|---|---|---|
| `ogden2013qusam` | Ogden et al. | QuASM: A System for Question Answering Using Semi-Structured Data | JCDL 2013 | [ACM DL](https://dl.acm.org/doi/10.1145/2467696.2467726) |
| `rajpurkar2016squad` | Rajpurkar et al. (Stanford) | SQuAD: 100,000+ Questions for Machine Comprehension of Text | EMNLP 2016 | [1606.05250](https://arxiv.org/abs/1606.05250) |
| `rajpurkar2018squad2` | Rajpurkar et al. | Know What You Don't Know: Unanswerable Questions for SQuAD | ACL 2018 | [1806.03822](https://arxiv.org/abs/1806.03822) |

**Usage:** `rajpurkar2016squad` / `rajpurkar2018squad2` are the dataset papers for experiments. `ogden2013qusam` is the structural antecedent to QuSAM used as the context schema.

---

## 8. Retrieval-Augmented Generation (RAG)

| BibTeX Key | Authors | Title | Venue / Year | arXiv / DOI |
|---|---|---|---|---|
| `lewis2020rag` | Lewis et al. (Facebook AI) | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | NeurIPS 2020 | [2005.11401](https://arxiv.org/abs/2005.11401) |
| `gao2023ragsurvey` | Gao et al. | Retrieval-Augmented Generation for Large Language Models: A Survey | arXiv 2023 | [2312.10997](https://arxiv.org/abs/2312.10997) |
| `mao2020questiondecomp` | — | Question Decomposition for Retrieval-Augmented Generation | — | (see docx notes) |

**Usage:** RAG subsection and methodology. `lewis2020rag` is the foundational paper. `gao2023ragsurvey` covers modular/speculative RAG variants.

---

## 9. Novel Contribution — Related / Closely Adjacent Work

| BibTeX Key | Authors | Title | Venue / Year | arXiv / DOI |
|---|---|---|---|---|
| `focused_cot` | — | Focused Chain-of-Thought: Efficient LLM Reasoning via Structured Input Information | arXiv | (see docx notes) |
| `autoprompting` | — | Explaining Patterns in Data with Language Models via Interpretable Autoprompting | arXiv | (see docx notes) |
| `patternmachines` | — | Large Language Models as General Pattern Machines | arXiv | (see docx notes) |
| `policyteacher` | — | Large Language Model as a Policy Teacher | arXiv | (see docx notes) |
| `syntheticdata` | — | Generative AI for Synthetic Data Generation: Methods, Challenges and the Future | arXiv | (see docx notes) |

**Usage:** These papers directly border the novel contribution. Use them in the Architecture and Related Work sections to position QuSAM-based context encoding as distinct from, but informed by, these approaches.

---

## 10. Benchmarks Referenced

| Name | Description | Citation |
|---|---|---|
| SQuAD v1.1 / v2.0 | Primary dataset for all 3 experiments | `rajpurkar2016squad` / `rajpurkar2018squad2` |
| MMLU | Massive Multitask Language Understanding | Hendrycks et al. 2021, [2009.03300](https://arxiv.org/abs/2009.03300) |
| BIG-Bench Hard | Challenging reasoning tasks beyond GPT-4 | Suzgun et al. 2022, [2210.09261](https://arxiv.org/abs/2210.09261) |
| HELM | Holistic Evaluation of Language Models | Liang et al. 2022, [2211.09110](https://arxiv.org/abs/2211.09110) |

---

## 11. Papers Still Needing Full Verification

These are in your notes but need confirmed authors/years before adding to `sample.bib`:

- [ ] "Response planning during question-answering: does deciding what to say involve deciding how to say it?"
- [ ] "How Do We Answer Complex Questions: Discourse Structure of Long-Form Answers" (2022)
- [ ] "First Ask Then Answer: A Framework Design for AI Dialogue Based on Supplementary Questioning"
- [ ] "Beyond Single Embeddings: Capturing Diverse Targets with Multi-Query Retrieval"
- [ ] "CoMM: Collaborative Multi-Agent, Multi-Reasoning-Path Prompting for Complex Problem Solving"
- [ ] "Focused Chain-of-Thought" — confirm full citation
- [ ] Mixture of Agents study — "A Large-Scale Study on the Development and Issues of Multi-Agent AI Systems"

---

## Quick Citation Style Note

This thesis uses `\bibliographystyle{alpha}`. Keys should follow the format `firstauthorYEARkeyword` (e.g., `wei2022cot`, `kaplan2020scaling`). When adding a new entry, add it to both this table and `Masters_Thesis/sample.bib`.
