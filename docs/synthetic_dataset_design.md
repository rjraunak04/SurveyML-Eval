# Synthetic Dataset Design Specification

**Project:** SurveyML-Eval
**Checkpoint:** CP-07B
**Status:** Proposed design — pending review and approval
**Date:** 31 October 2026
**Parent document:** `docs/dataset_inventory.md`
**Schema reference:** `docs/dataset_schema.md`

---

## 1. Purpose

This document defines the statistical and engineering design for generating the synthetic datasets used in SurveyML-Eval.

The benchmark evaluates whether large language models can reason correctly about:

1. Complex survey sampling designs.
2. Survey-weighted predictive modelling.
3. Data leakage prevention.
4. Model validation strategies.
5. Class imbalance.
6. External validation and distribution shift.
7. Missing data and statistical uncertainty.
8. Calibration and interpretability.

The synthetic datasets will provide controlled experimental conditions with known data-generating mechanisms.

The design will support reproducible generation, reference solutions, deterministic validation, and benchmark grading.

All observations will be synthetic. No synthetic result will be presented as an empirical finding about India, Nepal, fertility prevalence, or any real population.

## 2. Overall Dataset Architecture

The benchmark will use one common synthetic survey population and derive task-specific dataset views.

### 2.1 Dataset groups

| Dataset ID | Dataset name | Design purpose |
|---|---|---|
| DS-01 | Core Synthetic Survey Population | Survey design and predictive modelling |
| DS-02 | Leakage Scenario Views | Controlled data leakage |
| DS-03 | Missingness and Imbalance Views | Missing data and class imbalance |
| DS-04 | External Population Views | External validation and distribution shift |

### 2.2 Dataset relationships

DS-01 will act as the development population.

DS-02 and DS-03 will be derived from DS-01 through controlled scenario transformations.

DS-04 will be generated using a modified population-generating mechanism to represent an independent external population.

The relationships will be recorded through parent dataset identifiers and scenario metadata.

### 2.3 Dataset lineage

```text
                   Synthetic Data Generator
                            |
                            v
                    DS-01 Core Population
                            |
               +------------+------------+
               |            |            |
               v            v            v
             DS-02        DS-03        DS-04
            Leakage    Missingness    External
           Scenarios   & Imbalance   Population
               |            |            |
               +------------+------------+
                            |
                            v
                      Task Instances
                         T01-T08
                            |
                            v
                    Reference Solutions
                            |
                            v
                     Benchmark Grading
```

## 3. Initial Dataset Size and Generation Parameters

The following are the initial engineering specifications.

| Parameter | Initial design |
|---|---|
| Core dataset sample size | 10,000 |
| External dataset sample size | 3,000 |
| Number of development strata | 8 |
| PSUs in development sampling frame | 160 |
| Selected development PSUs | 80 |
| Records selected per development PSU | 125 |
| Development sample size | 10,000 |
| Random seed | 42 |
| Outcome type | Binary |
| Data source | Synthetic |
| Primary data format | CSV |
| Metadata format | JSON |
| Python implementation | CP-07C |
| Initial schema version | 1.0 |

These values are engineering targets. Final realized counts and distributions must be checked by the generator and validation pipeline.

The generator must make sample sizes, seeds, and other design parameters configurable.

## 4. Synthetic Population Design

### 4.1 Population characteristics

The synthetic population will contain simulated demographic, socioeconomic, household, and survey-design characteristics.

The variables will be designed to support statistical modelling and survey analysis.

The population will not be calibrated to claim that it represents an actual country or survey.

### 4.2 Planned variable groups

| Variable | Type | Role |
|---|---|---|
| respondent_id | String/identifier | Unique observation identifier |
| age | Integer | Predictor |
| education_level | Categorical | Predictor |
| wealth_index | Numeric | Predictor |
| residence_type | Categorical | Predictor |
| employment_status | Categorical | Predictor |
| household_size | Integer | Predictor |
| media_access | Binary | Predictor |
| health_access | Binary | Predictor |
| simulated_outcome | Integer | Binary target |
| stratum_id | Categorical | Survey design |
| psu_id | Identifier | Survey design |
| survey_weight | Float | Survey design |

