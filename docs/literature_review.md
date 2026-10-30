# SurveyML-Eval: Literature Review and Research Gap Analysis

## 1. Purpose

This document reviews existing research on evaluating Large Language Models (LLMs) in statistical reasoning, statistical code generation, data-based reasoning, population-level statistical realism, and complex survey analysis.

The purpose is to identify the existing research landscape and establish a defensible research-gap hypothesis for SurveyML-Eval.

This is a preliminary literature review based on the identified sources. It is not an exhaustive systematic review.

## 2. Review of Existing Research

### 2.1 StatQA — NeurIPS 2024

**Title:** Are Large Language Models Good Statisticians?

**Authors:** Yizhang Zhu, Shiyin Du, Boyan Li, Yuyu Luo, and Nan Tang.

**Publication:** NeurIPS 2024, Datasets and Benchmarks Track.

**DOI:** https://proceedings.neurips.cc/paper_files/paper/2024/file/729786203d330da046dd8091c2d92a66-Paper-Datasets_and_Benchmarks_Track.pdf

**Main contribution:**

StatQA introduces a benchmark containing 11,623 examples designed to evaluate LLM capabilities in statistical analysis tasks, particularly the applicability of statistical methods and hypothesis-testing procedures.

The research evaluates multiple LLMs and prompting approaches and investigates differences between human and LLM statistical errors.

**Relevance to SurveyML-Eval:**

StatQA establishes that statistical reasoning and method applicability are already recognized benchmark research areas.

**Research implication:**

SurveyML-Eval must not claim novelty simply from evaluating LLMs on statistical questions. Its contribution must be grounded in a more specific applied workflow.

Source: https://proceedings.neurips.cc/paper_files/paper/2024/file/729786203d330da046dd8091c2d92a66-Paper-Datasets_and_Benchmarks_Track.pdf

### 2.2 QRData — Findings of ACL 2024

**Title:** Are LLMs Capable of Data-based Statistical and Causal Reasoning? Benchmarking Advanced Quantitative Reasoning with Data.

**Authors:** Xiao Liu, Zirui Wu, Xueqing Wu, Pan Lu, Kai-Wei Chang, and Yansong Feng.

**Publication:** Findings of the Association for Computational Linguistics: ACL 2024.

**DOI:** https://doi.org/10.18653/v1/2024.findings-acl.548

**Main contribution:**

QRData evaluates statistical and causal reasoning using real-world data. It contains 411 questions accompanied by data sheets and an additional 290 text-only questions.

The study investigates natural-language reasoning, program-based reasoning, and agent-based approaches.

**Relevance to SurveyML-Eval:**

QRData demonstrates the importance of evaluating statistical reasoning with actual data rather than relying exclusively on theoretical questions.

**Research implication:**

SurveyML-Eval should emphasize realistic analytical workflows, data interpretation, and methodological decision-making rather than isolated statistical questions.

Source: https://aclanthology.org/2024.findings-acl.548/

### 2.3 StatEval — 2025 Preprint

**Title:** StatEval: A Comprehensive Benchmark for Large Language Models in Statistics.

**Publication:** arXiv preprint, October 2025.

**arXiv:** https://arxiv.org/abs/2510.09517

**Main contribution:**

StatEval proposes a broad statistical benchmark with 13,817 foundational problems and 2,374 research-level proof tasks.

It includes human-in-the-loop validation and evaluations across different statistical difficulty levels.

**Relevance to SurveyML-Eval:**

This work demonstrates that broad statistical benchmark construction is already an active research direction.

**Research implication:**

SurveyML-Eval should remain narrowly focused on applied survey-weighted predictive machine learning rather than attempting to build another general statistics benchmark.

### 2.4 StatLLM — Scientific Data, 2026

**Title:** StatLLM: A Dataset for Evaluating the Performance of Large Language Models in Statistical Analysis.

**Authors:** Xinyi Song, Lina Lee, Kexin Xie, Xueying Liu, Xinwei Deng, and Yili Hong.

**Publication:** Scientific Data, February 2026.

**DOI:** https://doi.org/10.1038/s41597-026-06731-4

**Main contribution:**

StatLLM provides 207 statistical analysis tasks, LLM-generated SAS code, human-verified reference code, and expert evaluation scores.

Its evaluation considers code correctness, readability, executability, and output quality.

**Relevance to SurveyML-Eval:**

StatLLM demonstrates the importance of human-verified reference solutions and expert assessment of LLM-generated statistical code.

**Research implication:**

SurveyML-Eval should use transparent reference solutions, explicit scoring rubrics, code execution checks, and human-reviewed evaluation.

Source: https://www.nature.com/articles/s41597-026-06731-4

