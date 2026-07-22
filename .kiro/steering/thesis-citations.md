---
inclusion: manual
---

# Citation Verification Tracker

Pull this file into context when reviewing or verifying citations for a section.

## ⭐ DEFERRED MILESTONE: Full-text verification (after ALL claims are done)

Once every section's claims are finalized, do a dedicated pass to verify EVERY cited paper against its FULL TEXT — not just the abstract/snippet.

Why: Abstracts can support a claim that the full paper actually qualifies, contradicts, or scopes narrowly.

Priorities flagged:
- `costofdownscaling2023` (confirm fact-recall-vs-ICL split holds as worded)
- `nonfactoid_taxonomy2022` (confirm non-factoid scope doesn't undercut general use)
- `xie2022icl` (confirm "uncertainty collapses with few examples" framing)
- Many bib entries have `author = "various"` placeholders — fix real author lists during this pass

---

## Hook Section (§1.1)

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `kaplan2020scaling` | Large models superior but resource-constrained | HIGH | arXiv (2700+ citations) | Unverified |
| `strubell2019energy` | Resource constraints | HIGH | ACL 2019 | Unverified |
| `patterson2021carbon` | Resource constraints | HIGH | arXiv (Google) | Unverified |
| `smalllmsready2024` | Small models compete with large | MEDIUM | arXiv | Unverified |
| `modelsizematters2024` | Small models compete with large | MEDIUM | arXiv | Unverified |
| `wei2022cot` | CoT can improve small model performance | HIGH | arXiv (highly cited) | Unverified |
| `cot_limitations2025` | CoT has shortcomings | MEDIUM | arXiv | Unverified |
| `cot_mirage2025` | CoT has shortcomings | MEDIUM | arXiv | Unverified |
| `lewis2020rag` | RAG can improve small models | HIGH | NeurIPS 2020 | Unverified |
| `rag_survey2023` | RAG has shortcomings | MEDIUM | arXiv | Unverified |
| `devlin2019bert` | Small models comprehend language | HIGH | NAACL 2019 | Unverified |
| `liu2019roberta` | Small models comprehend language | HIGH | arXiv | Unverified |
| `costofdownscaling2023` | Comprehension survives downscaling | MEDIUM | arXiv | Unverified |
| `liroth2002questions` | Finite question type classification | HIGH | COLING 2002 | Unverified |
| `nonfactoid_taxonomy2022` | Finite answer structures exist | HIGH | SIGIR 2022 | Unverified |

## Problem Statement (§1.2)

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `eloundou2023gpts` | LLMs are transformative (labor market impact) | MEDIUM | arXiv / Science 2024 | Unverified |
| `llm_critical_societal2024` | LLMs are transformative (healthcare, finance, law) | MEDIUM | arXiv | Unverified |
| `llmoverview2023` | LLMs are transformative (general survey) | MEDIUM | arXiv | Unverified |
| `liesenfeld2024closed` | Most capable are closed/proprietary | HIGH | Nature 2024 | Unverified |
| `kapoor2024societal` | Concentrated control limits contributions | MEDIUM | arXiv / ICML 2024 | Unverified |
| `bommasani2023fmti` | No external input on training; can't be audited | HIGH | arXiv (Stanford) | Unverified |
| `liesenfeld2024openwashing` | "Open-source" models aren't truly open | HIGH | ACM FAccT 2024 | Unverified |
| `strubell2019energy` | Environmental cost | HIGH | ACL 2019 | Unverified |
| `patterson2021carbon` | Environmental cost | HIGH | arXiv (Google) | Unverified |
| `modelsizematters2024` | Small models underperform | MEDIUM | arXiv | Unverified |
| `kaplan2020scaling` | Limited parametric capacity; hard cap | HIGH | arXiv (2700+ citations) | Unverified |
| `costofdownscaling2023` | Can't encode everything; brittleness | MEDIUM | arXiv | Unverified |
| `linguistic_competence_scale2025` | Linguistic competence survives scaling | MEDIUM | arXiv | Unverified |
| `emergent_reducedscale2024` | Emergent abilities in small models | MEDIUM | NAACL 2024 | Unverified |
| `slm_survey2024` | Small models accessible; domain training | MEDIUM | arXiv (Penn State) | Unverified |
| `domain_expert_smalllm2024` | Small models match domain experts | MEDIUM | arXiv | Unverified |
| `catastrophic_forgetting2023` | Specialization costs generality | MEDIUM | arXiv | Unverified |

## Purpose of the Paper (§1.3) — reviewed via web search

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `devlin2019bert` | Encoder classifier maps question → structure type | HIGH | NAACL 2019 | ✅ Verified (canonical fit) |
| `costofdownscaling2023` | Core mechanism: in-context ability survives down-scaling | MEDIUM | ICLR 2024 / arXiv | ✅ Verified; claim REWORDED to match |
| `xie2022icl` | Scaffold narrows probability space | HIGH | ICLR 2022 | ✅ NEW — direct fit |
| `liroth2002questions` | Answer structure inferable from question text | HIGH | COLING 2002 | ✅ Verified (canonical fit) |
| `nonfactoid_taxonomy2022` | Finite set of answer structure types exists | HIGH | SIGIR 2022 (Best Paper) | ✅ VERIFIED — direct hit |
| `smalllmsready2024` | Generator can be any small model | MEDIUM | arXiv | ✅ Keep |
| `slm_survey2024` | Generator can be any small model | MEDIUM | arXiv (Penn State) | ✅ NEW here |

## Lit Review §2.3 — Fine-Tuning and Parameter-Efficient Adaptation

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `peft_survey2024` | Weight modification is the established approach (claim 1) | HIGH | arXiv (comprehensive PEFT survey, Dec 2023) | Unverified — abstract confirms it's a systematic review of PEFT methods framing weight modification as standard |
| `hu2022lora` | LoRA: low-rank adaptation method (claim 2) | HIGH | ICLR 2022 | Unverified — canonical, thousands of citations |
| `houlsby2019adapters` | Adapters: parameter-efficient transfer (claim 2) | HIGH | ICML 2019 | Unverified — canonical, introduced the concept |
| `li2021prefixtuning` | Prefix tuning: continuous prompt optimization (claim 2) | HIGH | ACL 2021 | Unverified — canonical, well-known |
| `instructiontuning2022` | Instruction tuning improves zero-shot generalization (claim 2) | HIGH | arXiv (Google/DeepMind, Flan-2 paper) | Unverified — canonical instruction tuning paper; directly demonstrates generalization improvements across model classes. **REPLACED** `instructiontuning2023` (too narrow). |
| `catastrophic_forgetting2023` | Task-specific limitation; fine-tuning skews distribution toward fine-tuning tasks (claims 3, 4) | HIGH | ICLR 2024 | Unverified — abstract directly states "improving performance on tasks within the fine-tuning data distribution comes at the expense of capabilities on other tasks" and frames it as distribution skewing, not just forgetting. **Strong fit for claim 4's distribution-narrowing framing.** |
| `alignment_tax2024` | Fine-tuning degrades performance on knowledge/reasoning benchmarks (claim 4) | MEDIUM-HIGH | arXiv | Unverified — abstract directly states benchmark degradation during SFT; full text not read |
| `costofdownscaling2023` | ICL survives downscaling (claim 6) | MEDIUM | ICLR 2024 / arXiv | Unverified for §2.3 use specifically — verified for other sections in earlier passes |
| `linguistic_competence_scale2025` | Language understanding survives downscaling (claim 6) | MEDIUM | arXiv | Unverified for §2.3 use specifically |

### §2.3 Action Items (UPDATED)
- [x] ~~Replace `instructiontuning2023` with canonical instruction tuning citation~~ → replaced with Flan-2 paper (`instructiontuning2022`)
- [x] ~~Verify `catastrophic_forgetting2023` supports distribution-narrowing framing~~ → confirmed from abstract; ICLR 2024 publication
- [x] ~~Verify `peft_survey2024` provides general framing~~ → confirmed from abstract; comprehensive survey
- [ ] Full-text verification pass (deferred milestone)

## Lit Review §2.4 — Prompt Engineering and In-Context Learning

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `brown2020gpt3` | Prompt engineering definition; ICL mechanism; few-shot; zero-shot (claims 1, 2, 3, 6) | HIGH | NeurIPS 2020 | Unverified for §2.4 specifically — canonical |
| `sahoo2024promptsurvey` | System/instruction prompting as established categories (claim 2) | HIGH | arXiv 2024 (IIT Patna / Stanford / Amazon) | Unverified — comprehensive survey covering prompt engineering techniques systematically |
| `manyshot2024` | Many-shot prompting (claim 3) | HIGH | NeurIPS 2024 (Google DeepMind) | Unverified — canonical many-shot paper |
| `wei2022cot` | Chain-of-Thought prompting (claim 4) | HIGH | NeurIPS 2022 | Unverified for §2.4 — canonical |
| `yao2023tot` | Tree of Thoughts (claim 4) | HIGH | NeurIPS 2023 | Unverified for §2.4 — canonical |
| `wang2023selfconsistency` | Self-Consistency (claim 4) | HIGH | ICLR 2023 | Unverified for §2.4 — canonical |
| `prompt_control_theory2023` | Additional context narrows prediction space / prompts steer distributions (claim 5) | MEDIUM | arXiv (unreviewed) | Unverified — abstract directly supports "prompts steer output probability distributions" |
| `xie2022icl` | Few examples sharply reduce uncertainty over latent task (claim 6) | HIGH | ICLR 2022 | ✅ Verified in earlier passes |
| `costofdownscaling2023` | ICL survives downscaling (claim 7) | HIGH | ICLR 2024 | ✅ Verified — TL;DR directly states ICL withstands aggressive down-scaling |

### §2.4 Action Items
- [ ] Full-text verification pass (deferred milestone)
- [ ] Verify `sahoo2024promptsurvey` covers system/instruction prompting specifically (abstract confirms comprehensive survey, details TBD)
- [ ] Consider whether `prompt_control_theory2023` (unreviewed) needs replacement with a stronger venue citation

## Lit Review §2.6 — Unconstrained Prediction (REVISED)

| Citation | Claim | Confidence | Venue | Status |
|----------|-------|------------|-------|--------|
| `ji2023hallucination` | Claim 1: Definition of hallucination (output ≠ expected) | HIGH | ACM Computing Surveys 2023 | Unverified |
| `brown2020gpt3` | Claim 2: Autoregressive mechanism; no separate failure mode (supports premise, conclusion is ours) | HIGH | NeurIPS 2020 | Unverified |
| `llmreasoning_stochastic2024` | Claim 2: LLMs as stochastic pattern-matchers; supports "no separate failure mode" | MEDIUM | arXiv | Unverified |
| `godey2024softmax` | Claim 3: Small models cannot fully express target probability distribution (dimensional bottleneck) | HIGH | arXiv 2024 (Inria) | Unverified |
| `costofdownscaling2023` | Claim 3: Fact recall degrades before ICL; lower-resolution approximation | MEDIUM | ICLR 2024 / arXiv | Unverified |
| `lpsr2026` | Claim 4: Inference-time error compounding in autoregressive generation | HIGH | arXiv 2026 (under review) | Unverified |
| `exposure_bias_ilp2022` | Claim 4: Error propagation (training-side exposure bias); secondary support | MEDIUM | arXiv | Unverified |
| `prompt_control_theory2023` | Claim 5: Prompts steer output distributions; narrowing works | MEDIUM | arXiv (unreviewed) | Unverified |
| `brevity_constraints2025` | Claim 5: Constraining output form inverts model-size performance rankings | MEDIUM | arXiv (unreviewed) | Unverified |
| `costofdownscaling2023` | Claim 7: ICL withstands aggressive down-scaling | HIGH | ICLR 2024 / arXiv | Unverified |
| `olsson2022inductionheads` | Claim 7: ICL mechanistically driven by attention heads (architectural, not capacity-dependent) | HIGH | ACL 2023 / arXiv:2209.11895 | Unverified |
| `taskspecific_prompts2025` | Claim 7: Task-specific prompts provably improve ICL (matched > generic) | HIGH | AISTATS 2025 / arXiv:2503.02102 | Unverified |
| `blueprints_slm2025` | Claim 7: Structured task-matched guides improve SLM performance up to 20% without training | HIGH | ICML 2025 Workshop / arXiv:2506.08669 | Unverified |

### §2.6 Citation Decisions (this pass)

- **DROPPED** `hallucination_unified2024` from claim 1 — "world model" definition conflicts with our simpler "output ≠ expected" framing. `ji2023hallucination` alone is sufficient.
- **DROPPED** `hallucination_survey2024` and `zhang2023hallucination` — supported existence of problem but were not cited in actual claims; ambient support not needed.
- **DROPPED** `llmreasoning_stochastic2024` from claim 7 — replaced with stronger, more specific citations.
- **ADDED** `olsson2022inductionheads` — mechanistic support for ICL being architectural (attention heads).
- **ADDED** `taskspecific_prompts2025` — theoretical proof that task-specific prompts improve ICL.
- **ADDED** `blueprints_slm2025` — empirical evidence that matched structure helps SLMs specifically.
- Claim 6 has no citations (synthesis claim with cross-references only) — this is intentional.

## Lit Review §2.2 — Scale and Structure

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `kaplan2020scaling` | Scale is dominant performance predictor; capacity explanation | HIGH | arXiv (2700+ citations) | Unverified |
| `hoffmann2022chinchilla` | Compute-optimal scaling; model+data should scale equally | HIGH | NeurIPS 2022 (DeepMind) | Unverified |
| `brown2020gpt3` | GPT-3 vs GPT-2 jump demonstrates capacity gap | HIGH | NeurIPS 2020 | Unverified |
| `llmoverview2023` | More parameters → more connections encoded | MEDIUM | arXiv | Unverified |
| `smalllmsready2024` | Small models match large on specific tasks (gap is conditional) | MEDIUM | arXiv | Unverified |
| `modelsizematters2024` | Small models match large on specific tasks (gap is conditional) | MEDIUM | arXiv | Unverified |
| `costofdownscaling2023` | External context can close gap; scale ≠ completeness | MEDIUM | ICLR 2024 / arXiv | Unverified for §2.2 use |
| `math_reasoning_limits2024` | Large models still fail on multi-step/structured tasks | MEDIUM | arXiv | Unverified |
| `lrm_complexity2025` | Reasoning models collapse beyond certain complexity | MEDIUM | NeurIPS 2025 (Apple) | Unverified |
| `wei2022cot` | CoT imposes structure → improves reasoning | HIGH | arXiv (highly cited) | Unverified |
| `brevity_constraints2025` | Output form constraints invert large-vs-small rankings | MEDIUM | arXiv (unreviewed) | Unverified |
| `prompt_control_theory2023` | Prompts steer output probability distributions | MEDIUM | arXiv (unreviewed) | Unverified |
| `llmreasoning_stochastic2024` | LLM output is pattern-based, not genuine reasoning | MEDIUM | arXiv | Unverified |
| `liesenfeld2024closed` | Closed-source internals unverifiable (footnote) | HIGH | Nature 2024 | Unverified |

## Lit Review §2.1 — Large Language Models

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `vaswani2017attention` | Transformer architecture; self-attention | HIGH | NeurIPS 2017 | Unverified |
| `llmoverview2023` | LLM definition and overview | MEDIUM | arXiv | Unverified |
| `brown2020gpt3` | Token prediction; decoder pre-training; autoregressive decoding | HIGH | NeurIPS 2020 | Unverified |
| `devlin2019bert` | Encoder pre-training (masked LM) | HIGH | NAACL 2019 | Unverified |
| `exposure_bias_ilp2022` | Error propagation in autoregressive generation | MEDIUM | arXiv | Unverified |
| `llama3_2024` | Confirms autoregressive decoder for open models | HIGH | arXiv (Meta) | Unverified |
| `liesenfeld2024closed` | Closed models don't disclose internals (footnote) | HIGH | Nature 2024 | Unverified |
| `llmreasoning_stochastic2024` | LLMs as probability engines; stochastic nature | MEDIUM | arXiv | Unverified |

## §1.3 Applied Changes (from previous sessions)

- Generator claim: dropped `modelsizematters2024` (wrong support), added `slm_survey2024`
- Core-mechanism claim: kept `costofdownscaling2023`, REWORDED to credit surviving ICL ability
- Probability-space claim: replaced `llmreasoning_stochastic2024` with `xie2022icl` for §1.3 specifically
- Metadata bug FIXED: `llmreasoning_stochastic2024` bib year corrected 2024 → 2025

## Lit Review §2.7 — Question Classification in QA

| Citation | Claim it supports | Confidence | Venue | Status |
|----------|-------------------|------------|-------|--------|
| `liroth2002questions` | Claim 1: QC is well-established prior art (20+ years) | HIGH | COLING 2002 | Unverified |
| `nonfactoid_taxonomy2022` | Claim 1: Extended taxonomies across domains | HIGH | SIGIR 2022 | Unverified |
| `analogical_reasoning2022` | Claim 2: Analogical questions signal relational mapping | MEDIUM-HIGH | arXiv (Webb et al. 2022) | Unverified — supports claim from answer side rather than question-feature side; defensible but slightly indirect |
| `wei2022cot` | Claim 2: Multi-step questions require chained inference (demonstrated in practice) | HIGH | NeurIPS 2022 | Unverified for §2.7 use |
| `devlin2019bert` | Claim 3: Encoder architecture for classification | HIGH | NAACL 2019 | Unverified |
| `xu2019qc_bert` | Claim 3: Modern BERT-based QC achieves SOTA; QC improves QA accuracy | HIGH | arXiv:1908.05441 (U of Arizona + AI2, 2019) | Unverified — abstract directly states BERT QC achieves SOTA on TREC + domain benchmarks and improves QA by +1.7% |
| `blueprints_slm2025` | Claim 4: Adjacent work — reasoning blueprints per task category | MEDIUM | ICML 2025 Workshop (TTODLer-FM) | Unverified — workshop paper, not main-track peer review |
| `templaterl2025` | Claim 4: Adjacent work — template library matched to problems via RL | MEDIUM-HIGH | ACL Findings 2026 | Unverified — strong venue; constructs template library via MCTS |
| `dynamic_template_selection2025` | Claim 4: Adjacent work — classifier routes queries to templates | LOW-MEDIUM | arXiv:2511.20683 (unreviewed preprint) | Unverified — weakest citation; no venue; useful for due diligence on broad engagement |

### §2.7 Citation Notes
- Claim 5 has no citations (author synthesis) — intentional
- `analogical_reasoning2022` is slightly indirect for claim 2 (about LLMs doing analogical reasoning, not about question features per se) — defensible but flagged
- `dynamic_template_selection2025` is the weakest citation in this section (unreviewed, single author, no venue) — included to show breadth of engagement, not leaned on heavily
- `blueprints_slm2025` is a workshop paper — fine to cite but reviewer may note lack of full peer review

### §2.7 Action Items
- [ ] Full-text verification pass (deferred milestone)
- [ ] Verify `xu2019qc_bert` reports specific accuracy numbers on TREC benchmark (abstract confirms SOTA + QA improvement)
- [ ] Verify `templaterl2025` is accepted at ACL Findings 2026 (found in ACL anthology PDF, needs confirmation)
- [ ] Consider whether `analogical_reasoning2022` needs replacement with a question-features-specific paper

## Legacy Review Items

- [ ] Consider enhancing Hook Claim 3 to strengthen "comprehension survives scale" argument
- [ ] Verify `nonfactoid_taxonomy2022` defines answer types (not just question types)
- [ ] Verify `liroth2002questions` finite question type classification with learned classifier