Additional fields may be introduced when required by a specific task instance.

The final variable dictionary will be maintained separately and must follow `docs/dataset_schema.md`.

### 4.3 Variable generation principles

Variables must have plausible internal statistical relationships.

Examples:

- Age will be generated within a defined adult age range.
- Education may be associated with wealth and employment.
- Wealth may be associated with media access and health access.
- Household size may vary across simulated strata.
- Residence type may influence socioeconomic characteristics.

These associations are controlled simulation assumptions, not empirical claims.

## 5. Complex Survey Sampling Design

### 5.1 Sampling design

The initial development dataset will use a two-stage stratified cluster sampling design.

The design will provide known inclusion probabilities and sampling weights.

### 5.2 Stratification

The development population will contain eight strata:

```text
STR-01
STR-02
STR-03
STR-04
STR-05
STR-06
STR-07
STR-08
```

Each stratum will contain 20 PSUs in the initial sampling frame.

Total development sampling-frame PSUs:

\[
8 \times 20 = 160
\]

### 5.3 First-stage sampling

Ten PSUs will be selected without replacement from each stratum.

Therefore:

\[
M_h = 20
\]

\[
m_h = 10
\]

Under equal-probability simple random sampling without replacement:

\[
\pi_{hj}^{(1)} = \frac{m_h}{M_h}
\]

\[
\pi_{hj}^{(1)} = \frac{10}{20}=0.5
\]

Where:

- \(h\) represents the stratum.
- \(j\) represents the PSU.
- \(M_h\) is the number of PSUs in the sampling frame.
- \(m_h\) is the number of selected PSUs.

Total selected PSUs:

\[
8 \times 10 = 80
\]

### 5.4 Second-stage sampling

Within each selected PSU, 125 observations will be sampled without replacement.

The initial PSU population sizes will vary between 180 and 320 observations.

Let:

- \(N_{hj}\) be the number of population units in PSU \(j\) of stratum \(h\).
- \(n_{hj}\) be the number of selected observations.

The conditional second-stage inclusion probability is:

\[
\pi_{hji}^{(2)} = \frac{n_{hj}}{N_{hj}}
\]

For the initial design:

\[
n_{hj}=125
\]

### 5.5 Overall inclusion probability

The overall inclusion probability is:

\[
\pi_{hji} =
\pi_{hj}^{(1)}
\times
\pi_{hji}^{(2)}
\]

### 5.6 Survey sampling weight

The base sampling weight will be calculated as:

\[
w_{hji} = \frac{1}{\pi_{hji}}
\]

Equivalently:

\[
w_{hji} =
\frac{1}
{\pi_{hj}^{(1)} \times \pi_{hji}^{(2)}}
\]

The generator must calculate weights from the actual selection probabilities.

Weights must not be assigned arbitrarily.

### 5.7 Finite population correction

Where applicable, the design will document the first-stage and second-stage sampling fractions.

First-stage sampling fraction:

\[
f_h^{(1)} = \frac{m_h}{M_h}
\]

Second-stage sampling fraction:

\[
f_{hj}^{(2)} = \frac{n_{hj}}{N_{hj}}
\]

The corresponding finite population information must be retained in metadata.

### 5.8 Survey design metadata

The generated dataset must support:

- Stratum identifiers.
- PSU identifiers.
- Base sampling weights.
- First-stage inclusion probabilities.
- Second-stage inclusion probabilities.
- Sampling-stage definitions.
- Finite population information.
- Variance estimation documentation.

Replicate weights will remain optional in the initial version. If implemented, their generation method must be explicitly documented.

## 6. Outcome Data-Generating Process

### 6.1 Outcome definition

The target variable will be a simulated binary outcome.

\[
Y_i \in \{0,1\}
\]

The outcome is designed for statistical and machine learning evaluation.

It does not represent actual fertility risk or any measured real-world health outcome.

### 6.2 Logistic outcome mechanism