### 2.5 SSDataBench — PNAS, May 2026

**Title:** Evaluating the Statistical Realism of LLM-generated Social Science Data.

**Authors:** Yueqi Xie and colleagues.

**Publication:** Proceedings of the National Academy of Sciences, May 2026.

**DOI:** https://doi.org/10.1073/pnas.2538145123

**Main contribution:**

SSDataBench evaluates population-level statistical realism in LLM-generated social science data.

It evaluates 15 LLMs using four longitudinal and three cross-sectional survey datasets across five statistical pattern types:

1. Univariate distributions.
2. Bivariate associations.
3. Multivariate outcome predictions.
4. Life event sequence distributions.
5. Associations between life event sequences and covariates.

The study identifies limitations in the ability of LLMs to reproduce population-level heterogeneity and statistical patterns.

**Relevance to SurveyML-Eval:**

This work is directly relevant to survey-based statistical evaluation and population-level validity.

**Research implication:**

SurveyML-Eval must distinguish evaluating the statistical realism of generated synthetic data from evaluating whether LLMs can correctly perform and justify predictive machine learning analyses on survey data.

Source: https://www.pnas.org/doi/10.1073/pnas.2538145123

### 2.6 Trusting Your LLM — Mathematica, March 2026

**Title:** Trusting Your LLM: A Framework for Evaluating AI Models on Complex Statistical Data.

**Authors:** Andrés Nigenda, Dallas Dotter, and Camille Shao.

**Publisher:** Mathematica.

**Publication date:** March 6, 2026.

**Main contribution:**

This work introduces a framework for evaluating LLMs on complex, survey-based statistical data.

It uses 35 validated descriptive and causal questions based on American Community Survey Public Use Microdata Sample data.

It compares reasoning-only and code-execution workflows and highlights the importance of data access, metadata, structured prompts, and controlled analytical execution.

**Relevance to SurveyML-Eval:**

This work directly overlaps with the applied complex-survey analysis motivation of SurveyML-Eval.

**Research implication:**

SurveyML-Eval cannot claim that complex survey analysis has not previously been evaluated. Its proposed contribution must be differentiated through the integration of survey-weighted predictive modelling, leakage-safe validation, and external population validation.

Source: https://www.mathematica.org/publications/trusting-your-llm

### 2.7 SurveyUQBench — September 2026

**Title:** SurveyUQBench: Recovering Complex-Survey Designs and Design-Based Uncertainty from Official Documentation.

**Author:** Junxi Zhou.

**Publication:** Exploring Science Academic Conference Series, Volume 16, September 2026.

**DOI:** https://doi.org/10.70267/aitia.2026456464

**Main contribution:**

SurveyUQBench introduces a benchmark of 360 tasks from 12 public survey programmes.

It evaluates the recovery of survey weights, strata, primary sampling units, replicate-weight conventions, domain rules, degrees of freedom, and confidence-interval procedures.

The resource includes official-document evidence, reference R analyses, and deterministic graders.

**Relevance to SurveyML-Eval:**

This work directly overlaps with complex survey design interpretation and design-based uncertainty evaluation.

**Research implication:**

SurveyML-Eval should not position basic survey-design recovery or design-based uncertainty assessment as its unique contribution.

Instead, it should investigate how survey-design considerations interact with predictive modelling, leakage prevention, and external validation.

Source: https://journals.zeuspress.org/index.php/conference/article/view/1349

## 3. Comparative Research Landscape

| Research | Statistical reasoning | Survey data | Code evaluation | Population validity | Predictive workflow under shift |
|---|---|---|---|---|---|
| StatQA | Yes | Not its central focus | Statistical task evaluation | Not its central focus | Not its central focus |
| QRData | Yes | Real-world data | Program-based reasoning | Not its central focus | Not its central focus |
| StatEval | Yes | Not its central focus | Computational and proof tasks | Not its central focus | Not its central focus |
| StatLLM | Yes | Multiple datasets | Yes, SAS code | Not its central focus | Not its central focus |
| SSDataBench | Yes | Yes | Not its central focus | Yes | Not its central focus |
| Trusting Your LLM | Yes | Yes | Yes, code execution | Applied population estimates | Not established as its central focus |
| SurveyUQBench | Yes | Yes | Yes, reference R analyses | Design-based uncertainty | Not established as its central focus |

This table summarizes the reviewed publications and descriptions. It does not establish that an unlisted capability is absent from the full underlying research.

## 4. Identified Research Gap

The reviewed studies establish several important research directions:

- General statistical reasoning has been benchmarked.
- Data-based statistical and causal reasoning has been evaluated.
- Statistical code generation has been evaluated using expert-reviewed reference solutions.
- Population-level statistical realism has been studied using social science survey data.
- Complex survey analysis and design-based uncertainty have been addressed by recent evaluation frameworks.

