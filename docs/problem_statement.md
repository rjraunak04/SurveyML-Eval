# SurveyML-Eval: Evaluating Large Language Models on Survey-Weighted Machine Learning Under Distribution Shift

## 1. Abstract

Large Language Models (LLMs) are increasingly used to support statistical analysis and machine learning workflows. However, their ability to produce methodologically valid solutions in applied statistical settings remains an important evaluation challenge.

This project proposes SurveyML-Eval, a reproducible benchmark designed to evaluate LLM performance on survey-weighted machine learning and external validation under distribution shift.

The benchmark focuses on interconnected analytical challenges, including complex survey design, survey weights, predictive modelling, data leakage, validation strategy, class imbalance, missing data, uncertainty, calibration, and interpretability.

Unlike evaluations limited to isolated statistical questions, SurveyML-Eval will assess whether LLMs can make reliable analytical decisions across a structured applied workflow.

The benchmark will use controlled evaluation tasks, reference solutions, explicit scoring criteria, repeated model trials, and human-reviewed failure analysis. Experimental findings will be reported only after actual model evaluations have been completed.

## 2. Background and Motivation

LLMs can generate code, explain statistical concepts, recommend machine learning methods, and assist with data analysis. Nevertheless, producing syntactically correct code does not necessarily mean that the resulting analysis is statistically valid.

Applied survey-based machine learning introduces additional challenges. Analysts must consider sampling weights, population representation, validation design, data leakage, class imbalance, uncertainty, and generalizability.

A model may produce apparently strong predictive performance while using an inappropriate validation strategy or ignoring the survey design.

These problems motivate a systematic evaluation of LLMs in realistic survey-based machine learning workflows.

## 3. Research Problem

The central research problem is to determine how reliably LLMs can solve applied survey-weighted machine learning tasks when multiple statistical and machine learning constraints interact.

The evaluation will examine both the technical correctness of generated solutions and the methodological validity of the decisions made by the models.

The benchmark will specifically investigate whether LLMs can:

- Interpret survey sampling information and weights correctly.
- Select appropriate modelling and validation strategies.
- Identify and prevent data leakage.
- Evaluate predictive performance under class imbalance.
- Recognize distribution shift during external validation.
- Handle missing data and statistical uncertainty appropriately.
- Interpret model calibration and explainability outputs.
- Produce reproducible analytical workflows.

## 4. Research Gap and Novelty Hypothesis

Existing research has explored statistical reasoning, statistical code generation, data-based reasoning, and broader LLM evaluation.

However, the proposed project investigates a more focused applied evaluation setting: the interaction of complex survey design, survey-weighted predictive modelling, leakage-safe validation, and external population validation under distribution shift.

The working research-gap hypothesis is that these interconnected requirements may not be adequately assessed together by evaluations focused on isolated statistical questions or general-purpose machine learning tasks.

This hypothesis must be examined through a structured literature review before making definitive novelty claims.

SurveyML-Eval will seek to contribute a reproducible evaluation framework with transparent scoring, reference solutions, repeated trials, and human-reviewed error analysis.

## 5. Research Questions

### Primary Research Question

How reliably can modern LLMs perform survey-weighted predictive modelling and external validation when multiple statistical and machine learning constraints interact?

### Secondary Research Questions

**RQ1:** How accurately do LLMs interpret complex survey sampling designs and survey weights?

**RQ2:** Can LLMs identify data leakage and select appropriate validation strategies?

**RQ3:** How effectively do LLMs handle class imbalance and distribution shift?

**RQ4:** Do LLM-generated solutions distinguish predictive performance from statistical validity and population generalizability?

**RQ5:** How consistent are LLM responses across repeated trials under controlled evaluation settings?

**RQ6:** What systematic methodological and technical failure patterns occur during survey-based machine learning tasks?

## 6. Research Objectives

1. Design a reproducible benchmark for evaluating LLMs on survey-weighted machine learning workflows.
2. Develop well-defined evaluation tasks with reference solutions and transparent scoring criteria.
3. Assess model understanding of survey design, sampling weights, and population representation.
4. Evaluate leakage prevention and validation strategy selection.
5. Examine model performance under class imbalance and external distribution shift.
6. Assess the treatment of missing data, uncertainty, calibration, and interpretability.
7. Compare model performance across repeated trials.
8. Identify systematic model limitations through structured failure analysis.