The outcome will be generated through a logistic model.

\[
P(Y_i=1\mid X_i)=
\frac{1}{1+\exp(-\eta_i)}
\]

Where:

\[
\eta_i =
\beta_0 +
\beta_1X_{i1}+
\beta_2X_{i2}+
\cdots+
\beta_pX_{ip}
\]

Here:

- \(\beta_0\) is the intercept.
- \(\beta_1,\ldots,\beta_p\) are simulation coefficients.
- \(X_{i1},\ldots,X_{ip}\) are simulated predictors.

The outcome will be sampled from a Bernoulli distribution:

\[
Y_i \sim \operatorname{Bernoulli}(p_i)
\]

where \(p_i=P(Y_i=1\mid X_i)\).

### 6.2.1 Population-level outcome generation

The synthetic predictors and binary outcomes will be generated for the full finite population before the survey sample is selected.

The two-stage sampling procedure will then select observations from this generated population. This preserves the relationship between the finite population, outcome-generation process, inclusion probabilities and survey sampling weights.

The generator must retain the population-level information required to reproduce the sampling design and validate the resulting sample.

### 6.3 Proposed coefficient specification

The initial illustrative coefficient structure is:

| Predictor | Symbol | Proposed coefficient |
|---|---|---:|
| Age (standardized) | \(\beta_1\) | 0.45 |
| Education indicator | \(\beta_2\) | -0.35 |
| Wealth index (standardized) | \(\beta_3\) | -0.40 |
| Residence indicator | \(\beta_4\) | 0.20 |
| Employment indicator | \(\beta_5\) | -0.15 |
| Household size (standardized) | \(\beta_6\) | 0.30 |
| Media access | \(\beta_7\) | -0.25 |
| Health access | \(\beta_8\) | -0.20 |

The intercept and final coding conventions will be calibrated and documented during implementation.

These coefficients are simulation parameters, not estimates from NFHS-5 or Nepal DHS.

### 6.4 Ground-truth preservation

The benchmark will retain:

- True coefficient values.
- Outcome-generation formula.
- Random seed.
- Predictor distributions.
- Outcome probabilities.
- Generated target values.

The model-facing benchmark inputs must not expose hidden reference answers or private grading information.

## 7. DS-02: Data Leakage Scenario Design

DS-02 will be constructed using controlled modifications of the core population.

### 7.1 Scenario LEAK-01: Direct target leakage

A feature will contain a direct copy of the target.

Example:

```text
simulated_outcome = 1
leak_target_copy = 1
```

Expected evaluation:

- Identify the copied target.
- Explain why it creates leakage.
- Recommend removal from the predictor set.

### 7.2 Scenario LEAK-02: Identifier leakage

A deliberately constructed identifier will encode information associated with the target.

Expected evaluation:

- Identify suspicious identifier patterns.
- Explain the leakage mechanism.
- Recommend safe identifier handling.

### 7.3 Scenario LEAK-03: Post-outcome leakage

A variable will be generated using information only available after the outcome.

Expected evaluation:

- Identify temporal leakage.
- Explain why the feature cannot be used for prospective prediction.
- Recommend a valid feature-availability cutoff.

### 7.4 Scenario LEAK-04: Preprocessing leakage

A task will describe preprocessing performed before the train/test split.

Examples:

- Imputation using all observations.
- Feature selection using test outcomes.
- Scaling using held-out observations.

Expected evaluation:

- Identify the leakage source.
- Explain its effect on evaluation.
- Recommend fitting transformations only on training data.

### 7.5 Scenario LEAK-05: Duplicate partition leakage

Controlled duplicate records will be introduced across development partitions.

Expected evaluation:

- Identify duplicate records.
- Explain the risk of inflated evaluation.
- Recommend group-aware partitioning or deduplication.

### 7.6 Leakage ground truth

Each leakage task instance will have:

- Scenario ID.
- Leakage type.
- Affected fields.
- Leakage mechanism.
- Correct diagnosis.
- Recommended correction.
- Reference grading criteria.

## 8. DS-03: Missingness and Class Imbalance Design

