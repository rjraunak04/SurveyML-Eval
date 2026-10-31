# Benchmark Task Schema

**Project:** SurveyML-Eval
**Document:** Benchmark Task Schema Specification
**Version:** 1.0
**Status:** Proposed schema
**Checkpoint:** CP-06B

---

## 1. Purpose

This document defines a standardized schema for representing benchmark task instances in SurveyML-Eval.

The schema ensures that all benchmark tasks follow a consistent structure, regardless of their task family, difficulty, input type, or evaluation method.

It supports reproducible execution, model-provider independence, reliable grading, and systematic comparison across large language models (LLMs).

The schema is designed for the eight benchmark task families defined in the benchmark task design document.

## 2. Schema Design Principles

The task schema follows these principles:

1. **Consistency:** Every benchmark task instance must follow a common structure.
2. **Unique identification:** Every task instance must have a unique identifier.
3. **Version control:** Task definitions and evaluation criteria must be versioned.
4. **Separation of concerns:** Task prompts, reference answers, and grading metadata must remain separate.
5. **Provider independence:** Task definitions must not depend on a particular LLM provider.
6. **Reproducibility:** Task inputs and evaluation configurations must be preserved.
7. **Machine readability:** Task definitions should support JSON-based storage and validation.
8. **Evaluation transparency:** Every scoring criterion must be documented.
9. **Data governance:** Restricted or unauthorized datasets must not be distributed.

## 3. Task Identification Structure

Each benchmark task instance must contain the following identifiers.

| Field | Description | Example |
|---|---|---|
| benchmark_id | Benchmark identifier | SurveyML-Eval |
| benchmark_version | Benchmark release version | 1.0.0 |
| task_id | Task family identifier | T01 |
| task_instance_id | Unique task instance identifier | T01-001 |
| task_version | Task definition version | 1.0 |
| schema_version | Schema version | 1.0 |
| difficulty | Task difficulty | intermediate |

The task family identifies the broader evaluation category, while the task instance identifies one specific problem within that category.

Multiple task instances may belong to the same task family.

## 4. Task Family Definitions

The schema must support all eight benchmark task families.

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

Each task instance must belong to exactly one primary task family.

A task may additionally include secondary tags to represent related statistical or machine learning concepts.

## 5. Core Task Definition

Every task instance must define the following components.

### 5.1 Metadata

Metadata describes the identity and classification of a task.

Required fields:

- benchmark_id
- benchmark_version
- task_id
- task_instance_id
- task_version
- schema_version
- difficulty
- task_title
- domain
- tags

### 5.2 Task Description

The task description explains the problem being evaluated.

It should include:

- Background and problem context.
- Objective of the task.
- Relevant statistical or machine learning concepts.
- Specific problem constraints.
- Required deliverables.

The description must be sufficiently clear to avoid unnecessary ambiguity.

### 5.3 Model-Facing Prompt

The model-facing prompt contains the information actually provided to the evaluated LLM.

It must include:

- Problem statement.
- Relevant context.
- Input references or supplied data.
- Explicit instructions.
- Expected response format.
- Any applicable assumptions or constraints.

The prompt must not contain hidden reference answers, grading rubrics, or evaluator-only information.

### 5.4 Input Specification

The input specification describes the information required to solve the task.

Possible input types include:

- Structured tabular data.
- CSV or JSON data.
- Statistical summaries.
- Model evaluation results.
- Scenario descriptions.
- Variable definitions.
- Survey design metadata.

Each input must specify its format, description, and relevant data dictionary.

### 5.5 Expected Response Format

Every task must define the expected response structure.

Supported response formats may include:

- Plain text.
- Structured JSON.
- Numerical answers.
- Statistical interpretations.
- Tables.
- Step-by-step analytical explanations.
- Code or pseudocode, when required.

The expected format must be specific enough for consistent evaluation.

### 5.6 Evaluation Criteria

Each task must define evaluation criteria before model execution.

Evaluation criteria may assess:

- Statistical correctness.
- Methodological correctness.
- Reasoning quality.
- Interpretation accuracy.
- Data leakage awareness.
- Validation strategy.
- Uncertainty assessment.
- Reproducibility.
- Completeness of the response.

Task-specific scoring criteria must be linked to the grading framework.

## 6. Hidden Evaluation Metadata

Hidden evaluation information must be stored separately from model-facing task definitions.

It may include:

- Reference answer.
- Expected numerical values.
- Accepted alternative answers.
- Evaluation rubric.
- Scoring weights.
- Critical error conditions.
- Expert review notes.
- Grader configuration.

This information is accessible only to the evaluation pipeline and authorized reviewers.

It must never be included in the prompt sent to an evaluated model.

## 7. Logical JSON Task Structure

The following example illustrates the proposed logical structure of a task instance.

It is a schema illustration, not an actual benchmark question or verified experimental result.

