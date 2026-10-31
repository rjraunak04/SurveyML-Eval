# Dataset Schema Specification

**Project:** SurveyML-Eval
**Document:** Dataset Schema Specification
**Version:** 1.0
**Status:** Proposed schema
**Checkpoint:** CP-06C

---

## 1. Purpose

This document defines the standardized dataset structure for SurveyML-Eval.

The dataset schema establishes common requirements for storing, describing, validating, and managing benchmark datasets across all eight benchmark task families.

The schema is designed to preserve statistical information, especially complex survey design metadata, while supporting reproducible machine learning evaluation and external validation.

It distinguishes between analytical variables, survey design variables, outcome variables, identifiers, and evaluation metadata.

## 2. Dataset Design Principles

The dataset schema follows these principles:

1. **Consistency:** All benchmark datasets must follow documented structural conventions.
2. **Traceability:** Each dataset must have a unique identifier and version.
3. **Statistical integrity:** Survey weights, strata, and cluster information must be preserved where applicable.
4. **Reproducibility:** Dataset provenance, transformations, and processing steps must be documented.
5. **Data separation:** Training, validation, test, and external validation datasets must be distinguishable.
6. **Leakage prevention:** Identifiers, target variables, and post-outcome information must be handled carefully.
7. **Data governance:** Restricted or unauthorized data must not be distributed.
8. **Provider independence:** Dataset representation must not depend on a particular LLM provider.
9. **Machine readability:** Dataset metadata should use JSON, with tabular data stored in suitable structured formats.
10. **Research transparency:** Synthetic, licensed, and illustrative datasets must be clearly identified.

## 3. Dataset Identification

Every dataset must have a unique identity.

| Field | Description | Example |
|---|---|---|
| dataset_id | Unique dataset identifier | DS-T01-001 |
| dataset_name | Human-readable name | Survey Design Example |
| dataset_version | Dataset version | 1.0.0 |
| schema_version | Dataset schema version | 1.0 |
| task_id | Associated task family | T01 |
| task_instance_id | Associated task instance | T01-001 |
| source_type | Data origin category | synthetic |
| file_format | Storage format | CSV |
| created_date | Dataset creation date | ISO 8601 date |
| record_count | Number of observations | 1000 |
| variable_count | Number of variables | 12 |

A dataset may support multiple task instances. Where appropriate, task-to-dataset relationships must be documented explicitly.

## 4. Dataset Categories

SurveyML-Eval may use the following dataset categories.

### 4.1 Synthetic Datasets

Synthetic datasets are generated for benchmark development, testing, and evaluation.

They should:

- Contain generated observations rather than copied restricted records.
- Include documented generation assumptions.
- Preserve relevant statistical relationships where intended.
- Identify their generation procedure and version.
- Avoid representing synthetic observations as actual survey respondents.

Synthetic datasets are the preferred option for public benchmark distribution when real microdata access is restricted.

### 4.2 Licensed or Authorized Datasets

Real-world datasets may be used only when their licensing and access conditions permit the intended research activity.

Their documentation must identify:

- Dataset source.
- Access conditions.
- License or authorization status.
- Permitted analytical use.
- Redistribution restrictions.
- Required attribution.

### 4.3 Derived Datasets

Derived datasets are created through documented transformations of source datasets.

Their metadata must identify:

- Parent dataset.
- Transformation procedure.
- Processing version.
- Variable modifications.
- Exclusions and filtering rules.
- Reproducibility information.

A derived dataset must not be distributed if its source license or authorization prohibits redistribution.

## 5. Variable Classification

Every variable must be assigned a documented role.

| Variable role | Purpose |
|---|---|
| Identifier | Identifies observations or sampling units |
| Feature | Predictive or explanatory information |
| Target | Outcome to be predicted |
| Survey weight | Represents the sampling or analysis weight |
| Stratum | Identifies sampling strata |
| Cluster / PSU | Identifies primary sampling units or clusters |
| Time variable | Represents temporal information |
| Group variable | Identifies population or subgroup membership |
| Metadata | Provides supporting dataset information |

A variable may have a different role depending on the task. Its intended use must therefore be documented at task level.

Identifiers should not automatically be treated as predictive features.

Survey design variables must not be silently discarded during preprocessing.

## 6. Variable Dictionary

Each dataset must include a variable dictionary.

Required fields:

| Field | Description |
|---|---|
| variable_name | Unique column name |
| data_type | Data representation type |
| variable_role | Feature, target, weight, identifier, etc. |
| description | Meaning of the variable |
| unit | Measurement unit, if applicable |
| allowed_values | Permitted categories or range |
| missing_value_codes | Documented missing-value codes |
| source_variable | Original source name, if applicable |
| transformation | Applied transformation, if applicable |

Supported logical data types include:

- Integer
- Float
- String
- Boolean
- Date
- Categorical
- Identifier

Categorical variables must document their category labels and coding conventions.

## 7. Complex Survey Design Metadata

Preserving complex survey design is a central requirement of SurveyML-Eval.