## 7. Proposed Benchmark Task Families

The benchmark will initially contain eight task families.

| ID | Task family | Evaluation focus |
|---|---|---|
| T01 | Complex Survey Design and Weight Interpretation | Sampling design and weight interpretation |
| T02 | Survey-Weighted Predictive Modelling | Appropriate modelling under survey constraints |
| T03 | Data Leakage Detection and Prevention | Identification and prevention of leakage |
| T04 | Validation Strategy Selection | Appropriate validation design |
| T05 | Class Imbalance and Performance Evaluation | Metrics and imbalance-aware evaluation |
| T06 | External Validation and Distribution Shift | Generalization across populations |
| T07 | Missing Data and Statistical Uncertainty | Missingness, uncertainty and statistical validity |
| T08 | Model Calibration and Interpretability | Calibration and explanation quality |

Each task will include a clearly defined input, expected output, reference solution, scoring rubric, and relevant edge cases.

The final number and structure of tasks will be determined after feasibility testing and review of the hackathon constraints.

## 8. Proposed Methodology

### Phase 1: Literature Review

Review existing work on statistical reasoning benchmarks, LLM evaluation, statistical code generation, complex survey analysis, and machine learning under distribution shift.

### Phase 2: Benchmark Construction

Develop evaluation tasks, synthetic or appropriately licensed datasets, reference solutions, expected outputs, and grading rubrics.

### Phase 3: Evaluation Framework

Implement a reproducible Python-based evaluation system that records model responses, scores, errors, and execution details.

### Phase 4: Model Experiments

Evaluate selected LLMs under documented and controlled settings. Conduct repeated trials where feasible.

### Phase 5: Statistical Analysis

Compare task-level and overall performance, repeated-trial consistency, error patterns, and relevant uncertainty measures.

### Phase 6: Failure Analysis

Review incorrect and partially correct responses to identify methodological, statistical, computational, and reasoning failures.

### Phase 7: Reproducibility and Documentation

Publish the benchmark specifications, scoring logic, experiment configuration, raw evaluation outputs, dependencies, and execution instructions, subject to licensing and hackathon requirements.

## 9. Evaluation Metrics

Potential evaluation measures include:

- Task-level pass rate.
- Overall benchmark success rate.
- Pass@k.
- Pass^k.
- Numeric error within predefined tolerances.
- Methodological correctness.
- Code execution success.
- Calibration and uncertainty measures where applicable.
- Repeated-trial consistency.
- Failure-category frequency.
- Runtime and API cost.

Metric definitions, aggregation rules, and scoring weights will be specified before the final experiments.

## 10. Expected Contributions

The project aims to deliver:

1. A focused benchmark for LLM evaluation in survey-weighted machine learning.
2. A collection of reproducible evaluation tasks and reference solutions.
3. A transparent and testable scoring framework.
4. Experimental evidence about LLM performance across interconnected statistical challenges.
5. A structured analysis of methodological and technical failure patterns.
6. A reusable open-source benchmark repository, subject to data and licensing restrictions.

These are planned contributions, not established experimental findings.

## 11. Ethical and Reproducibility Considerations

The benchmark will prioritize synthetic or appropriately licensed datasets.

Restricted survey microdata will not be redistributed without explicit authorization. Any external datasets will be used according to their applicable access and licensing conditions.

No API keys, credentials, private records, or confidential information will be included in the repository.

Model identifiers, versions, settings, execution dates, trial counts, and scoring configurations will be documented to support reproducibility.

## 12. Limitations

The benchmark may not represent every domain of applied statistics or machine learning. Results may depend on the selected models, prompts, model versions, datasets, and evaluation settings.

Synthetic tasks may not capture all complexities of real-world survey data. Human judgment may also be required for evaluating certain methodological decisions.

These limitations will be documented and considered when interpreting experimental findings.

## 13. Planned Research Paper Structure

1. Introduction
2. Related Work
3. Research Gap and Contributions
4. Benchmark Design and Task Construction
5. Experimental Methodology
6. Evaluation Metrics and Statistical Analysis
7. Experimental Results
8. Failure Analysis and Discussion
9. Threats to Validity
10. Limitations
11. Conclusion and Future Work
12. References
13. Supplementary Materials and Reproducibility Appendix

---

**Project status:** Research proposal and benchmark design stage. No experimental results or model-performance claims have been established yet.