### 8.1 Purpose

DS-03 will evaluate reasoning about missing-data mechanisms, statistical uncertainty, and imbalanced outcomes.

### 8.2 MCAR scenario

Missingness will be introduced independently of observed and unobserved data values.

\[
P(R_i=1\mid X_i,Y_i)=c
\]

Where:

- \(R_i=1\) indicates an observed value.
- \(c\) is a controlled observation probability.

The missingness rate will be configurable.

### 8.3 MAR scenario

Missingness will depend on observed variables.

\[
P(R_i=1\mid X_i,Y_i)
=
\operatorname{logit}^{-1}
(\alpha_0+\alpha_1X_{i1}+\alpha_2X_{i2})
\]

The mechanism will be documented so that the missingness process is known.

### 8.4 MNAR scenario

Missingness will depend on the variable's own unobserved value or another unobserved quantity.

\[
P(R_i=1\mid X_i)
=
\operatorname{logit}^{-1}(\gamma_0+\gamma_1X_i)
\]

The benchmark will explicitly document that MNAR cannot generally be identified from observed data alone without additional assumptions.

### 8.5 Missingness scenarios

Initial missingness-rate targets:

| Scenario | Target missingness rate |
|---|---:|
| MISS-01 | 5% |
| MISS-02 | 10% |
| MISS-03 | 20% |
| MISS-04 | 30% |

These are experimental settings, not empirical missingness estimates.

### 8.6 Missing-value representation

The implementation must follow the missing-value conventions in `docs/dataset_schema.md`.

The generator must distinguish genuine missing values from valid zero values and special category codes.

Missingness indicators may be retained in reference metadata where required.

### 8.7 Class imbalance scenarios

The benchmark will include controlled outcome distributions.

Initial target scenarios:

| Scenario | Approximate minority-class proportion |
|---|---:|
| IMB-01 | 40% |
| IMB-02 | 20% |
| IMB-03 | 10% |
| IMB-04 | 5% |

The final observed proportions must be measured and recorded rather than assumed from the target settings.

### 8.8 Evaluation considerations

The benchmark will examine whether LLMs understand:

- Accuracy limitations under imbalance.
- Precision and recall.
- F1-score.
- ROC-AUC.
- PR-AUC.
- Class-specific performance.
- Sampling-weighted metrics.
- Appropriate uncertainty estimates.

## 9. DS-04: External Population and Distribution Shift

### 9.1 Purpose

DS-04 will evaluate model generalization across an independently generated population.

The external population will have its own sampling frame and documented generation parameters.

### 9.2 External sample design

Initial external sample target:

\[
n_{\text{external}}=3000
\]

The external sample will be generated independently from the development sample.

Its sampling design and inclusion probabilities will be documented separately.

The external population must not be constructed by randomly splitting the development sample.

### 9.3 Covariate shift

Covariate shift occurs when:

\[
P_{\text{development}}(X)
\neq
P_{\text{external}}(X)
\]

while the conditional relationship may remain approximately stable:

\[
P_{\text{development}}(Y\mid X)
\approx
P_{\text{external}}(Y\mid X)
\]

The generator will modify selected predictor distributions to construct this scenario.

### 9.4 Outcome prevalence shift

Outcome prevalence shift will be introduced through a controlled change in the outcome-generation intercept.

\[
\beta_{0,\text{external}}
\neq
\beta_{0,\text{development}}
\]

This changes the marginal outcome distribution while retaining the documented predictor mechanism, unless a task explicitly specifies additional changes.

### 9.5 Concept shift

Concept shift will be introduced by modifying selected predictor coefficients.

\[
\beta_{j,\text{external}}
\neq
\beta_{j,\text{development}}
\]

The modified relationships will be recorded in the scenario metadata.

### 9.6 External validation metadata

The external dataset must record:

- External dataset identifier.
- Parent or reference dataset identifier.
- Population-generation parameters.
- Sampling design.
- Variable harmonization rules.
- Outcome-generation parameters.
- Distribution-shift scenario.
- Random seed.
- Observation count.
- Validation status.