```json
{
  "metadata": {
    "benchmark_id": "SurveyML-Eval",
    "benchmark_version": "1.0.0",
    "task_id": "T01",
    "task_instance_id": "T01-001",
    "task_version": "1.0",
    "schema_version": "1.0",
    "difficulty": "intermediate",
    "task_title": "Survey Weight Interpretation",
    "domain": "complex_survey_analysis",
    "tags": [
      "survey_weights",
      "sampling_design",
      "statistical_inference"
    ]
  },
  "task": {
    "description": "Illustrative task description.",
    "objective": "Assess understanding of survey weights.",
    "constraints": [],
    "model_prompt": {
      "system_instruction": null,
      "user_prompt": "Illustrative model-facing prompt."
    }
  },
  "inputs": {
    "input_type": "scenario",
    "data_references": [],
    "variable_definitions": [],
    "assumptions": []
  },
  "response_specification": {
    "format": "structured_text",
    "required_elements": [
      "interpretation",
      "justification"
    ]
  },
  "evaluation": {
    "grading_method": "rubric_based",
    "criteria_reference": "T01-001-rubric-v1",
    "maximum_score": 10
  },
  "provenance": {
    "source_type": "illustrative",
    "data_license": null,
    "created_by": "benchmark_development_team"
  }
}
```

The example uses placeholder content. It does not represent a completed task or an actual reference answer.

## 8. Task and Reference Separation

The benchmark will maintain separate logical records for:

### 8.1 Public Task Definition

Contains:

- Task metadata.
- Problem description.
- Model-facing prompt.
- Input specifications.
- Expected response format.
- Public task constraints.

### 8.2 Private Reference Definition

Contains:

- Reference answers.
- Accepted answer variations.
- Grading rubrics.
- Scoring weights.
- Critical error definitions.
- Evaluator notes.

The public task definition and private reference definition must share a common task_instance_id.

This ensures that responses can be matched to the correct grading criteria without exposing the reference information to the model.

## 9. Task Lifecycle

Each task instance follows a controlled lifecycle:

1. Task design.
2. Schema validation.
3. Input validation.
4. Expert review.
5. Task approval.
6. Benchmark execution.
7. Response collection.
8. Grading.
9. Score recording.
10. Result analysis.

Changes to an approved task must be versioned and documented.

## 10. Validation Requirements

Every task instance must pass structural and content validation.

### 10.1 Structural Validation

- All required metadata fields must exist.
- Task identifiers must follow the naming convention.
- The task family must be one of T01–T08.
- Schema version must be specified.
- Expected response format must be defined.
- Evaluation method must be specified.

### 10.2 Content Validation

- The problem statement must be understandable.
- The input must be sufficient to address the task.
- Instructions must not contradict one another.
- Evaluation criteria must match the task objective.
- The task must not expose hidden evaluation information.
- Any data source must have documented provenance and permitted usage.

### 10.3 Expert Validation

A qualified reviewer should assess:

- Statistical validity.
- Methodological accuracy.
- Ambiguity.
- Difficulty classification.
- Scoring fairness.
- Alignment with the task family.

## 11. Error Handling

The task validation system should identify:

- Missing required fields.
- Invalid task identifiers.
- Unsupported task families.
- Invalid JSON structure.
- Missing input references.
- Undefined response formats.
- Missing grading configurations.
- Invalid version metadata.

Invalid tasks must not enter the benchmark execution pipeline until corrected.

## 12. Storage and Naming Convention

Task definitions will use JSON as the primary machine-readable format.

Proposed directory structure:

```text
tasks/
├── T01/
│   ├── T01-001.json
│   └── T01-002.json
├── T02/
├── T03/
├── T04/
├── T05/
├── T06/
├── T07/
└── T08/

reference_answers/
├── T01/
│   ├── T01-001.json
│   └── T01-002.json
├── T02/
├── T03/
├── T04/
├── T05/
├── T06/
├── T07/
└── T08/
```

The directory structure is a proposed target structure. It does not indicate that all task files have already been implemented.

## 13. Relationship with Other Benchmark Components

The task schema will integrate with:

- Repository architecture.
- Dataset schema.
- Model provider adapters.
- Benchmark execution engine.
- Response storage.
- Grading framework.
- Statistical evaluation pipeline.
- Reporting system.

The task schema defines what is evaluated, while the execution architecture defines how models are evaluated.

The grading architecture defines how model responses are assessed.

## 14. Implementation Boundaries

This checkpoint defines the logical structure and requirements of benchmark task instances.

It does not implement:

- All eight task families.
- Complete task datasets.
- Automated task generation.
- Model API integrations.
- Execution scripts.
- Grading algorithms.
- Experimental results.

These components will be developed and validated in subsequent checkpoints.

## 15. Acceptance Criteria

CP-06B will be considered complete when:

1. The task metadata structure is defined.
2. All eight task families are supported.
3. Model-facing and evaluator-only information are separated.
4. Input and response specifications are documented.
5. Evaluation metadata is defined.
6. A logical JSON example is provided.
7. Task validation requirements are documented.
8. Storage and naming conventions are specified.
9. Integration with the benchmark architecture is explained.
10. The document passes content and formatting review.

## 16. Architecture Status

**Status:** Proposed schema specification.

This document establishes the logical task-instance contract for SurveyML-Eval.

The schema will be refined during implementation and validated against representative task instances before being treated as a stable benchmark release specification.
