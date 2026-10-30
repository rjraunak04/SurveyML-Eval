# SurveyML-Eval: Research Objectives, Questions and Evaluation Framework

## 1. Purpose of This Document

This document operationalizes the research problem established in `problem_statement.md`.

It defines measurable research questions, research objectives, evaluation dimensions, and the relationship between benchmark tasks and the micro1 Eval Hackathon judging criteria.

The purpose is to ensure that SurveyML-Eval is not merely a collection of statistical questions, but a structured, reproducible evaluation benchmark.

## 2. Primary Research Question

**PRQ:** How reliably can modern Large Language Models perform survey-weighted predictive modelling and external validation when multiple statistical and machine learning constraints interact?

The primary question will be investigated through task-level correctness, methodological validity, code execution, repeated-trial consistency, and failure analysis.

## 3. Secondary Research Questions and Measurable Outcomes

### RQ1: Complex Survey Design

How accurately do LLMs interpret complex survey sampling designs and survey weights?

**Evaluation dimensions:**
- Correct interpretation of sampling weights.
- Understanding of population representation.
- Recognition of stratification and clustering.
- Identification of inappropriate unweighted analysis.

**Measurable outcomes:**
- Correctness score for survey-design questions.
- Frequency of incorrect weight interpretation.
- Methodological error rate.

### RQ2: Data Leakage and Validation

Can LLMs identify data leakage and select appropriate validation strategies?

**Evaluation dimensions:**
- Identification of target leakage.
- Recognition of preprocessing leakage.
- Appropriate train-test separation.
- Selection of suitable validation strategies.

**Measurable outcomes:**
- Leakage detection accuracy.
- Validation strategy correctness.
- Frequency of critical leakage-related errors.

### RQ3: Class Imbalance and Distribution Shift

How effectively do LLMs handle class imbalance and distribution shift?

**Evaluation dimensions:**
- Selection of appropriate performance metrics.
- Recognition of class imbalance.
- Understanding of changes in population distributions.
- Recognition of performance deterioration under distribution shift.

**Measurable outcomes:**
- Metric selection correctness.
- Distribution-shift identification score.
- Methodological correctness score.

### RQ4: Predictive Performance and Statistical Validity

Do LLM-generated solutions distinguish predictive performance from statistical validity and population generalizability?

**Evaluation dimensions:**
- Interpretation of predictive metrics.
- Recognition of survey-design limitations.
- Understanding of population-level generalizability.
- Identification of unsupported conclusions.

**Measurable outcomes:**
- Statistical reasoning score.
- Generalizability assessment score.
- Frequency of unsupported analytical conclusions.

### RQ5: Repeated-Trial Consistency

How consistent are LLM responses across repeated trials under controlled evaluation settings?

**Evaluation dimensions:**
- Repeated execution of identical tasks.
- Stability of generated answers.
- Consistency of scoring outcomes.
- Variability in methodological decisions.

**Measurable outcomes:**
- Pass@k.
- Pass^k.
- Trial-level score variability.
- Consistency of methodological decisions.

### RQ6: Systematic Failure Patterns

What systematic methodological and technical failure patterns occur during survey-based machine learning tasks?

**Evaluation dimensions:**
- Statistical reasoning failures.
- Incorrect modelling decisions.
- Data leakage failures.
- Code execution failures.
- Incorrect interpretation of results.
- Reproducibility failures.

**Measurable outcomes:**
- Frequency of each failure category.
- Severity of identified failures.
- Distribution of errors across benchmark task families.

## 4. Refined Research Objectives

### RO1: Benchmark Development

Develop a reproducible benchmark for evaluating LLMs on survey-weighted machine learning workflows.

**Success criteria:**
- Clearly documented task specifications.
- Defined input and expected output for each task.
- Reference solutions.
- Explicit scoring criteria.

### RO2: Survey Statistical Reasoning

Evaluate the ability of LLMs to interpret survey sampling designs and population weights.

**Success criteria:**
- Correctness of sampling-weight interpretation.
- Identification of survey-design requirements.
- Appropriate methodological decisions.

### RO3: Leakage-Safe Machine Learning

Evaluate whether LLMs identify data leakage and recommend appropriate validation strategies.

**Success criteria:**
- Correct identification of leakage scenarios.
- Appropriate validation recommendations.
- Correct handling of data preprocessing boundaries.

### RO4: Robust Predictive Evaluation

Assess LLM performance in class imbalance and external distribution-shift scenarios.

**Success criteria:**
- Appropriate metric selection.
- Correct identification of distribution shift.
- Methodologically valid external evaluation recommendations.

### RO5: Statistical Reliability

Evaluate the consistency and statistical validity of LLM-generated analytical solutions.