### 9.7 Evaluation requirements

The benchmark will examine:

- Internal versus external performance.
- Differences in outcome prevalence.
- Changes in feature distributions.
- Calibration differences.
- Generalization performance.
- Appropriate adaptation or recalibration recommendations.

## 10. DS-01 and DS-04: Calibration and Interpretability Design

The core and external populations will support T08.

### 10.1 Calibration evaluation

The benchmark will examine:

- Calibration-in-the-large.
- Calibration slope.
- Brier score.
- Reliability diagrams.
- Predicted versus observed risk.
- Changes in calibration under distribution shift.

### 10.2 Interpretability evaluation

The benchmark will include tasks involving:

- Logistic model coefficients.
- Feature importance.
- SHAP-based explanations.
- Global versus local explanations.
- Interpretation of feature effects.
- Limitations of associational explanations.

### 10.3 Ground-truth interpretability

Because the outcome is generated using known coefficients, the benchmark can compare model explanations with the underlying data-generating mechanism.

However, true generating coefficients and fitted model coefficients must not be treated as identical.

The benchmark will distinguish:

- True simulation parameters.
- Estimated model parameters.
- Model-specific feature importance.
- Post-hoc explanation outputs.

## 11. Randomness and Reproducibility

### 11.1 Random seed

The initial master random seed will be:

```text
42
```

### 11.2 Independent random streams

The generator should use separate random streams for:

- Population generation.
- Survey sampling.
- Outcome generation.
- Missingness.
- Class imbalance scenarios.
- Leakage scenarios.
- External population generation.

This will reduce accidental dependence between unrelated generation stages.

### 11.3 Reproducibility requirements

Each generated dataset must record:

- Master random seed.
- Component-level random seeds or stream identifiers.
- Generator version.
- Dataset version.
- Schema version.
- Generation parameters.
- Record count.
- Variable count.
- Dataset checksum.

### 11.4 Deterministic regeneration

The same generator version, parameters, and random seeds must produce identical outputs under a controlled software environment.

The implementation must record relevant package versions and environment information.

## 12. Dataset Metadata Design

Each dataset must have a corresponding metadata record.

The logical metadata structure will follow `docs/dataset_schema.md`.

Example:

```json
{
  "dataset_metadata": {
    "dataset_id": "DS-01",
    "dataset_name": "Core Synthetic Survey Population",
    "dataset_version": "1.0.0",
    "schema_version": "1.0",
    "source_type": "synthetic",
    "file_format": "CSV",
    "record_count": 10000,
    "random_seed": 42,
    "parent_dataset_id": null
  },
  "survey_design": {
    "design_type": "stratified_two_stage_cluster_sampling",
    "number_of_strata": 8,
    "frame_psus_per_stratum": 20,
    "selected_psus_per_stratum": 10,
    "observations_per_selected_psu": 125,
    "weight_variable": "survey_weight",
    "strata_variable": "stratum_id",
    "cluster_variable": "psu_id",
    "sampling_stages": 2,
    "variance_estimation_method": null
  },
  "outcome": {
    "variable_name": "simulated_outcome",
    "data_type": "integer",
    "allowed_values": [0, 1],
    "generation_method": "logistic_bernoulli"
  },
  "validation": {
    "structural_checks": "pending",
    "value_checks": "pending",
    "statistical_checks": "pending",
    "leakage_review": "pending"
  }
}
```

This is an illustrative metadata specification, not a generated dataset or experimental result.

Actual metadata values must be populated by the generator.

## 13. Dataset-to-Task Mapping

| Task ID | Task family | Dataset | Main design component |
|---|---|---|---|
| T01 | Complex Survey Design and Weight Interpretation | DS-01 | Strata, PSU, weights and sampling probabilities |
| T02 | Survey-Weighted Predictive Modelling | DS-01 | Survey-aware modelling and evaluation |
| T03 | Data Leakage Detection and Prevention | DS-02 | Controlled leakage scenarios |
| T04 | Validation Strategy Selection | DS-01 and DS-02 | Partitioning and validation |
| T05 | Class Imbalance and Performance Evaluation | DS-03 | Controlled outcome imbalance |
| T06 | External Validation and Distribution Shift | DS-04 | Independent external population |
| T07 | Missing Data and Statistical Uncertainty | DS-03 | MCAR, MAR and MNAR |
| T08 | Model Calibration and Interpretability | DS-01 and DS-04 | Calibration and explanation under shift |

