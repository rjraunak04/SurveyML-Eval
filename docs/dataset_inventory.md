# Dataset Inventory and Engineering Plan

**Project:** SurveyML-Eval
**Checkpoint:** CP-07A
**Status:** Draft — pending final review and approval
**Date:** 31 October 2026

## 1. Purpose

This document defines the planned synthetic dataset inventory and engineering requirements for SurveyML-Eval.

The inventory connects the eight benchmark task families (T01–T08) to a consistent synthetic survey population and its task-specific dataset views.

The objective is to support reproducible evaluation of large language models on:

- Complex survey interpretation.
- Survey-weighted predictive modelling.
- Data leakage detection and prevention.
- Validation strategy selection.
- Class imbalance and performance evaluation.
- External validation and distribution shift.
- Missing data and statistical uncertainty.
- Model calibration and interpretability.

All generated records will be synthetic. They will not represent actual individuals or be presented as empirical estimates of fertility prevalence in India or any other country.

## 2. Dataset Design Strategy

The benchmark will use one coherent synthetic population as its foundation.

Task-specific datasets will be derived from this population through controlled transformations and scenarios.

This strategy is intended to:

- Preserve consistency across related benchmark tasks.
- Make comparisons between task families meaningful.
- Enable controlled experiments with known data-generating mechanisms.
- Avoid unnecessary duplication of unrelated populations.
- Support reproducibility through documented generation parameters and random seeds.
- Maintain traceability between base populations and derived dataset views.

The dataset views described below are logical benchmark assets. They do not necessarily require separate, independently generated populations.

Each derived dataset must retain its parent dataset identifier and document the transformations applied.

## 3. Dataset Inventory

The initial benchmark will contain four logical dataset groups.

| Dataset ID | Dataset name | Purpose |
|---|---|---|
| DS-01 | Core Synthetic Survey Population | Base population with survey design information and predictive features |
| DS-02 | Leakage Scenario Views | Controlled examples of target leakage and identifier leakage |
| DS-03 | Missingness and Imbalance Views | Controlled missing-data mechanisms and class imbalance |
| DS-04 | External Population Views | External validation and distribution-shift scenarios |

### 3.1 DS-01: Core Synthetic Survey Population

**Purpose:** Provide the common foundation for survey-design interpretation and predictive modelling tasks.

Planned components:

- Synthetic demographic and socioeconomic variables.
- A simulated binary outcome.
- Sampling strata identifiers.
- Primary sampling unit (PSU) identifiers.
- Survey sampling weights.
- Additional survey design metadata, where applicable.
- Documented relationships between predictors and outcome.

The outcome will be generated using an explicit data-generating process.

Its mechanism and parameters will be documented so that benchmark reference solutions can use the known ground truth.

The simulated outcome must not be interpreted as a real-world fertility prevalence estimate.

### 3.2 DS-02: Leakage Scenario Views

**Purpose:** Evaluate whether models can identify and prevent data leakage.

Planned scenarios:

- Direct target leakage.
- Identifier-based leakage.
- Post-outcome information.
- Improper preprocessing before data splitting.
- Inappropriate train/test separation.
- Duplicate observations across partitions.
- Leakage through feature selection or preprocessing.

Each scenario will document the source of leakage, the expected risk, and the appropriate corrective action.

### 3.3 DS-03: Missingness and Imbalance Views

**Purpose:** Evaluate statistical reasoning under incomplete data and unequal class distributions.

Planned scenarios:

- Missing completely at random (MCAR).
- Missing at random (MAR).
- Controlled missing not at random (MNAR).
- Different levels of missingness.
- Controlled class imbalance.
- Changes in missingness patterns across dataset partitions.

The generation process will document how missingness is introduced and how the outcome distribution is modified.

### 3.4 DS-04: External Population Views

**Purpose:** Evaluate external validation and distribution-shift reasoning.

Planned scenarios:

- Covariate distribution shift.
- Outcome prevalence shift.
- Changes in selected predictor relationships.
- Differences between development and external populations.
- Differences in simulated sampling design.

The external population will be derived using documented changes to the base data-generating process.

It will not be treated as real Nepal DHS data or as an empirical representation of any country.

## 4. Task-to-Dataset Mapping

The following table defines the primary dataset mapping for the eight benchmark task families.

| Task ID | Task family | Primary dataset |
|---|---|---|
| T01 | Complex Survey Design and Weight Interpretation | DS-01 |
| T02 | Survey-Weighted Predictive Modelling | DS-01 |
| T03 | Data Leakage Detection and Prevention | DS-02 |
| T04 | Validation Strategy Selection | DS-01 and DS-02 |
| T05 | Class Imbalance and Performance Evaluation | DS-03 |
| T06 | External Validation and Distribution Shift | DS-04 |
| T07 | Missing Data and Statistical Uncertainty | DS-03 |
| T08 | Model Calibration and Interpretability | DS-01 and DS-04 |

Task instances may combine multiple dataset views when necessary.

The exact input files, expected outputs, reference solutions, and grading criteria will be specified during task-instance construction.