**Success criteria:**
- Repeated-trial evaluation.
- Transparent scoring.
- Consistency analysis.
- Appropriate uncertainty reporting.

### RO6: Failure Analysis

Identify and categorize systematic errors in LLM-generated statistical and machine learning solutions.

**Success criteria:**
- Documented failure taxonomy.
- Human-reviewed error examples.
- Task-level failure summaries.
- Evidence-based interpretation.

### RO7: Reproducibility

Build an evaluation workflow that allows independent execution and verification.

**Success criteria:**
- Documented dependencies.
- Reproducible task inputs.
- Versioned experiment settings.
- Saved raw model outputs and scores.
- Clear execution instructions.

## 5. Research Question to Benchmark Task Mapping

| Research question | Primary task families |
|---|---|
| RQ1 | T01, T02 |
| RQ2 | T03, T04 |
| RQ3 | T05, T06 |
| RQ4 | T01, T02, T06 |
| RQ5 | T01–T08 |
| RQ6 | T01–T08 |

The task mapping is intended to create traceability between the research questions and the benchmark experiments.

## 6. Research Objective to Hackathon Judging Criteria Mapping

The hackathon uses seven judging dimensions.

| Hackathon criterion | Weight | SurveyML-Eval evidence |
|---|---:|---|
| Real-world relevance | 15 | Applied survey-based ML scenarios |
| Task design | 20 | Eight structured task families and edge cases |
| Grader reliability | 20 | Reference solutions, explicit rubrics and grader validation |
| Evidence of model limitations | 15 | Repeated trials and failure analysis |
| Reproducibility | 15 | Versioned configurations, raw outputs and documentation |
| Human expertise/review | 10 | Statistical and methodological expert review |
| Insight/hot take | 5 | Evidence-based conclusions about LLM reliability |

**Total: 100 points.**

The weights represent the hackathon judging rubric, not the project's experimental performance.

## 7. Benchmark-Level Success Criteria

The following are proposed design targets, not achieved results.

1. Construct eight benchmark task families.
2. Develop approximately 5–10 well-designed evaluation tasks, subject to task quality and available time.
3. Define reference solutions and transparent grading criteria for every task.
4. Include meaningful edge cases and methodological judgment scenarios.
5. Conduct repeated trials for selected model-task combinations.
6. Preserve raw outputs, evaluation scores and experiment metadata.
7. Review a sample of graded responses manually.
8. Document incorrect answers, grader disagreements and known limitations.

The final number of tasks, trials, models and evaluation settings will be determined by feasibility and the hackathon deadline.

## 8. Evaluation and Statistical Analysis Plan

### 8.1 Task-Level Evaluation

Each task will be evaluated using a predefined rubric.

Depending on the task, scoring may consider:
- Statistical correctness.
- Methodological correctness.
- Computational correctness.
- Code execution.
- Interpretation quality.

### 8.2 Overall Evaluation

Report:
- Task-level pass rates.
- Overall benchmark success rate.
- Performance by task family.
- Failure-category frequencies.
- Runtime and API cost where available.

### 8.3 Repeated-Trial Evaluation

For tasks evaluated multiple times, report:
- Pass@k: probability of obtaining at least one successful result within k attempts, using a clearly specified success definition.
- Pass^k: probability that all k attempts are successful.
- Mean and variability of trial-level scores.

### 8.4 Grader Reliability

Assess the agreement between automated scoring and human-reviewed judgments.

Record:
- Agreement rate.
- False acceptance of incorrect answers.
- False rejection of correct answers.
- Ambiguous scoring cases.

Use an appropriate agreement statistic when the grading design and sample size support it.

### 8.5 Uncertainty and Statistical Reporting

Where appropriate, report uncertainty intervals and use suitable statistical comparisons.

The statistical methods will be selected according to the evaluation design, sample size, outcome type and independence assumptions.

## 9. Traceability and Reproducibility

Every benchmark task should be traceable through the following structure:

**Research question → Research objective → Task specification → Reference solution → Scoring rubric → Model output → Evaluation result → Failure analysis.**

This traceability structure will support transparent evaluation and independent review.

## 10. Scope and Constraints

SurveyML-Eval will remain focused on the micro1 Eval Hackathon problem.

The project will prioritize:
- A compact but rigorous benchmark.
- Reliable grading.
- Clear evidence of model limitations.
- Reproducible experiments.
- Human-reviewed findings.
- A self-contained hackathon submission.

Research-paper documentation will be developed from the same benchmark and experiments rather than creating a separate, unrelated project.

No model-performance findings will be claimed until experiments have actually been conducted.

## 11. Document Status

**Status:** Research questions and measurable objectives design.

**Related document:** `problem_statement.md`

**Project:** SurveyML-Eval

**Purpose:** Hackathon evaluation benchmark and publication-oriented research development.