Where applicable, each dataset must document the following information.

### 7.1 Sampling Weights

The dataset must identify:

- Weight variable name.
- Weight interpretation.
- Weight scaling or normalization.
- Intended analytical use.
- Any documented adjustment or transformation.

Weights must not be assumed to be interchangeable across datasets or surveys.

### 7.2 Strata

The dataset must identify:

- Stratum variable.
- Number of strata, where known.
- Stratum coding.
- Any special treatment of strata.

### 7.3 Clusters and Primary Sampling Units

The dataset must identify:

- Cluster or PSU variable.
- Cluster identification convention.
- Nested or multistage sampling information, where available.
- Any documented variance-estimation requirements.

### 7.4 Additional Survey Design Information

Where available, the schema should preserve:

- Sampling stages.
- Finite population corrections.
- Replicate weights.
- Replication method.
- Survey domain definitions.
- Design documentation.

Missing survey design information must be explicitly recorded as unavailable or not applicable rather than silently assumed.

## 8. Missing Data Representation

Missing values must follow a documented representation policy.

The dataset documentation must distinguish, where possible:

- Unknown values.
- Not applicable values.
- Not collected values.
- Refused responses.
- Invalid or out-of-range values.
- Structurally missing values.

The schema must document the original missing-value codes and any transformations applied during preprocessing.

Missing-value codes must not be interpreted as ordinary numerical measurements without justification.

Imputation procedures must be documented separately from the original data representation.

## 9. Dataset Splitting and Validation

Dataset partitions must be explicitly documented.

### 9.1 Training Dataset

Used for model fitting and learning.

### 9.2 Validation Dataset

Used for model selection, hyperparameter tuning, and model development decisions.

### 9.3 Test Dataset

Used for final internal performance assessment after model development decisions are completed.

### 9.4 External Validation Dataset

Used to assess model performance on an independent population, survey, time period, or data source.

External validation must not be treated as an ordinary random split of the same development sample.

### 9.5 Split Metadata

Each partition should record:

- Split identifier.
- Parent dataset identifier.
- Partition purpose.
- Sampling or partitioning strategy.
- Random seed, where applicable.
- Partition date.
- Observation count.
- Inclusion and exclusion criteria.

Where the sampling design or target population requires it, splitting must respect the appropriate sampling units and population structure.

The use of survey weights during model fitting and performance estimation must be documented separately.

## 10. External Validation and Distribution Shift

External validation datasets require additional metadata.

The documentation should include:

- Source population.
- Geographic coverage.
- Survey period.
- Data collection methodology.
- Variable harmonization rules.
- Differences in measurement definitions.
- Differences in sampling design.
- Differences in outcome prevalence.
- Potential covariate or concept shift.

Where datasets come from different countries or survey programmes, variable names and definitions must not be assumed equivalent.

Harmonization decisions must be documented before comparative evaluation.

Distribution shift should be assessed using justified statistical or machine learning methods rather than inferred solely from dataset names.

## 11. Data Leakage Prevention

The dataset schema must support identification of potential leakage sources.

Potential leakage risks include:

- Target variables appearing among predictive features.
- Post-outcome variables.
- Duplicate observations across partitions.
- Identifiers that encode target information.
- Preprocessing performed using held-out observations.
- Feature selection using test outcomes.
- External validation data influencing model development.
- Time-dependent information leaking into historical predictions.

Every dataset should have a documented leakage review.

The schema must preserve enough information to reproduce partitioning and preprocessing decisions.

## 12. Dataset Provenance

Each dataset must document its origin and processing history.

Required provenance information includes:

- Source organization or source category.
- Source dataset identifier, if applicable.
- Source citation or documentation reference.
- License or authorization status.
- Download or access date, where applicable.
- Processing history.
- Transformation scripts or references.
- Parent dataset identifier for derived data.
- Dataset checksum, where implemented.

Provenance records must not expose confidential information, credentials, or restricted access details.

## 13. Data Quality Requirements

Each dataset must undergo appropriate quality checks.

### 13.1 Structural Checks

- Required columns exist.
- Column names are unique.
- Data types match the variable dictionary.
- Record and variable counts are recorded.
- Dataset identifiers are valid.

### 13.2 Value Checks

- Values follow documented ranges.
- Categorical values use permitted codes.
- Missing-value conventions are respected.
- Unexpected duplicate records are investigated.
- Invalid weights are identified.
- Required survey design identifiers are checked.

### 13.3 Statistical Checks

Where appropriate, validation may include:

- Weight distribution summaries.
- Sample size by stratum.
- Cluster counts.
- Outcome distribution.
- Missingness rates.
- Feature distributions.
- Extreme-value checks.
- Partition consistency.

A failed check must be documented and reviewed rather than silently ignored.

## 14. Proposed Dataset Metadata Structure

The following JSON illustrates the proposed logical dataset metadata format.

It is a schema example, not a real dataset or an experimental result.