## 5. Variable Groups and Survey Design Metadata

The dataset inventory will use the variable definitions and conventions established in `docs/dataset_schema.md`.

### 5.1 Identification Variables

Planned identification fields include:

- Synthetic respondent or observation identifier.
- Dataset identifier.
- Dataset version.
- Task identifier.
- Task-instance identifier, where applicable.
- Scenario identifier, where applicable.

Identifiers must not encode outcome information or introduce unintended predictive leakage.

### 5.2 Predictive Variables

Planned variable groups include:

- Demographic characteristics.
- Socioeconomic characteristics.
- Household-related characteristics.
- Other simulated predictors justified by the data-generating process.

Each variable must have a documented:

- Variable name.
- Data type.
- Variable role.
- Description.
- Allowed values or range.
- Missing-value convention.

### 5.3 Outcome Variables

The core population will contain a simulated binary outcome.

The documentation must specify:

- Outcome definition.
- Outcome variable name.
- Data type and allowed values.
- Outcome-generation mechanism.
- Parameters used in the data-generating process.
- Expected outcome distribution.

The simulated outcome is illustrative and must not be interpreted as real-world fertility prevalence.

### 5.4 Survey Design Variables

The synthetic survey population will document the following design components:

| Component | Description |
|---|---|
| Sampling weight | Weight assigned to each sampled observation |
| Stratum identifier | Identifier for the sampling stratum |
| PSU identifier | Primary sampling unit or cluster identifier |
| Sampling stages | Description of sampling stages, where applicable |
| Finite population correction | FPC information, where applicable |
| Replicate weights | Replicate-weight variables, if implemented |
| Variance estimation method | Documented method for variance estimation |

Fields that are not applicable or not implemented must be explicitly represented as null or otherwise documented according to the dataset schema.

Survey design metadata must be sufficient to understand how the sampling design affects estimation and uncertainty.

### 5.5 Scenario Variables

Task-specific scenario views may contain:

- Missingness indicators.
- Leakage indicators.
- Population or domain indicators.
- Scenario identifiers.
- Partition identifiers.

Scenario variables must not automatically be treated as predictive features.

Their availability must follow the corresponding task definition.

## 6. Initial Engineering Targets

The following values are preliminary planning targets, not finalized dataset specifications.

| Parameter | Initial proposal |
|---|---|
| Core population size | 10,000 observations |
| External population size | 3,000 observations |
| Outcome type | Binary simulated outcome |
| Reproducibility seed | 42 |
| Primary format | CSV |
| Metadata format | JSON |
| Data source | Synthetic generation |

Final sample sizes, variable definitions, and file formats must be checked against the complete dataset schema and benchmark execution constraints before implementation.

The final dataset sizes may be adjusted based on task complexity, execution runtime, storage limits, and grading requirements.

## 7. Dataset Partitioning and Validation Strategy

Dataset partitions must be explicitly documented.

### 7.1 Training Dataset

Used for model fitting and learning.

### 7.2 Validation Dataset

Used for model selection, hyperparameter tuning, and model development decisions.

### 7.3 Test Dataset

Used for final internal performance assessment after model development decisions are completed.

### 7.4 External Validation Dataset

Used to evaluate model performance on an independent synthetic population or independently generated population scenario.

External validation must not be treated as an ordinary random split of the same development sample.

### 7.5 Split Metadata

Each partition must record:

- Split identifier.
- Parent dataset identifier.
- Partition purpose.
- Sampling or partitioning strategy.
- Random seed, where applicable.
- Partition date.
- Observation count.
- Inclusion and exclusion criteria.

Where appropriate, partitioning must respect the sampling units and population structure.

The use of survey weights during model fitting and performance estimation must be documented separately.

## 8. External Validation and Distribution Shift

DS-04 will provide controlled external population scenarios.

The documentation will include:

- Source population description.
- Geographic coverage as a simulated scenario attribute, where relevant.
- Simulated survey period.
- Data-generation methodology.
- Variable harmonization rules.
- Differences in measurement definitions.
- Differences in sampling design.
- Differences in outcome prevalence.
- Potential covariate shift.
- Potential concept shift.

The external population will be generated through documented modifications to the base data-generating process.

The benchmark must distinguish between:

1. Covariate distribution shift.
2. Outcome prevalence shift.
3. Changes in predictor-outcome relationships.

The presence and magnitude of distribution shift must be verified using statistical summaries and appropriate analytical methods rather than inferred solely from dataset labels.

Synthetic external data must not be represented as actual NFHS-5 or Nepal DHS observations.

## 9. Data Leakage Prevention

Every dataset view must undergo a documented leakage review.

Potential leakage scenarios include:

- Target variables appearing among predictive features.
- Post-outcome information.
- Duplicate observations across partitions.
- Identifiers that encode target information.
- Preprocessing performed before data splitting.
- Feature selection using test outcomes.
- External validation data influencing model development.
- Time-dependent information leaking into historical predictions.

DS-02 will contain intentionally constructed leakage scenarios.

Each scenario must document:

- Leakage type.
- Affected variables or processing steps.
- Why the leakage occurs.
- Expected model-development risk.
- Appropriate prevention strategy.
- Expected reference solution.

The dataset generation process must preserve enough information to reproduce partitioning and preprocessing decisions.

Reference answers and grading keys must remain separate from model-facing dataset inputs.

## 10. Dataset Provenance and Governance

### 10.1 Synthetic Dataset Provenance

Each synthetic dataset must document:

- Source category.
- Dataset identifier.
- Dataset version.
- Parent dataset identifier, where applicable.
- Generator or transformation reference.
- Processing history.
- Generation parameters.
- Random seed.
- Dataset checksum, where implemented.

### 10.2 External Dataset Governance

The initial public benchmark release will use synthetic data.

Restricted NFHS-5 and Nepal DHS microdata must not be included in the public repository unless redistribution is explicitly authorized.

Any future use of external datasets must document:

- Source organization.
- Source dataset identifier.
- Source citation or documentation.
- License or authorization status.
- Download or access date, where applicable.
- Permitted use.
- Redistribution restrictions.
- Required attribution.

Provenance documentation must not expose confidential information, credentials, or restricted access details.

All synthetic records must be clearly labelled as synthetic.

## 11. Data Quality and Statistical Validation

Each generated dataset must pass appropriate structural, value, statistical, and scenario-specific checks.

### 11.1 Structural Checks

- Required columns exist.
- Column names are unique.
- Data types match the variable dictionary.
- Record and variable counts are recorded.
- Dataset identifiers are valid.

### 11.2 Value Checks

- Values follow documented ranges.
- Categorical variables use permitted codes.
- Missing-value conventions are respected.
- Unexpected duplicate records are investigated.
- Invalid sampling weights are identified.
- Required survey design identifiers are checked.

### 11.3 Statistical Checks

Where applicable, validation should include:

- Sampling-weight distribution summaries.
- Sample size by stratum.
- Number of clusters or PSUs.
- Outcome distribution.
- Missingness rates.
- Feature distributions.
- Extreme-value checks.
- Partition consistency.
- Class distribution across partitions.

### 11.4 Scenario Validation

Additional checks will verify:

- Correct generation of MCAR, MAR, and MNAR scenarios.
- Intended class imbalance.
- Intended distribution shifts.
- Correct construction of leakage scenarios.
- Absence of unintended leakage.
- Consistency between parent and derived datasets.

A failed validation check must be documented and reviewed rather than silently ignored.

Validation results will be retained for each dataset version.

## 12. Reproducibility, Formats, and Repository Organization

### 12.1 Reproducibility Requirements

Each dataset release must record:

- Dataset ID and version.
- Schema version.
- Generator version.
- Random seed.
- Generation parameters.
- Number of records.
- Number of variables.
- Data dictionary reference.
- Validation status.
- Generation timestamp.
- Parent dataset identifier, where applicable.

Changes to generation logic that affect the generated data must result in a documented version update.

### 12.2 Supported Data Formats

| Format | Intended use |
|---|---|
| CSV | Tabular benchmark inputs |
| JSON | Dataset metadata and structured records |
| Parquet | Efficient storage of larger tabular datasets |
| YAML | Configuration and dataset references |

The selected format must preserve required data types and missing-value semantics.

Format conversions must be documented and validated.

### 12.3 Repository Directory Structure

The dataset organization will follow the structure proposed in `docs/dataset_schema.md`.

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

The task-specific folders will contain the relevant dataset views and processed benchmark inputs.

The metadata folders will hold dataset descriptions, variable dictionaries, provenance records, and validation reports.

Restricted raw datasets must not be copied into the public repository.

Large datasets should be managed separately when repository storage limits or data governance require it.

The final code-generation directory must remain consistent with `docs/repository_architecture.md` rather than introducing an independent source-code layout.

## 13. Open Decisions

The following decisions remain open until implementation planning:

1. Final sample sizes for each dataset view.
2. Exact variable dictionary and coding.
3. Survey sampling design and weight construction.
4. Outcome-generation mechanism and parameters.
5. Missingness rates and mechanisms.
6. Magnitude and type of external distribution shift.
7. Exact file naming and versioning conventions.
8. Whether derived dataset views should be materialized or generated dynamically.
9. Final partition proportions and partitioning strategy.
10. Whether replicate weights and finite population corrections will be implemented.

These decisions must be documented before the synthetic generator is finalized.

## 14. Completion Criteria

CP-07A will be considered complete when:

- The dataset inventory is documented.
- All eight task families are mapped to dataset views.
- Dataset purposes and generation assumptions are explicit.
- Survey design metadata requirements are covered.
- Training, validation, test, and external validation partitions are documented.
- External validation metadata requirements are covered.
- Leakage prevention requirements are documented.
- Data provenance and governance requirements are documented.
- Structural, value, and statistical quality checks are specified.
- Reproducibility and versioning requirements are documented.
- The repository layout is consistent with the dataset schema.
- The inventory is consistent with the complete dataset schema.
- The document passes content and formatting review.
- The approved document is committed to the repository.

**End of CP-07A.**
