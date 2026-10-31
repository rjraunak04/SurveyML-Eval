
# SurveyML-Eval: Repository Architecture Specification

**Project:** SurveyML-Eval
**Document:** Repository Architecture Specification
**Version:** 1.0
**Status:** Proposed architecture
**Development stage:** Day 2 — Benchmark Construction

---

## 1. Purpose

This document defines the proposed software repository architecture for SurveyML-Eval.

The architecture is intended to support a reproducible benchmark for evaluating Large Language Models on statistical reasoning, complex survey analysis, survey-weighted predictive modelling, validation, and distribution shift.

The repository will separate benchmark definitions, datasets, model execution, grading, statistical analysis, and reporting.

The architecture is a development specification. Components described here are proposed and must not be considered implemented until their files and tests exist.

## 2. Architecture Principles

The architecture follows these principles:

1. **Modularity:** Each component has a clearly defined responsibility.
2. **Reproducibility:** Every task, model execution, trial, and grading result must be identifiable.
3. **Traceability:** Raw model responses must remain traceable to their task and execution configuration.
4. **Provider independence:** Model execution must be separated from benchmark task definitions and grading.
5. **Grader independence:** Grading must not depend on the model provider used for execution.
6. **Data governance:** Dataset provenance, licensing, and synthetic-data generation must be documented.
7. **Version control:** Benchmark definitions and grading specifications must be versioned.
8. **Testability:** Core components must support automated unit and integration testing.
9. **Research transparency:** No experimental results should be represented as verified before execution.
10. **Extensibility:** New models, tasks, and grading methods should be addable without redesigning the complete system.

## 3. Proposed Repository Structure

```text
SurveyML-Eval/
│
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── .env.example
│
├── configs/
│   ├── benchmark.yaml
│   ├── models.yaml
│   └── execution.yaml
│
├── data/
│   ├── raw/
│   ├── synthetic/
│   ├── processed/
│   └── metadata/
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
│   ├── T01/
│   ├── T02/
│   ├── T03/
│   ├── T04/
│   ├── T05/
│   ├── T06/
│   ├── T07/
│   └── T08/
│
├── src/
│   └── surveymleval/
│       ├── __init__.py
│       ├── config/
│       ├── data/
│       ├── tasks/
│       ├── models/
│       ├── execution/
│       ├── graders/
│       ├── evaluation/
│       ├── analysis/
│       └── reporting/
│
├── results/
│   ├── raw_outputs/
│   ├── graded_outputs/
│   ├── scores/
│   └── reports/
│
├── scripts/
│   ├── validate_tasks.py
│   ├── generate_data.py
│   ├── run_benchmark.py
│   └── generate_report.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
└── docs/
    ├── problem_statement.md
    ├── research_objectives.md
    ├── literature_review.md
    ├── benchmark_task_design.md
    ├── methodology.md
    ├── evaluation_protocol.md
    ├── grading_framework.md
    └── repository_architecture.md
```

This is the proposed target structure. Directories will be created progressively as their implementation checkpoints begin.

## 4. Component Responsibilities

### 4.1 configs/

Stores benchmark-wide configuration.

Responsibilities:

- Benchmark version and metadata.
- Task-family registration.
- Model identifiers and provider settings.
- Execution configuration.
- Trial configuration.
- Reproducibility settings.

Configuration files must not contain API keys or passwords.

### 4.2 data/

Stores benchmark datasets and their metadata.

Responsibilities:

- Synthetic data.
- Permitted raw data.
- Processed datasets.
- Data dictionaries.
- Dataset provenance.
- Generation metadata.

Restricted datasets must not be committed to the public repository.

### 4.3 tasks/

Contains the executable task definitions for the eight benchmark families.

| Directory | Task Family |
|---|---|
| T01 | Complex Survey Design and Weight Interpretation |
| T02 | Survey-Weighted Predictive Modelling |
| T03 | Data Leakage Detection and Prevention |
| T04 | Validation Strategy Selection |
| T05 | Class Imbalance and Performance Evaluation |
| T06 | External Validation and Distribution Shift |
| T07 | Missing Data and Statistical Uncertainty |
| T08 | Model Calibration and Interpretability |

Each task should have a unique task identifier, task instance identifier, input specification, expected response format, constraints, and grading reference.

### 4.4 reference_answers/

Stores reference solutions and grading evidence.

Responsibilities:

- Reference answers.
- Expected numerical results.
- Valid alternative approaches.
- Assumptions.
- Critical-error examples.
- Task-specific scoring references.

Reference answers must be separated from model-facing task inputs to avoid accidental exposure during evaluation.

### 4.5 src/surveymleval/config/

Loads and validates benchmark configuration.

### 4.6 src/surveymleval/data/

Handles dataset loading, metadata validation, and data-generation interfaces.

### 4.7 src/surveymleval/tasks/

Loads task definitions and validates task instances against the benchmark schema.

### 4.8 src/surveymleval/models/

Defines model-provider interfaces and provider-specific adapters.

A provider adapter is responsible for communication with a model API or supported local model.

### 4.9 src/surveymleval/execution/

Controls benchmark execution.

Responsibilities:

- Task scheduling.
- Prompt construction.
- Trial management.
- Model invocation.
- Timeout and retry policies.
- Execution metadata.
- Raw response persistence.

### 4.10 src/surveymleval/graders/

Implements grading methods.

Responsibilities:

- Deterministic grading.
- Rule-based grading.
- Structured-output validation.
- Critical-error detection.
- Human-review integration.
- Criterion-level scoring.