Therefore, the research gap should not be framed as the absence of LLM statistical benchmarks or the absence of survey-related LLM evaluations.

The proposed research-gap hypothesis is narrower:

**There may be value in a unified evaluation framework that examines whether LLMs can integrate survey-design considerations with leakage-safe predictive machine learning and external population validation under distribution shift.**

This combination will be investigated through controlled benchmark tasks and reproducible experiments.

The novelty hypothesis remains provisional until a broader systematic literature review confirms the extent of existing coverage.

## 5. Proposed Contribution of SurveyML-Eval

SurveyML-Eval proposes to investigate the following integrated capabilities:

1. Interpreting survey design and sampling weights in predictive modelling contexts.
2. Selecting appropriate survey-aware modelling and validation strategies.
3. Identifying target leakage and preprocessing leakage.
4. Evaluating predictive performance under class imbalance.
5. Assessing generalization across external populations and distribution shifts.
6. Interpreting uncertainty, calibration, and model explanations.
7. Producing reproducible analytical workflows.
8. Maintaining methodological correctness across repeated model trials.

The contribution will be an evaluation benchmark and experimental analysis, not a claim that the underlying statistical methods themselves are new.

## 6. Research Gap to Benchmark Task Mapping

| Proposed contribution | Benchmark task families |
|---|---|
| Survey-design interpretation for predictive analysis | T01, T02 |
| Survey-weighted predictive modelling | T02 |
| Leakage-safe modelling | T03 |
| Validation strategy selection | T04 |
| Class imbalance evaluation | T05 |
| External validation and distribution shift | T06 |
| Missing data and uncertainty | T07 |
| Calibration and interpretability | T08 |

## 7. Limitations of the Current Literature Review

This review is preliminary and has several limitations:

1. It is based on a selected group of identified publications and resources.
2. It does not yet include a complete database search across all relevant research indexes.
3. The comparison table summarizes available publication descriptions and does not establish that unmentioned methods are absent from the full papers.
4. SurveyUQBench is a recent conference proceeding and should receive an independent assessment of its methodology, review process, and reproducibility.
5. The novelty hypothesis must be reassessed after a broader search covering survey-weighted prediction, complex survey machine learning, external validation, distribution shift, and LLM evaluation.

## 8. Preliminary Conclusion

Existing literature demonstrates substantial progress in statistical reasoning benchmarks, statistical programming evaluation, population-level statistical realism, and LLM-assisted complex survey analysis.

SurveyML-Eval will therefore focus on the interaction of survey design, predictive machine learning, leakage prevention, and external population validation.

The proposed contribution will be evaluated empirically rather than asserted in advance.

## 9. References

1. Zhu, Y., Du, S., Li, B., Luo, Y., & Tang, N. (2024). Are Large Language Models Good Statisticians? NeurIPS 2024. https://proceedings.neurips.cc/paper_files/paper/2024/file/729786203d330da046dd8091c2d92a66-Paper-Datasets_and_Benchmarks_Track.pdf

2. Liu, X., Wu, Z., Wu, X., Lu, P., Chang, K.-W., & Feng, Y. (2024). Are LLMs Capable of Data-based Statistical and Causal Reasoning? Findings of ACL 2024. https://doi.org/10.18653/v1/2024.findings-acl.548

3. Lu, Y., et al. (2025). StatEval: A Comprehensive Benchmark for Large Language Models in Statistics. arXiv:2510.09517. https://arxiv.org/abs/2510.09517

4. Song, X., Lee, L., Xie, K., Liu, X., Deng, X., & Hong, Y. (2026). StatLLM: A Dataset for Evaluating the Performance of Large Language Models in Statistical Analysis. Scientific Data. https://doi.org/10.1038/s41597-026-06731-4

5. Xie, Y., et al. (2026). Evaluating the Statistical Realism of LLM-generated Social Science Data. Proceedings of the National Academy of Sciences. https://doi.org/10.1073/pnas.2538145123

6. Nigenda, A., Dotter, D., & Shao, C. (2026). Trusting Your LLM: A Framework for Evaluating AI Models on Complex Statistical Data. Mathematica. https://www.mathematica.org/publications/trusting-your-llm

7. Zhou, J. (2026). SurveyUQBench: Recovering Complex-Survey Designs and Design-Based Uncertainty from Official Documentation. Exploring Science Academic Conference Series, 16. https://doi.org/10.70267/aitia.2026456464

---

**Document status:** Preliminary literature review and research-gap hypothesis. Further literature searching and verification are required before making definitive novelty claims.