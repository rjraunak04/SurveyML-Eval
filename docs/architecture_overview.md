# SurveyML-Eval: Unified Architecture Overview

**Project:** SurveyML-Eval
**Document:** Unified Architecture Overview
**Version:** 1.0
**Status:** Proposed architecture
**Related Checkpoints:** CP-06A to CP-06E

---

## 1. Purpose

This document provides a unified overview of the SurveyML-Eval benchmark architecture.

It connects the repository architecture, benchmark task schema, dataset schema, execution architecture, and grading architecture into a single conceptual system.

The objective is to establish a consistent understanding of how benchmark tasks are defined, prepared, executed, evaluated, and reported.

This document summarizes the architecture specifications. It does not claim that the described components have already been implemented.

## 2. System Overview

SurveyML-Eval is designed to evaluate the reliability of Large Language Models (LLMs) on statistical reasoning, machine learning workflows, complex survey analysis, and model validation under distribution shift.

The benchmark follows a modular architecture consisting of six major stages:

1. Task definition and management.
2. Dataset preparation and validation.
3. Prompt construction and model execution.
4. Response collection and preservation.
5. Response grading and score generation.
6. Evaluation analysis and reporting.

The architecture separates benchmark definitions, datasets, model executions, reference answers, and grading records to support reproducibility and auditability.

## 3. High-Level Architecture

The conceptual workflow is:

```text
Benchmark Task Definitions
          |
          v
Task and Dataset Validation
          |
          v
Dataset and Input Preparation
          |
          v
Prompt Construction
          |
          v
Model Provider Adapter
          |
          v
LLM Execution
          |
          v
Raw Response Preservation
          |
          v
Grading Engine
          |
          v
Grading Records and Scores
          |
          v
Evaluation Analysis
          |
          v
Benchmark Reports
```

Supporting components include configuration management, logging, experiment tracking, provenance management, and quality assurance.

## 4. Architecture Components

### 4.1 Repository Architecture

The repository architecture defines how project files, documentation, datasets, source code, tests, and experiment artifacts are organized.

Its responsibilities include:

- Maintaining a consistent project structure.
- Separating source code from data and generated outputs.
- Supporting modular development.
- Preserving experiment traceability.
- Maintaining reproducibility and documentation.

Detailed specification: [Repository Architecture](repository_architecture.md).

### 4.2 Benchmark Task Management

The task management component defines the benchmark's individual task instances.

Each task instance should contain:

- Task identification and metadata.
- Task family and difficulty information.
- Model-facing instructions.
- Required inputs.
- Expected response format.
- Evaluation criteria.
- Reference information maintained separately from model-facing content.

The benchmark contains eight task families, identified as T01 through T08.

Detailed specification: [Benchmark Task Schema](benchmark_task_schema.md).

### 4.3 Dataset Management

The dataset management component defines how benchmark datasets and their metadata are organized, validated, and documented.

Its responsibilities include:

- Dataset provenance and licensing.
- Variable definitions and roles.
- Survey weights, strata, and cluster information.
- Missing-data documentation.
- Training, validation, test, and external-validation separation.
- Leakage prevention.
- Dataset quality checks.

Synthetic or appropriately licensed data must be used in accordance with the project's data governance requirements.

Detailed specification: [Dataset Schema](dataset_schema.md).

### 4.4 Model Execution

The execution component manages interactions between benchmark tasks and LLM providers.

Its responsibilities include:

- Provider-independent model adapters.
- Prompt construction.
- Model and execution configuration.
- Trial and attempt tracking.
- Response preservation.
- Error handling and retry management.
- Token, latency, and cost recording.
- Execution provenance.

The execution layer should preserve raw model outputs for subsequent grading and audit.

Detailed specification: [Execution Architecture](execution_architecture.md).

### 4.5 Grading and Evaluation

The grading component evaluates model responses against benchmark-specific requirements.

It supports:

- Deterministic grading.
- Rubric-based grading.
- Hybrid grading.
- Partial credit.
- Critical error detection.
- Human expert review.
- Inter-rater agreement analysis.
- Supplementary LLM-assisted grading.

Grading records should preserve the applied rubric version, grading method, score, and relevant audit information.

LLM-assisted grading must not be treated as the sole source of ground truth.

Detailed specification: [Grading Architecture](grading_architecture.md).

## 5. Benchmark Task Families

The architecture supports the following eight task families:

| ID | Task family |
|---|---|
| T01 | Complex Survey Design and Weight Interpretation |
| T02 | Survey-Weighted Predictive Modelling |
| T03 | Data Leakage Detection and Prevention |
| T04 | Validation Strategy Selection |
| T05 | Class Imbalance and Performance Evaluation |
| T06 | External Validation and Distribution Shift |
| T07 | Missing Data and Statistical Uncertainty |
| T08 | Model Calibration and Interpretability |

Each task family may contain multiple task instances. A task instance can be executed across multiple models and repeated trials.

## 6. End-to-End Data Flow

### Stage 1: Task Selection

The benchmark selects a valid task instance using its unique identifier.

Task metadata and model-facing instructions are retrieved separately from hidden reference information.

