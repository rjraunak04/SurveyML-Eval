# SurveyML-Eval

**A reproducible benchmark evaluating Large Language Models on statistical reasoning, survey-weighted machine learning, validation, and distribution shift.**

[![Status](https://img.shields.io/badge/status-research%20design-blue)]()
[![Benchmark Tasks](https://img.shields.io/badge/tasks-8-orange)]()
[![Scoring](https://img.shields.io/badge/scoring-80%20points-green)]()
[![License](https://img.shields.io/badge/license-MIT-lightgrey)]()

## 1. Project Overview

SurveyML-Eval is a research-oriented benchmark designed to evaluate the reliability of Large Language Models (LLMs) in applied statistical reasoning and machine learning workflows involving complex survey data.

The benchmark focuses on an integrated analytical challenge: whether LLMs can correctly reason about complex survey designs, survey-weighted predictive modelling, leakage-safe validation, external population validation, statistical uncertainty, and model interpretation.

Rather than evaluating isolated statistical questions alone, SurveyML-Eval aims to assess how well models connect statistical principles with practical machine learning decisions.

The benchmark is designed to produce reproducible, evidence-based evaluations of model strengths, limitations, and failure patterns.

**Current status:** Research design and documentation completed. Benchmark implementation, empirical evaluation, and grader validation remain in progress.

## 2. Research Motivation

LLMs are increasingly used to assist with data analysis, statistical programming, and machine learning workflows.

However, producing a plausible explanation is not equivalent to producing a statistically valid analytical workflow.

In complex survey-based predictive modelling, several methodological decisions must be considered together:

- Sampling weights and complex survey design.
- Survey-aware predictive modelling.
- Data leakage prevention.
- Appropriate validation strategy.
- Class imbalance and performance evaluation.
- External validation across populations.
- Missing-data assumptions and uncertainty.
- Calibration and model interpretability.

An LLM may answer individual statistical questions correctly while failing to integrate these decisions into a valid end-to-end workflow.

SurveyML-Eval is designed to investigate this problem.

## 3. Research Problem and Proposed Gap

Existing statistical and quantitative reasoning benchmarks provide important foundations for evaluating LLM capabilities.

SurveyML-Eval investigates a more focused evaluation setting: the integration of complex survey design with predictive machine learning and external population validation.

The proposed research gap concerns whether current LLMs can consistently:

1. Interpret complex survey sampling structures.
2. Incorporate survey weights appropriately into predictive workflows.
3. Prevent leakage during preprocessing and model development.
4. Select validation strategies aligned with the target population and deployment setting.
5. Evaluate generalisation under external distribution shift.
6. Interpret statistical uncertainty and model reliability.

This is a focused research-gap hypothesis, not a claim that no previous benchmark has studied survey-related reasoning.

The literature review documents related work and the areas of overlap.

## 4. Research Questions

The primary research question is:

**How reliably can Large Language Models reason about survey-weighted machine learning workflows, leakage-safe validation, and external population generalisation?**

The secondary research questions investigate:

- Survey design and sampling-weight interpretation.
- Appropriate implementation of survey-weighted predictive modelling.
- Detection and prevention of data leakage.
- Selection of valid validation strategies.
- Performance evaluation under class imbalance.
- External validation and distribution shift.
- Missing-data handling and statistical uncertainty.
- Model calibration and interpretability.

Detailed research questions and measurable objectives are available in:

- [Research Problem and Statement](docs/problem_statement.md)
- [Research Objectives and Questions](docs/research_objectives.md)

## 5. Benchmark Task Families

SurveyML-Eval contains eight proposed task families.

| Task ID | Task Family | Evaluation Focus |
|---|---|---|
| T01 | Complex Survey Design and Weight Interpretation | Sampling weights, strata, clusters, design effects |
| T02 | Survey-Weighted Predictive Modelling | Weight-aware predictive modelling workflows |
| T03 | Data Leakage Detection and Prevention | Leakage identification and prevention |
| T04 | Validation Strategy Selection | Appropriate validation design |
| T05 | Class Imbalance and Performance Evaluation | Classification metrics, resampling, thresholds |
| T06 | External Validation and Distribution Shift | Population generalisation and distribution shift |
| T07 | Missing Data and Statistical Uncertainty | Missingness mechanisms, imputation, uncertainty |
| T08 | Model Calibration and Interpretability | Calibration, SHAP, feature importance, limitations |

Each task family contributes a maximum of 10 points.

**Total proposed benchmark score: 80 points.**

Detailed task specifications, evaluation objectives, expected evidence, and cross-task requirements are provided in:

[Benchmark Task Design](docs/benchmark_task_design.md)

## 6. Research Methodology

The proposed methodology follows a structured benchmark-development and evaluation process.

### Phase 1 — Benchmark design

- Define research questions and evaluation objectives.
- Establish task families and task-level requirements.
- Develop realistic statistical and machine learning scenarios.

### Phase 2 — Task and dataset construction

- Develop task instances with explicit input and output requirements.
- Use synthetic or appropriately licensed datasets.
- Document dataset assumptions and provenance.
- Develop reference solutions and accepted alternative approaches.

### Phase 3 — Model evaluation

- Select and identify models using exact model identifiers and versions.
- Standardise prompts and execution configurations.
- Conduct repeated model trials.
- Record raw outputs and execution metadata.

### Phase 4 — Grading and validation

- Apply deterministic grading where possible.
- Use rule-based methodological evaluation.
- Include human expert review for complex judgments.
- Measure grader agreement and reliability.

### Phase 5 — Statistical analysis

- Calculate task-level and overall performance.
- Examine repeated-run variability.
- Analyse critical errors and failure categories.
- Compare model performance using appropriate uncertainty estimates.

The full methodology is documented in:

[Research Methodology](docs/methodology.md)

## 7. Evaluation Protocol

The evaluation protocol is designed to support consistent comparisons across models and task instances.

Planned evaluation components include:

- Standardised prompts and task configurations.
- Exact model identifiers and versions.
- Repeated trials for each model and task instance.
- Task-level and overall performance.
- Criterion-level grading.
- Pass@k and pass^k where appropriate.
- Statistical uncertainty estimation.
- Paired model comparisons where justified.
- Failure analysis.
- Runtime and cost measurement.

Task-instance variability and repeated-run variability will be analysed separately.

No model performance results are claimed at the current research-design stage.

Detailed procedures are available in:

[Evaluation Protocol](docs/evaluation_protocol.md)

## 8. Grading Framework

The proposed grading framework uses an 80-point scoring structure.

| Grading Component | Maximum Points |
|---|---:|
| T01 — Survey Design | 10 |
| T02 — Survey-Weighted Modelling | 10 |
| T03 — Data Leakage | 10 |
| T04 — Validation Strategy | 10 |
| T05 — Class Imbalance | 10 |
| T06 — External Validation | 10 |
| T07 — Missing Data and Uncertainty | 10 |
| T08 — Calibration and Interpretability | 10 |
| **Total** | **80** |

Each task includes explicit scoring criteria covering:

- Statistical or technical correctness.
- Methodological reasoning.
- Interpretation and justification.
- Completeness and clarity.

The grading architecture separates:

1. Machine-checkable evaluation.
2. Rule-based methodological grading.
3. Human expert assessment.

Critical errors are recorded separately, and alternative scientifically valid approaches may receive credit.

LLM-based judging, if used, will remain an auxiliary assessment method rather than being treated as ground truth.

See the complete [Grading Framework](docs/grading_framework.md).

## 9. Planned Evaluation Metrics

The benchmark is designed to report multiple dimensions rather than relying on a single aggregate score.

| Evaluation Dimension | Planned Measurement |
|---|---|
| Task correctness | Criterion-level and task-level scores |
| Overall performance | Total and normalised benchmark score |
| Repeated-run consistency | Mean and variability |
| Pass@k | Probability of at least one successful attempt among k attempts |
| Pass^k | Probability that all k attempts are successful |
| Grader reliability | Appropriate inter-rater reliability measures |
| Model limitations | Critical-error and failure-category frequency |
| Efficiency | Runtime and cost where measurable |

The exact statistical procedure will depend on the task structure and available observations.

## 10. Reproducibility and Transparency

Reproducibility is a central design principle.

The intended benchmark release will document:

- Task definitions and task-instance identifiers.
- Dataset provenance and permitted usage.
- Reference answers and grading criteria.
- Model identifiers and versions.
- Prompt configurations.
- Evaluation dates and trial identifiers.
- Raw model responses.
- Criterion-level scores.
- Execution settings.
- Runtime and cost measurements.
- Grader versions and adjudication records.

No API credentials, private datasets, or confidential information should be included in the repository or submission ZIP.

An `.env.example` file, where required, will contain environment-variable names only.

## 11. Research Ethics and Data Governance

SurveyML-Eval will use synthetic data or datasets that are appropriately licensed and authorised for the intended use.

The benchmark will distinguish between:

- Publicly available data.
- Synthetic benchmark data.
- Restricted or licensed research data.

Restricted NFHS/DHS microdata will not be redistributed without appropriate authorisation.

The benchmark will avoid exposing personal information and will document relevant dataset limitations.

## 12. Repository Structure

The planned repository organisation is:

```text
SurveyML-Eval/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── docs/
│   ├── problem_statement.md
│   ├── research_objectives.md
│   ├── literature_review.md
│   ├── benchmark_task_design.md
│   ├── methodology.md
│   ├── evaluation_protocol.md
│   ├── grading_framework.md
│   ├── repository_architecture.md
│   ├── benchmark_task_schema.md
│   ├── dataset_schema.md
│   ├── execution_architecture.md
│   ├── grading_architecture.md
│   └── architecture_overview.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── synthetic/
│
├── tasks/
│   ├── T01/
│   ├── T02/
│   ├── T03/
│   ├── T04/
│   ├── T05/
│   ├── T06/
│   ├── T07/
│   └── T08/
│
├── reference_answers/
├── evaluation/
├── graders/
├── results/
├── scripts/
└── tests/
```

The structure above describes the intended organisation. Directories and implementation files will be added as development progresses.

## 13. Installation and Usage

CP-07C implements the synthetic benchmark dataset generator and validation workflow for SurveyML-Eval.

## Quick start

```bash
python -m pip install -r requirements.txt
python scripts/generate_synthetic_data.py
pytest -q
```

The generator creates the benchmark data bundle under `data/synthetic/` and writes the required dataset groups:

- `DS-01/` finite population and core sample data.
- `DS-02/` leakage scenarios.
- `DS-03/` missingness and class-imbalance scenarios.
- `DS-04/` independent external population and external validation sample.
- `manifest.json` with file checksums and provenance metadata.

## Dataset-generation design

The generator implements the CP-07B design decisions for the synthetic benchmark:

- Eight strata and twenty PSUs per stratum.
- Population generation before sample selection.
- Ten selected PSUs per stratum and 125 units sampled per selected PSU.
- Stage-specific inclusion probabilities and inverse-probability weights.
- Binary outcome generation from a calibrated logistic model with a synthetic expected prevalence.
- Independent external population generation with covariate and prevalence shifts.
- Synthetic provenance metadata and checksum tracking.

The generator is reproducible through the master seed `42` and separate random streams for population generation, sampling, missingness, imbalance, and external validation.

For the benchmark, the clean model-facing sample excludes leakage columns and protected audit variables. Leakage and missingness scenarios are intentionally created as separate dataset views.

## 14. Experimental Results

**No empirical model results are available at this stage.**

The following reporting tables are reserved for completed experiments.

| Model | T01 | T02 | T03 | T04 | T05 | T06 | T07 | T08 | Total / 80 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Model A | — | — | — | — | — | — | — | — | — |
| Model B | — | — | — | — | — | — | — | — | — |

Results will only be added after benchmark execution, grading validation, and appropriate analysis.

## 15. Limitations

The proposed benchmark has anticipated limitations:

- Task coverage may not represent every statistical or machine learning application.
- Some tasks may permit multiple valid solutions.
- Expert grading may involve subjective judgments.
- Synthetic data may not fully reproduce real-world survey complexity.
- Equal task-family weighting is a design choice.
- Benchmark performance does not guarantee reliable performance in production environments.
- Model and API updates may affect evaluation comparability.

These limitations will be revisited as the benchmark is implemented and empirically evaluated.

## 16. Hackathon Submission

The repository is being developed with reproducibility, evaluation transparency, task quality, grader reliability, and evidence of model limitations as core priorities.

Planned submission components:

- Benchmark evaluation ZIP.
- Root README and setup instructions.
- Task inputs and reference grading criteria.
- Scoring logic and explanation.
- Raw model outputs and evaluation scores.
- Model and experiment metadata.
- Short video walkthrough.

### Video walkthrough

**Status:** Pending.

Video link will be added after recording and publication.

The final submission package will follow the official size, accessibility, and documentation requirements.

## 17. Research Documentation

The following documents define the research design, benchmark methodology, and system architecture.

| Document | Description |
|---|---|
| [Problem Statement](docs/problem_statement.md) | Research motivation, problem, and scope |
| [Research Objectives](docs/research_objectives.md) | Research questions and measurable objectives |
| [Literature Review](docs/literature_review.md) | Related work and proposed research gap |
| [Benchmark Task Design](docs/benchmark_task_design.md) | Eight task families and task specifications |
| [Research Methodology](docs/methodology.md) | Proposed benchmark methodology |
| [Evaluation Protocol](docs/evaluation_protocol.md) | Model evaluation and statistical analysis |
| [Grading Framework](docs/grading_framework.md) | Task rubrics and scoring framework |
| [Architecture Overview](docs/architecture_overview.md) | Unified overview of the benchmark architecture |
| [Repository Architecture](docs/repository_architecture.md) | Repository organization and component responsibilities |
| [Benchmark Task Schema](docs/benchmark_task_schema.md) | Task metadata and instance structure |
| [Dataset Schema](docs/dataset_schema.md) | Dataset organization, metadata, and governance |
| [Execution Architecture](docs/execution_architecture.md) | Model execution and response management |
| [Grading Architecture](docs/grading_architecture.md) | Grading methods, scoring, and audit records |

## 18. Future Development Roadmap

The next development stages will focus on:

1. Finalising benchmark task instances.
2. Constructing synthetic datasets and reference solutions.
3. Implementing the benchmark execution pipeline.
4. Developing deterministic grading scripts.
5. Validating grading reliability.
6. Running model evaluations.
7. Analysing model failures and statistical uncertainty.
8. Preparing reproducible benchmark results.
9. Developing the research manuscript.
10. Preparing the final hackathon submission.

## 19. License

This repository currently includes an MIT License.

Dataset licences, model terms of use, and third-party dependencies remain subject to their respective terms and conditions.

## 20. Acknowledgement

SurveyML-Eval is an independent research-oriented benchmark project focused on the intersection of statistical reasoning, complex survey analysis, and machine learning reliability.

The goal is to contribute a transparent and reproducible evaluation framework that helps identify where LLM-generated statistical and machine learning workflows are reliable and where they require expert verification.

---

**Project:** SurveyML-Eval
**Research focus:** Survey-Weighted Machine Learning and LLM Evaluation
**Development status:** Research design and documentation completed; implementation and empirical evaluation pending.