```json
{
  "dataset_metadata": {
    "dataset_id": "DS-T01-001",
    "dataset_name": "Synthetic Survey Design Example",
    "dataset_version": "1.0.0",
    "schema_version": "1.0",
    "task_id": "T01",
    "task_instance_id": "T01-001",
    "source_type": "synthetic",
    "file_format": "CSV",
    "record_count": 1000,
    "variable_count": 6
  },
  "variables": [
    {
      "variable_name": "respondent_id",
      "data_type": "identifier",
      "variable_role": "identifier",
      "description": "Synthetic observation identifier",
      "missing_value_codes": []
    },
    {
      "variable_name": "outcome",
      "data_type": "integer",
      "variable_role": "target",
      "description": "Illustrative binary outcome",
      "allowed_values": [0, 1],
      "missing_value_codes": []
    },
    {
      "variable_name": "survey_weight",
      "data_type": "float",
      "variable_role": "survey_weight",
      "description": "Illustrative survey analysis weight",
      "missing_value_codes": []
    },
    {
      "variable_name": "stratum_id",
      "data_type": "categorical",
      "variable_role": "stratum",
      "description": "Illustrative sampling stratum",
      "missing_value_codes": []
    },
    {
      "variable_name": "psu_id",
      "data_type": "identifier",
      "variable_role": "cluster",
      "description": "Illustrative primary sampling unit",
      "missing_value_codes": []
    },
    {
      "variable_name": "feature_1",
      "data_type": "float",
      "variable_role": "feature",
      "description": "Illustrative numerical predictor",
      "missing_value_codes": []
    }
  ],
  "survey_design": {
    "weight_variable": "survey_weight",
    "strata_variable": "stratum_id",
    "cluster_variable": "psu_id",
    "sampling_stages": null,
    "finite_population_correction": null,
    "replicate_weights": [],
    "variance_estimation_method": null
  },
  "partitions": {
    "training": null,
    "validation": null,
    "test": null,
    "external_validation": null
  },
  "provenance": {
    "source_type": "synthetic",
    "source_reference": null,
    "license_status": "synthetic_generated",
    "parent_dataset_id": null
  }
}
```

The example uses illustrative metadata and values. Null partition details indicate that partition definitions have not yet been assigned.

## 15. Proposed Dataset Directory Structure

The proposed repository layout is:

```text
data/
├── raw/
│   └── README.md
├── synthetic/
│   ├── T01/
│   ├── T02/
│   ├── T03/
│   ├── T04/
│   ├── T05/
│   ├── T06/
│   ├── T07/
│   └── T08/
├── processed/
│   ├── T01/
│   ├── T02/
│   ├── T03/
│   ├── T04/
│   ├── T05/
│   ├── T06/
│   ├── T07/
│   └── T08/
└── metadata/
    ├── datasets/
    ├── dictionaries/
    ├── provenance/
    └── validation/
```

Raw restricted datasets must not be copied into the public repository.

Large datasets should be managed separately when repository storage limits or data governance require it.

## 16. Data Formats and Storage

The benchmark may use the following formats.

| Format | Intended use |
|---|---|
| CSV | Simple tabular benchmark inputs |
| JSON | Dataset metadata and structured records |
| Parquet | Efficient storage of larger tabular datasets |
| YAML | Configuration and dataset references |

The selected format must preserve the required data types and missing-value semantics.

Format conversion must be documented and validated.

## 17. Relationship with Other Benchmark Components

The dataset schema integrates with:

- Repository architecture.
- Benchmark task schema.
- Task definitions.
- Reference solutions.
- Model execution engine.
- Grading framework.
- Statistical evaluation pipeline.
- Reporting system.

Task definitions identify which datasets are required.

Dataset metadata explains how those datasets are structured and sourced.

The execution pipeline consumes approved inputs, while the grading and analysis components use the relevant evaluation records.

## 18. Implementation Boundaries

This checkpoint defines dataset representation, metadata, governance, and validation requirements.

It does not implement:

- Actual datasets for all eight task families.
- Synthetic data generation scripts.
- Complete preprocessing pipelines.
- Statistical modelling.
- Automated external validation.
- Data quality execution tools.
- Experimental benchmark results.

These components will be developed in subsequent checkpoints.

## 19. Acceptance Criteria

CP-06C will be considered complete when:

1. Dataset identification fields are documented.
2. Synthetic, licensed, and derived datasets are distinguished.
3. Variable roles and dictionaries are defined.
4. Survey weights, strata, and clusters are covered.
5. Missing-value representation is documented.
6. Dataset partitioning is specified.
7. External validation metadata is documented.
8. Leakage prevention requirements are defined.
9. Data provenance and quality checks are specified.
10. A logical JSON metadata example is provided.
11. Directory and file format conventions are documented.
12. Restricted-data governance is addressed.
13. The document passes content and formatting review.

## 20. Architecture Status

**Status:** Proposed dataset schema specification.

This document establishes the logical data contract for SurveyML-Eval.

The schema will be refined during dataset engineering and validated against representative synthetic benchmark datasets before being treated as a stable benchmark release specification.