### Stage 2: Dataset Preparation

The required dataset or input artifact is located and validated.

The system checks the relevant metadata, data provenance, variable definitions, and task-specific requirements.

### Stage 3: Prompt Construction

A model-facing prompt is assembled using the task instructions and permitted input data.

Hidden reference answers, grading rubrics, and evaluation keys must not be exposed to the evaluated model.

### Stage 4: Model Execution

The execution engine sends the prompt to the configured model provider.

Execution settings, model identification, timestamps, trial identifiers, and relevant usage information are recorded.

### Stage 5: Response Preservation

The raw model response is preserved with its execution metadata.

Responses should not be silently modified before grading.

### Stage 6: Grading

The grading engine selects the appropriate deterministic, rubric-based, or hybrid evaluation method.

The resulting grading record retains the score, grading method, rubric version, and audit information.

### Stage 7: Evaluation and Reporting

Grading records are aggregated for benchmark analysis.

Reports may examine task-level performance, model-level performance, failure patterns, uncertainty, and differences across task families.

## 7. Core Data Relationships

The architecture uses distinct identifiers for benchmark tasks, executions, responses, and grading records.

Conceptually:

```text
Task Family
    |
    v
Task Instance
    |
    v
Execution
    |
    v
Response
    |
    v
Grading Record
    |
    v
Evaluation Result
```

A task instance can be executed multiple times.

An execution produces a response record, and a response can be associated with a grading record.

Identifiers and version information should make it possible to trace a reported result back to its task, execution, response, and grading configuration.

## 8. Separation of Responsibilities

The architecture maintains clear boundaries between the major components.

| Component | Primary responsibility |
|---|---|
| Task management | Define benchmark tasks |
| Dataset management | Manage benchmark data and metadata |
| Prompt construction | Prepare model-facing inputs |
| Execution engine | Run configured model evaluations |
| Response storage | Preserve original outputs |
| Grading engine | Evaluate model responses |
| Evaluation analysis | Aggregate and analyze scores |
| Reporting | Present benchmark findings |

A component should not silently replace the responsibilities of another component.

## 9. Reproducibility and Traceability

Reproducibility is a central design requirement.

The system should preserve, where applicable:

- Task and task-instance identifiers.
- Task and dataset versions.
- Dataset provenance.
- Model provider and exact model identifier.
- Model version or snapshot where available.
- Prompt and execution configuration.
- Trial and attempt identifiers.
- Execution date and time.
- Random seed where applicable.
- Raw model response.
- Token usage, runtime, and cost where available.
- Grader and rubric versions.
- Final score and grading evidence.

These records are intended to support independent verification and repeatability of benchmark experiments.

## 10. Data Governance and Security

The benchmark must use data that can lawfully and appropriately be used for the intended purpose.

The architecture requires:

- Documented data provenance.
- Appropriate licensing or usage permission.
- No unauthorized redistribution of restricted microdata.
- Separation of public benchmark inputs and hidden evaluation material.
- Protection of API keys and credentials.
- Environment-based configuration for sensitive values.
- No accidental inclusion of secrets in Git history or submission archives.

Public benchmark releases should contain only permitted datasets, metadata, and supporting materials.

## 11. Quality Assurance

Quality assurance should be applied throughout the benchmark workflow.

Important validation areas include:

1. Task schema validation.
2. Dataset integrity and metadata validation.
3. Prompt and input validation.
4. Execution record validation.
5. Response preservation checks.
6. Grading correctness tests.
7. Reference-answer verification.
8. Score aggregation checks.
9. Reproducibility checks.
10. End-to-end benchmark validation.

Automated tests and expert review should be used where appropriate.

## 12. Architecture Specifications

The unified architecture is supported by five detailed specifications:

| Document | Checkpoint | Purpose |
|---|---|---|
| Repository Architecture | CP-06A | Repository organization and responsibilities |
| Benchmark Task Schema | CP-06B | Task definitions and metadata |
| Dataset Schema | CP-06C | Dataset organization and governance |
| Execution Architecture | CP-06D | Model execution and response management |
| Grading Architecture | CP-06E | Response evaluation and score management |

Each document provides the detailed requirements for its respective component.

## 13. Implementation Boundary

This document describes the proposed logical architecture.

It does not establish that:

- All components have been implemented.
- All datasets have been constructed.
- All benchmark tasks have been validated.
- All model providers have been integrated.
- All graders have passed expert validation.
- Any model evaluation results have been generated.

Implementation and validation will be addressed in subsequent development checkpoints.

## 14. Acceptance Criteria

The unified architecture documentation will be considered complete when:

1. All five detailed architecture specifications are linked.
2. The eight benchmark task families are consistently identified.
3. The end-to-end workflow is documented.
4. Component responsibilities are clearly separated.
5. Task, execution, response, and grading relationships are explained.
6. Reproducibility and traceability requirements are documented.
7. Data governance and security requirements are addressed.
8. No implementation or experimental results are falsely claimed.

## 15. Architecture Status

The unified architecture is documented as a proposed design based on CP-06A through CP-06E.

The specifications will be refined during implementation and validated through controlled testing before the architecture is treated as stable.