## 14. Statistical Validation Plan

The generated datasets will undergo the following checks.

### 14.1 Structural validation

- Expected dataset dimensions.
- Unique variable names.
- Valid data types.
- Unique respondent identifiers within the intended identifier scope.
- Valid dataset and scenario identifiers.

### 14.2 Survey design validation

- Valid strata identifiers.
- Valid PSU identifiers.
- Positive sampling weights.
- Inclusion probabilities within valid bounds.
- Correct calculation of inverse-probability weights.
- Consistent sample counts.
- Correct sampling fractions.

### 14.3 Outcome validation

- Binary outcome coding.
- Observed class proportions.
- Outcome probability ranges.
- Consistency with the documented logistic mechanism.

### 14.4 Missingness validation

- Missingness rates.
- Missingness mechanism configuration.
- Missing-value coding.
- Scenario-specific missingness patterns.

### 14.5 Distribution-shift validation

- Development versus external feature distributions.
- Outcome prevalence differences.
- Predictor-outcome relationship differences.
- Correct scenario identification.

### 14.6 Leakage validation

- Target-copy detection.
- Identifier leakage checks.
- Duplicate partition checks.
- Post-outcome variable checks.
- Preprocessing leakage review.

Failed checks must be recorded and investigated.

## 15. Proposed Repository Integration

The design will be implemented using the repository architecture already documented in `docs/repository_architecture.md` and `docs/dataset_schema.md`.

The data directory will follow the approved proposed structure:

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

The executable generator will be implemented in CP-07C.

This checkpoint does not create the final datasets or implement the generator.

## 16. Implementation Boundaries

CP-07B defines:

- Synthetic population design.
- Survey sampling design.
- Variable-generation assumptions.
- Outcome-generation mechanism.
- Leakage scenarios.
- Missingness scenarios.
- Class imbalance scenarios.
- External population scenarios.
- Calibration and interpretability design.
- Reproducibility requirements.
- Statistical validation requirements.

CP-07B does not implement:

- Executable data-generation scripts.
- Final CSV datasets.
- Final metadata files.
- Automated validation scripts.
- Model training pipelines.
- Benchmark execution.
- Experimental model evaluation.

These activities belong to subsequent checkpoints.

## 17. Open Decisions

The following items require confirmation or calibration during implementation:

1. Final intercept calibration for the binary outcome.
2. Final predictor distributions.
3. Final variable coding conventions.
4. Whether replicate weights will be implemented.
5. Whether finite population corrections will be used in variance estimation.
6. Final external population shift magnitudes.
7. Final missingness scenario parameters.
8. Final class imbalance generation procedure.
9. Final partition proportions.
10. Package and software environment versions.

Any change affecting the statistical design must be documented.

## 18. Completion Criteria

CP-07B will be considered complete when:

- The four dataset groups are fully designed.
- All eight task families have dataset mappings.
- The synthetic population structure is documented.
- The two-stage survey sampling design is specified.
- Inclusion probability and sampling weight formulas are defined.
- Survey design metadata requirements are documented.
- The binary outcome-generating mechanism is specified.
- Leakage scenarios are documented.
- MCAR, MAR and MNAR mechanisms are specified.
- Class imbalance scenarios are defined.
- External validation and distribution-shift scenarios are specified.
- Calibration and interpretability requirements are documented.
- Randomness and reproducibility requirements are specified.
- Metadata design is documented.
- Statistical validation requirements are defined.
- The document is consistent with the dataset schema and repository architecture.
- The document passes content and formatting review.
- The approved document is committed to the repository.

**End of CP-07B.**wc -l docs/synthetic_dataset_design.md