### 4.11 src/surveymleval/evaluation/

Coordinates task execution and scoring.

It connects task definitions, model execution, response storage, and grading records.

### 4.12 src/surveymleval/analysis/

Supports statistical analysis of benchmark results.

Potential responsibilities:

- Task-level summaries.
- Model comparisons.
- Repeated-run variability.
- Uncertainty estimation.
- Failure-category analysis.
- Grader reliability analysis.

### 4.13 src/surveymleval/reporting/

Generates structured benchmark reports and reproducibility summaries.

### 4.14 results/

Stores generated experimental artifacts.

- `raw_outputs/`: original model responses.
- `graded_outputs/`: grading records.
- `scores/`: task-level and aggregate scores.
- `reports/`: generated evaluation reports.

Large outputs, credentials, and sensitive information must not be committed without an explicit governance decision.

### 4.15 scripts/

Provides command-line entry points for common benchmark operations.

### 4.16 tests/

Contains unit tests, integration tests, and controlled fixtures.

## 5. Benchmark Execution Flow

The proposed execution flow is:

```text
Benchmark Configuration
          |
          v
     Task Loader
          |
          v
    Task Validation
          |
          v
    Prompt Builder
          |
          v
    Model Adapter
          |
          v
    Model Execution
          |
          v
    Raw Response Store
          |
          v
       Grader
          |
          v
   Criterion-Level Scores
          |
          v
    Statistical Analysis
          |
          v
     Report Generator
```

Each execution must preserve the relationship between the task, task instance, model, trial, raw response, and grading record.

## 6. Model Provider Independence

The benchmark must not depend on a single LLM provider.

A common model interface should be defined before implementing provider-specific adapters.

The interface should support:

- Model identifier.
- Prompt input.
- Model response.
- Execution timestamp.
- Runtime measurement.
- Token usage where available.
- Error and timeout reporting.
- Provider-specific metadata.

Provider-specific features must be documented because model APIs may expose different capabilities.

## 7. Task and Result Traceability

The architecture should distinguish the following identifiers:

| Identifier | Meaning |
|---|---|
| benchmark_id | Benchmark identity |
| benchmark_version | Benchmark release version |
| task_id | Task family identifier, T01–T08 |
| task_instance_id | Unique task instance |
| model_id | Exact model identifier |
| trial_id | Repeated execution identifier |
| execution_id | Unique execution record |
| response_id | Unique raw response record |
| grading_id | Unique grading record |

Identifiers must remain stable within the corresponding benchmark release.

## 8. Data and Reference Separation

Model-facing task inputs must not expose hidden reference answers or grading keys.

The benchmark should maintain separate storage for:

1. Public task instructions.
2. Model-visible data.
3. Hidden reference answers.
4. Grading configuration.
5. Raw model responses.
6. Final grading records.

This separation reduces the risk of answer leakage and accidental contamination.

## 9. Reproducibility Requirements

Each benchmark execution should record:

- Benchmark version.
- Task and task-instance identifiers.
- Dataset version or checksum.
- Model identifier and version.
- Prompt template version.
- Execution configuration.
- Trial identifier.
- Timestamp.
- Random seed where applicable.
- Runtime and token usage where available.
- Raw response.
- Grader version.
- Final criterion-level scores.

Reproducibility does not imply that nondeterministic model APIs will produce identical responses on every run. The execution record must preserve the conditions under which each response was obtained.

## 10. Security and Data Governance

The repository must:

- Keep API keys outside version control.
- Use `.env.example` for environment-variable names only.
- Exclude `.env` from Git.
- Avoid committing private datasets.
- Document dataset licences and provenance.
- Avoid storing personally identifiable information in benchmark outputs.
- Apply consistent access and retention rules to experimental artifacts.

## 11. Testing Strategy

The implementation should use several levels of testing.

### Unit testing

Tests individual functions and modules.

Examples:

- Configuration parsing.
- Task schema validation.
- Dataset metadata validation.
- Score calculation.
- Output formatting.

### Integration testing

Tests interactions between components.

Examples:

- Task loader to prompt builder.
- Model adapter to raw response storage.
- Response storage to grader.
- Grader to score aggregation.

### End-to-end testing

Tests a complete benchmark workflow using controlled test fixtures or a mock model adapter.

A successful test must not be confused with a completed real-model experiment.

## 12. Technology Choices

The proposed initial technology stack is:

| Component | Proposed Technology |
|---|---|
| Programming language | Python |
| Data manipulation | pandas, NumPy |
| Statistical analysis | SciPy, statsmodels |
| Machine learning utilities | scikit-learn |
| Configuration | YAML |
| Structured task and result data | JSON |
| Data storage | CSV and Parquet where appropriate |
| Testing | pytest |
| Version control | Git and GitHub |
| Visualisation | Matplotlib |

Final dependencies and versions will be frozen after implementation and compatibility testing.

## 13. Implementation Boundaries

This document defines the target architecture only.

The following are not yet claimed as implemented:

- Model-provider adapters.
- Benchmark execution engine.
- Dataset-generation pipeline.
- Task loader.
- Deterministic graders.
- Statistical reporting engine.
- Human-review interface.
- Automated benchmark runner.

These components will be implemented and tested in subsequent development checkpoints.

## 14. Architecture Status

The repository architecture has been specified as the intended technical foundation for SurveyML-Eval.

The actual implementation will proceed incrementally, with each module tested and documented before being integrated into the benchmark execution pipeline.

The architecture may be revised when implementation evidence identifies necessary changes. Material changes must be documented and version-controlled.
