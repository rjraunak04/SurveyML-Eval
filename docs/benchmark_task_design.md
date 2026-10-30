# SurveyML-Eval: Benchmark Task Design

## Document Purpose

This document defines eight benchmark task families for evaluating Large Language Models (LLMs) on survey-aware statistical reasoning and predictive machine learning workflows.

The benchmark evaluates whether LLMs can interpret complex survey structures, make appropriate modelling decisions, avoid analytical errors, select valid evaluation strategies, and produce reproducible predictive workflows.

| Task ID | Task Family |
|---|---|
| T01 | Complex Survey Design and Weight Interpretation |
| T02 | Survey-Weighted Predictive Modelling |
| T03 | Data Leakage Detection and Prevention |
| T04 | Validation Strategy Selection |
| T05 | Class Imbalance and Performance Evaluation |
| T06 | External Validation and Distribution Shift |
| T07 | Missing Data and Statistical Uncertainty |
| T08 | Model Calibration and Interpretability |

---

# T01: Complex Survey Design and Weight Interpretation

## 1. Task Overview

**Task ID:** T01

**Category:** Survey Statistics and Statistical Reasoning

**Difficulty:** Intermediate to Advanced

## 2. Real-World Problem

Large-scale population surveys frequently use complex sampling designs rather than simple random sampling.

These designs may include sampling weights, stratification, primary sampling units (PSUs), multistage sampling, domain estimation, and unequal selection probabilities.

An LLM must understand how these features affect population estimates, uncertainty, and downstream statistical analysis.

## 3. Evaluation Objectives

Evaluate whether an LLM can:

1. Identify the purpose of sampling weights.
2. Distinguish strata from PSUs.
3. Interpret multistage sampling structures.
4. Identify when design-based variance estimation is required.
5. Recognise incorrect use of unweighted population estimates.
6. Recommend an appropriate survey-analysis strategy.
7. Distinguish population estimation from predictive modelling.
8. Recognise insufficient survey-design information.
9. Identify implications of domain or subpopulation analysis.

## 4. Input Specification

A controlled synthetic survey dataset or compact design scenario will be provided.

Example:

```json
{
  "task_id": "T01_001",
  "sample_size": 5000,
  "weight_variable": "sample_weight",
  "strata_variable": "stratum_id",
  "psu_variable": "psu_id",
  "outcome_variable": "health_risk",
  "sampling_design": "stratified_multistage_cluster_sampling",
  "analysis_objective": "population_prevalence_estimation",
  "domain_variable": "urban_rural"
}
```

A data dictionary will explain variable definitions, weight construction where available, sampling stages, target population, and domain definitions.

Some instances may intentionally omit information to test whether a model recognises insufficient documentation.

## 5. Expected Model Output

```json
{
  "weight_purpose": "Explanation of the sampling weight",
  "strata_role": "Explanation of stratification",
  "psu_role": "Explanation of primary sampling units",
  "analysis_objective": "Identification of the statistical objective",
  "variance_method": "Recommended variance estimation approach",
  "domain_analysis": "Explanation of domain analysis",
  "missing_information": [],
  "analysis_warning": "Potential statistical error",
  "recommended_workflow": [
    "Step 1",
    "Step 2",
    "Step 3"
  ]
}
```

## 6. Reference Solution

The human-reviewed reference solution should establish that:

- Sampling weights account for unequal selection probabilities and, depending on their construction, nonresponse and calibration adjustments.
- Strata represent sampling subdivisions.
- PSUs represent primary sampling units selected at the first sampling stage.
- Variance estimation should reflect the actual survey design.
- Treating complex survey observations as a simple random sample without justification can produce incorrect standard errors and confidence intervals.
- Domain estimation should respect the survey design.

Potential variance methods include Taylor series linearization, jackknife, BRR, and other documented replication methods.

No single variance method should be prescribed universally.

## 7. Scoring and Grading Logic

**Total: 10 points**

| Component | Points |
|---|---:|
| Interpretation of weights | 2 |
| Distinction between strata and PSUs | 2 |
| Variance estimation recommendation | 2 |
| Identification of design errors | 1 |
| Target population and domain requirements | 1 |
| Structured output and workflow | 2 |
| **Total** | **10** |

Use deterministic JSON checks, reference-based statistical checks, and human review for ambiguous explanations.

Multiple defensible methods should be accepted when justified by the task specification.

## 8. Common LLM Failure Modes

1. Treating survey weights as ordinary frequency counts.
2. Confusing strata and PSUs.
3. Ignoring clustering.
4. Recommending ordinary standard errors without considering design.
5. Assuming all survey weights have identical construction.
6. Making unsupported claims when information is incomplete.
7. Ignoring domain-analysis requirements.
8. Confusing population estimation with prediction.

## 9. Reproducibility Requirements

Each instance must include a unique ID, survey-design description, data dictionary, target population, reference answer, output schema, grading rules, versioned input, difficulty label, and accepted alternative answers.

No confidential or unauthorised survey microdata will be included.

---

# T02: Survey-Weighted Predictive Modelling

## 1. Task Overview

**Task ID:** T02

**Category:** Applied Machine Learning and Survey Statistics

**Difficulty:** Advanced

## 2. Real-World Problem

Conventional machine learning workflows may optimise predictive performance without considering complex survey design.

For population-relevant prediction, analysts must consider the target population, modelling objective, sampling weights, evaluation metrics, validation design, and uncertainty estimation.

Sampling weights are not automatically interchangeable with class weights or ordinary observation weights.

## 3. Evaluation Objectives

Evaluate whether an LLM can:

1. Identify the target population and prediction objective.
2. Distinguish sampling weights from class weights.
3. Recommend a defensible survey-aware modelling strategy.
4. Explain how weights may influence model fitting.
5. Select appropriate weighted or unweighted evaluation metrics.
6. Identify limitations of conventional ML workflows.
7. Distinguish prediction from population-level inference.
8. Identify software limitations.
9. Separate fitting weights, evaluation weights, and design-aware uncertainty.

## 4. Input Specification

Example task metadata:

```json
{
  "task_id": "T02_001",
  "problem_type": "binary_classification",
  "target_variable": "risk_status",
  "sampling_weight": "sample_weight",
  "strata_variable": "stratum_id",
  "psu_variable": "psu_id",
  "candidate_models": [
    "logistic_regression",
    "random_forest",
    "xgboost"
  ],
  "evaluation_goal": "population_relevant_prediction",
  "target_population": "Synthetic target population",
  "estimand": "Population-level predictive performance",
  "primary_metric": "weighted_auc"
}
```

The dataset will include a data dictionary, target definition, survey metadata, training and evaluation definitions, target population, and software constraints.

## 5. Expected Model Output

```json
{
  "target_population": "Description of the target population",
  "estimand": "Defined prediction or evaluation target",
  "modelling_strategy": "Recommended modelling strategy",
  "sampling_weight_handling": "Explanation of sampling-weight handling",
  "class_weight_handling": "Explanation of class-weight handling",
  "validation_strategy": "Recommended validation approach",
  "evaluation_metrics": [
    "weighted_auc",
    "weighted_log_loss"
  ],
  "uncertainty_method": "Recommended uncertainty assessment",
  "software_limitations": [],
  "limitations": []
}
```

## 6. Reference Solution

The reference should address:

- Whether the prediction target is population-oriented.
- Whether sampling weights should influence fitting.
- Whether software supports the required weighting procedure.
- Whether weighted metrics are appropriate.
- Whether design-aware uncertainty is required.
- Whether the objective is predictive or inferential.
- Whether validation reflects the intended deployment setting.

Three separate decisions must be evaluated:

1. Model fitting weights.
2. Evaluation weights.
3. Design-aware uncertainty using strata, PSUs, and other available design information.

Passing a weight variable to an estimator does not automatically account for stratification, clustering, or complex survey variance.

Weighted AUC and log-loss are appropriate only when aligned with the explicitly defined evaluation estimand.

## 7. Scoring and Grading Logic

**Total: 10 points**

| Component | Points |
|---|---:|
| Target population and objective | 2 |
| Sampling versus class weights | 2 |
| Model-fitting weight strategy | 2 |
| Validation and evaluation metrics | 2 |
| Uncertainty and methodological limitations | 2 |
| **Total** | **10** |

Use deterministic output checks, reference-based methodological scoring, code execution, and human review where necessary.

## 8. Common LLM Failure Modes

1. Treating sampling and class weights as equivalent.
2. Ignoring the target population.
3. Assuming every estimator supports weights correctly.
4. Using weighted training but unjustified unweighted evaluation.
5. Assuming ordinary cross-validation handles survey design.
6. Confusing prediction with inference.
7. Ignoring software limitations.
8. Assuming weighted fitting guarantees population-level validity.
9. Recommending weighted metrics without defining the estimand.
10. Confusing weighting with design-based variance estimation.

## 9. Reproducibility Requirements

Each instance must include versioned synthetic data, data dictionary, survey metadata, modelling objective, target population, estimand, model and software requirements, reference workflow, output schema, scoring rules, random seed, dependencies, and metric definitions.

Experiments must preserve model identifiers, prompt versions, execution settings, timestamps, raw outputs, trial-level scores, grader versions, and cost where available.

---

# T03: Data Leakage Detection and Prevention

## 1. Task Overview

**Task ID:** T03

**Category:** Machine Learning Reliability and Evaluation

**Difficulty:** Intermediate to Advanced

## 2. Real-World Problem

Data leakage occurs when information unavailable at the intended prediction time influences training or evaluation.

It can produce unrealistically high performance and misleading conclusions about generalization.

In survey-based predictive modelling, leakage may arise through target-derived variables, post-outcome information, duplicates, preprocessing before splitting, feature selection, repeated household or PSU observations, and temporal information unavailable at prediction time.

## 3. Evaluation Objectives

Evaluate whether an LLM can:

1. Identify direct target leakage.
2. Recognise indirect and proxy leakage.
3. Detect preprocessing leakage.
4. Identify temporal leakage.
5. Recognise duplicate and group-overlap risks.
6. Distinguish legitimate predictors from post-outcome information.
7. Recommend leakage-prevention procedures.
8. Explain the effect of leakage on reported performance.

## 4. Input Specification

Example:

```json
{
  "task_id": "T03_001",
  "prediction_target": "health_risk",
  "prediction_time": "baseline_interview",
  "features": [
    {
      "name": "age",
      "availability": "baseline"
    },
    {
      "name": "previous_health_status",
      "availability": "baseline"
    },
    {
      "name": "future_treatment",
      "availability": "after_prediction"
    },
    {
      "name": "risk_label_copy",
      "availability": "target_derived"
    }
  ],
  "preprocessing": {
    "imputation": "performed_before_split",
    "feature_selection": "performed_before_split"
  },
  "group_variable": "household_id",
  "split_strategy": "random_row_split"
}
```

The task will define feature availability and the proposed workflow. Some instances may deliberately omit information.

## 5. Expected Model Output

```json
{
  "leakage_detected": true,
  "leakage_features": [
    "future_treatment",
    "risk_label_copy"
  ],
  "leakage_types": [
    "temporal_leakage",
    "target_leakage",
    "preprocessing_leakage"
  ],
  "preprocessing_risks": [],
  "split_risks": [],
  "recommended_fixes": [],
  "performance_warning": "Explanation of possible optimistic performance"
}
```

## 6. Reference Solution

The reference solution should establish that:

- Variables unavailable at prediction time should not be used.
- Features directly derived from the target should be excluded.
- Learned preprocessing must be fitted on training data only.
- Duplicate observations and repeated household records must be examined.
- Group splitting may be required for unseen-household or unseen-cluster prediction.
- Temporal splitting may be required for future prediction.

The benchmark must distinguish actual leakage from a potential risk requiring more information.

A fixed transformation that does not learn from data is not necessarily equivalent to preprocessing leakage.

## 7. Scoring and Grading Logic

**Total: 10 points**

| Component | Points |
|---|---:|
| Target and temporal leakage identification | 2 |
| Preprocessing leakage detection | 2 |
| Duplicate and group-overlap recognition | 2 |
| Prevention recommendations | 2 |
| Performance explanation and valid JSON | 2 |
| **Total** | **10** |

Use deterministic schema checks, reference-based feature classification, executable pipeline checks, and human review where necessary.

## 8. Common LLM Failure Modes

1. Missing target-derived features.
2. Accepting post-outcome information as a predictor.
3. Preprocessing the complete dataset.
4. Ignoring duplicates.
5. Recommending random splitting when group separation is required.
6. Confusing correlation with leakage.
7. Treating every highly predictive feature as leakage.
8. Failing to explain performance distortion.

## 9. Reproducibility Requirements

Each instance must include task ID, versioned synthetic data, prediction-time definition, feature availability, split specification, reference leakage labels, output schema, grading rules, human-reviewed explanations, and random seed where applicable.

---

# T04: Validation Strategy Selection

## 1. Task Overview

**Task ID:** T04

**Category:** Machine Learning Evaluation and Statistical Methodology

**Difficulty:** Advanced

## 2. Real-World Problem

Predictive performance estimates depend heavily on the validation strategy.

Random splitting may be inappropriate when observations are clustered, repeated, temporally ordered, or drawn from multiple populations.

Survey-based predictive modelling must also consider household and PSU clustering, target population, temporal ordering, intended prediction setting, and independence assumptions.

## 3. Evaluation Objectives

Evaluate whether an LLM can:

1. Distinguish random, stratified, grouped, temporal, and external validation.
2. Identify dependent observations.
3. Recognise repeated measurements and household clustering.
4. Recommend validation for unseen groups or populations.
5. Identify temporal ordering requirements.
6. Distinguish internal from external validation.
7. Explain inappropriate validation limitations.
8. Justify its strategy using the prediction objective.

## 4. Input Specification

Example:

```json
{
  "task_id": "T04_001",
  "problem_type": "binary_classification",
  "target_variable": "risk_status",
  "sample_size": 6000,
  "data_structure": {
    "household_cluster": "household_id",
    "psu_variable": "psu_id",
    "time_variable": "survey_year",
    "population_variable": "region"
  },
  "prediction_goal": "predict_for_unseen_households",
  "validation_candidates": [
    "random_split",
    "stratified_split",
    "group_split",
    "temporal_split",
    "external_validation"
  ],
  "external_dataset_available": false
}
```

The task will specify whether the goal concerns new individuals, households, PSUs, future periods, geographical populations, or an independent dataset.

## 5. Expected Model Output

```json
{
  "recommended_strategy": "group_split",
  "alternative_strategy": "group_k_fold",
  "reasoning": "Explanation of the selected validation method",
  "independence_assumption": "Relevant independence assumptions",
  "leakage_risk": "Potential overlap between training and validation groups",
  "survey_design_considerations": [],
  "limitations": []
}
```

## 6. Reference Solution

Expected principles:

- Random splitting may be suitable for independent observations under the intended deployment setting.
- Stratification preserves approximate class proportions but does not automatically address clustering.
- Group-based splitting evaluates generalization to unseen groups.
- Temporal validation evaluates future prediction from past information.
- External validation evaluates performance on a genuinely independent population or dataset.
- Internal and external validation answer different questions.

No single validation strategy is universally superior.

The reference solution must define the intended generalization target.

Split strategy and design-aware performance uncertainty must be evaluated separately.

## 7. Scoring and Grading Logic

**Total: 10 points**

| Component | Points |
|---|---:|
| Prediction and generalization objective | 2 |
| Validation strategy selection | 3 |
| Clustering and dependence recognition | 2 |
| Limitations and leakage risks | 1 |
| Structured output and justification | 2 |
| **Total** | **10** |

Use deterministic output checks, reference-based strategy evaluation, rules for group and temporal requirements, and human review where necessary.

Multiple strategies may be accepted when they address the same stated generalization objective.

## 8. Common LLM Failure Modes

1. Recommending random splitting for clustered observations without justification.
2. Confusing stratification with group separation.
3. Ignoring household or PSU overlap.
4. Using future information in temporal tasks.
5. Treating internal validation as external validation.
6. Recommending external validation without an independent dataset.
7. Ignoring population changes.
8. Ignoring deployment objectives.

## 9. Reproducibility Requirements

Each instance must include dataset version, target variable, group identifiers, time and population variables, prediction objective, generalization target, output schema, reference answer, accepted alternatives, grading rules, and reproducible split assignments.

---

# T05: Class Imbalance and Performance Evaluation

## 1. Task Overview

**Task ID:** T05

**Category:** Classification Metrics and Applied Machine Learning

**Difficulty:** Intermediate to Advanced

## 2. Real-World Problem

Many real-world survey-based classification problems involve imbalanced outcomes.

For example, a relatively small proportion of respondents may belong to a high-risk category.

In such settings, accuracy alone can provide a misleading assessment of predictive performance.

LLMs must understand how class prevalence, decision thresholds, sampling weights, and the intended population affect metric selection and model evaluation.

## 3. Evaluation Objectives

Evaluate whether an LLM can:

1. Identify class imbalance.
2. Explain why accuracy may be misleading.
3. Select appropriate metrics for imbalanced classification.
4. Interpret precision, recall, specificity, F1-score, and ROC-AUC.
5. Explain the use and limitations of precision-recall AUC.
6. Distinguish class weights from sampling weights.
7. Explain threshold selection.
8. Recognise the impact of class prevalence on predictive values.
9. Evaluate performance using metrics aligned with the target population.

## 4. Input Specification

Example:

```json
{
  "task_id": "T05_001",
  "problem_type": "binary_classification",
  "sample_size": 5000,
  "positive_class_count": 250,
  "negative_class_count": 4750,
  "sampling_weight": "sample_weight",
  "target_variable": "risk_status",
  "evaluation_objective": "identify_high_risk_individuals",
  "error_priority": "minimise_false_negatives",
  "candidate_metrics": [
    "accuracy",
    "precision",
    "recall",
    "specificity",
    "f1_score",
    "roc_auc",
    "pr_auc"
  ]
}
```

The task will provide actual or synthetic confusion matrices, predicted probabilities, class labels, and sampling weights where applicable.

The benchmark will define the relative cost of false positives and false negatives when threshold decisions are required.

## 5. Expected Model Output

```json
{
  "imbalance_detected": true,
  "accuracy_limitation": "Explanation of accuracy limitations",
  "recommended_metrics": [
    "recall",
    "precision",
    "pr_auc"
  ],
  "threshold_strategy": "Recommended decision threshold approach",
  "class_weight_recommendation": "Explanation of class weighting",
  "sampling_weight_consideration": "Explanation of survey sampling weights",
  "metric_interpretation": "Interpretation of model performance",
  "limitations": []
}
```

## 6. Reference Solution

The reference solution should establish that:

- Accuracy alone may hide poor minority-class detection.
- Precision measures the proportion of predicted positives that are truly positive.
- Recall measures the proportion of actual positives detected.
- Specificity measures the proportion of actual negatives correctly identified.
- F1-score combines precision and recall through their harmonic mean.
- ROC-AUC measures ranking discrimination across thresholds.
- PR-AUC focuses on precision-recall behaviour and is often informative for rare positive classes.
- Threshold selection must reflect the decision objective and error costs.
- Class weights and survey sampling weights represent different concepts.

When the objective is population-relevant evaluation, the task must explicitly define whether metrics should be weighted.

Metric calculations must be independently verified using reference code.

## 7. Scoring and Grading Logic

**Total: 10 points**

| Component | Points |
|---|---:|
| Recognition of class imbalance | 1 |
| Appropriate metric selection | 2 |
| Correct metric interpretation | 2 |
| Threshold and error-cost reasoning | 2 |
| Distinction between class and sampling weights | 2 |
| Valid structured output | 1 |
| **Total** | **10** |

Use deterministic numerical checks for metric calculations and reference-based scoring for methodological explanations.

## 8. Common LLM Failure Modes

1. Reporting accuracy as the only important metric.
2. Ignoring minority-class recall.
3. Confusing precision and recall.
4. Selecting thresholds without considering error costs.
5. Confusing class weights with survey weights.
6. Interpreting ROC-AUC as calibration.
7. Comparing PR-AUC values without considering prevalence and evaluation conditions.
8. Reporting metrics without defining the positive class.

## 9. Reproducibility Requirements

Each instance must contain class counts, target definition, confusion matrix or predictions, metric definitions, weight information where relevant, reference calculations, scoring rules, and versioned inputs.

---

# T06: External Validation and Distribution Shift

## 1. Task Overview

**Task ID:** T06

**Category:** Model Generalization and Statistical Validation

**Difficulty:** Advanced

## 2. Real-World Problem

A predictive model may perform well on its development dataset but perform poorly when applied to a different population.

This can happen because of:

- Changes in population characteristics.
- Differences in predictor distributions.
- Changes in outcome prevalence.
- Changes in predictor-outcome relationships.
- Measurement differences.
- Survey-design differences.
- Temporal or geographical shifts.

LLMs must distinguish genuine external validation from repeated internal testing and understand how distribution shift affects model performance.

## 3. Evaluation Objectives

Evaluate whether an LLM can:

1. Distinguish internal from external validation.
2. Identify covariate shift, label shift, and concept drift.
3. Interpret changes in population composition.
4. Recognise differences in survey design across populations.
5. Evaluate discrimination and calibration under external validation.
6. Recommend appropriate transportability assessments.
7. Explain limitations of external performance comparisons.
8. Identify when recalibration or model updating may be necessary.

## 4. Input Specification

Example:

```json
{
  "task_id": "T06_001",
  "development_population": "Population_A",
  "external_population": "Population_B",
  "development_year": 2021,
  "external_year": 2025,
  "target_variable": "health_risk",
  "development_auc": 0.84,
  "external_auc": 0.73,
  "development_prevalence": 0.12,
  "external_prevalence": 0.21,
  "survey_design_available": true,
  "external_validation_objective": "assess_population_generalization"
}
```

The benchmark will provide dataset descriptions, outcome definitions, survey metadata, population characteristics, and relevant performance estimates.

The example values are illustrative; actual task instances will use documented synthetic or appropriately licensed data.

## 5. Expected Model Output

```json
{
  "external_validation_status": "genuine_external_validation",
  "observed_performance_change": "Explanation of performance difference",
  "possible_shift_types": [
    "covariate_shift",
    "label_shift"
  ],
  "population_comparability": "Assessment of population differences",
  "recommended_analysis": [
    "Compare predictor distributions",
    "Assess outcome prevalence",
    "Evaluate external calibration"
  ],
  "recalibration_recommendation": "Conditional recommendation",
  "limitations": []
}
```

## 6. Reference Solution

The reference solution should establish that:

- External validation requires an independent dataset or population relevant to the intended generalization objective.
- Covariate shift concerns changes in predictor distributions.
- Label shift concerns changes in outcome prevalence or class distribution.
- Concept drift concerns changes in the relationship between predictors and the outcome.
- Performance differences should be interpreted alongside differences in population, measurement, survey design, and outcome definitions.
- Recalibration may address some calibration changes but does not necessarily resolve changes in discrimination or underlying relationships.
- Model updating requires separate evaluation and documentation.

The benchmark must avoid assuming that every performance decline is caused by distribution shift alone.

## 7. Scoring and Grading Logic

**Total: 10 points**

| Component | Points |
|---|---:|
| Correct identification of external validation | 2 |
| Shift-type identification | 2 |
| Interpretation of performance differences | 2 |
| Appropriate transportability assessment | 2 |
| Recalibration reasoning and limitations | 2 |
| **Total** | **10** |

Use deterministic numerical checks, reference-based shift classification, and human review for complex explanations.

## 8. Common LLM Failure Modes

1. Calling internal test performance external validation.
2. Confusing covariate shift with concept drift.
3. Ignoring changes in outcome prevalence.
4. Attributing every performance decline to overfitting.
5. Ignoring different measurement definitions.
6. Assuming recalibration solves all forms of distribution shift.
7. Comparing external performance without considering population differences.
8. Ignoring differences in survey sampling design.

## 9. Reproducibility Requirements

Each instance must include development and external dataset versions, population definitions, survey metadata, outcome definitions, evaluation metrics, reference calculations, scoring rules, and documentation of any transformation or recalibration.

---

# T07: Missing Data and Statistical Uncertainty

## 1. Task Overview

**Task ID:** T07

**Category:** Statistical Reasoning and Data Quality

**Difficulty:** Advanced

## 2. Real-World Problem

Missing data is a major challenge in household and population surveys.

Ignoring missingness without examining its mechanism may introduce bias and reduce the reliability of statistical conclusions.

An LLM must understand missing data mechanisms, appropriate treatment strategies, uncertainty, and the implications of missingness for predictive modelling.

## 3. Evaluation Objectives

Evaluate whether an LLM can:

1. Distinguish MCAR, MAR, and MNAR.
2. Identify potential missingness patterns.
3. Explain limitations of complete-case analysis.
4. Recommend appropriate imputation strategies.
5. Distinguish single from multiple imputation.
6. Explain how missingness can affect model performance.
7. Recognise uncertainty introduced by imputation.
8. Consider survey weights and design during missing-data analysis.
9. Avoid claiming that missingness mechanisms can always be identified from observed data alone.

## 4. Input Specification

Example:

```json
{
  "task_id": "T07_001",
  "dataset": "synthetic_household_survey",
  "sample_size": 4000,
  "variables": {
    "age": {
      "missing_percentage": 2.0
    },
    "income": {
      "missing_percentage": 18.0
    },
    "health_status": {
      "missing_percentage": 7.0
    }
  },
  "sampling_weight": "sample_weight",
  "strata_variable": "stratum_id",
  "psu_variable": "psu_id",
  "analysis_objective": "predictive_modelling"
}
```

The task may include missingness indicators, known simulation mechanisms, missingness patterns, or incomplete documentation.

## 5. Expected Model Output

```json
{
  "missingness_assessment": "Assessment of available missingness evidence",
  "possible_mechanisms": [
    "MAR"
  ],
  "mechanism_confidence": "Explanation of uncertainty",
  "recommended_strategy": "Recommended missing-data approach",
  "complete_case_limitations": "Potential bias and information loss",
  "survey_design_considerations": "Weight and design implications",
  "uncertainty_method": "Recommended uncertainty assessment",
  "limitations": []
}
```

## 6. Reference Solution

Expected statistical concepts include:

- MCAR: Missingness is independent of observed and unobserved data under the stated mechanism.
- MAR: Missingness may depend on observed information but not on missing values after conditioning on the observed data.
- MNAR: Missingness depends on unobserved values or additional unobserved factors.
- Complete-case analysis may lose information and can introduce bias depending on the missingness mechanism and analysis assumptions.
- Multiple imputation can reflect imputation uncertainty when its assumptions and implementation are appropriate.
- Single imputation may underestimate uncertainty if imputation uncertainty is ignored.
- Missingness mechanisms generally cannot be established with certainty using observed data alone.
- Survey design and weights may need to be considered in imputation and subsequent analysis.

The reference solution must distinguish predictive imputation from inferential multiple imputation where relevant.

## 7. Scoring and Grading Logic

**Total: 10 points**

| Component | Points |
|---|---:|
| Correct MCAR, MAR, MNAR understanding | 2 |
| Missingness pattern interpretation | 2 |
| Appropriate treatment strategy | 2 |
| Uncertainty and imputation reasoning | 2 |
| Survey-design considerations and valid output | 2 |
| **Total** | **10** |

Use deterministic checks for supplied numerical missingness information, reference-based methodology checks, and human review for ambiguous missingness mechanisms.

## 8. Common LLM Failure Modes

1. Treating all missingness as MCAR.
2. Claiming MAR or MNAR can always be identified from observed data.
3. Recommending mean imputation universally.
4. Ignoring complete-case selection bias.
5. Treating single imputation as uncertainty-free.
6. Ignoring survey design.
7. Failing to distinguish prediction from inference.
8. Reporting imputed results without documenting assumptions.

## 9. Reproducibility Requirements

Each instance must include dataset version, missingness percentages and patterns, known simulation mechanism where applicable, survey metadata, imputation settings, random seed, reference solution, scoring rules, and software versions.

---

# T08: Model Calibration and Interpretability

## 1. Task Overview

**Task ID:** T08

**Category:** Explainable Machine Learning and Predictive Reliability

**Difficulty:** Advanced

## 2. Real-World Problem

A predictive model may discriminate between positive and negative cases but still produce poorly calibrated probabilities.

Similarly, feature-importance explanations may be misinterpreted as causal effects.

For population-oriented survey applications, an LLM must understand calibration, discrimination, threshold decisions, and the limitations of model explanations.

## 3. Evaluation Objectives

Evaluate whether an LLM can:

1. Distinguish discrimination from calibration.
2. Interpret calibration curves.
3. Explain Brier score and log-loss.
4. Identify calibration problems.
5. Recommend appropriate recalibration approaches.
6. Interpret feature importance and SHAP values.
7. Distinguish association-based explanations from causal inference.
8. Recognise limitations of global and local explanations.
9. Consider population differences when interpreting explanations.

## 4. Input Specification

Example:

```json
{
  "task_id": "T08_001",
  "model_name": "synthetic_risk_classifier",
  "target_variable": "health_risk",
  "roc_auc": 0.82,
  "brier_score": 0.19,
  "log_loss": 0.58,
  "calibration_method": "none",
  "top_features": [
    "age",
    "household_income",
    "previous_health_status"
  ],
  "explanation_method": "SHAP",
  "analysis_objective": "population_relevant_risk_prediction"
}
```

The benchmark may provide:

- Predicted probabilities.
- Observed outcomes.
- Calibration tables.
- Calibration curves.
- Feature-importance values.
- SHAP summaries.
- Model and population descriptions.

Numerical task instances must contain enough information to support the expected interpretation.

## 5. Expected Model Output

```json
{
  "discrimination_assessment": "Interpretation of ROC-AUC",
  "calibration_assessment": "Interpretation of predicted probabilities",
  "probability_reliability": "Assessment of probability reliability",
  "recommended_calibration": "Conditional calibration recommendation",
  "feature_interpretation": [
    {
      "feature": "age",
      "interpretation": "Explanation of feature contribution"
    }
  ],
  "causal_warning": "Explanation of why feature importance is not causal evidence",
  "limitations": []
}
```

## 6. Reference Solution

The reference solution should establish that:

- Discrimination measures how well a model ranks cases relative to non-cases.
- Calibration measures agreement between predicted probabilities and observed event frequencies.
- A high ROC-AUC does not guarantee good calibration.
- Brier score and log-loss evaluate probabilistic prediction quality, subject to their definitions and evaluation distributions.
- Calibration methods may include Platt scaling, isotonic regression, or other suitable approaches.
- Recalibration must be fitted using appropriate validation data without leakage.
- SHAP values describe model-output contributions relative to a defined explanation framework and background distribution.
- Feature importance does not establish causal effects.
- Explanations may change across populations, model specifications, and background datasets.

The benchmark must not assume one calibration method is optimal for every dataset.

## 7. Scoring and Grading Logic

**Total: 10 points**

| Component | Points |
|---|---:|
| Discrimination interpretation | 1 |
| Calibration interpretation | 2 |
| Correct metric understanding | 2 |
| Recalibration recommendation | 2 |
| SHAP and interpretability reasoning | 2 |
| Causal limitations and valid output | 1 |
| **Total** | **10** |

Use deterministic checks for numerical interpretations where reference values exist, reference-based explanation checks, and human review for complex interpretability claims.

## 8. Common LLM Failure Modes

1. Treating high ROC-AUC as proof of good calibration.
2. Confusing Brier score with discrimination.
3. Recommending calibration without independent validation.
4. Fitting a calibration method on the test dataset.
5. Interpreting SHAP values as causal effects.
6. Confusing feature importance with statistical significance.
7. Ignoring the background dataset used for SHAP.
8. Ignoring population changes in explanations.
9. Making unsupported claims from incomplete calibration information.

## 9. Reproducibility Requirements

Each instance must include model and dataset versions, predicted probabilities where applicable, observed outcomes, metric definitions, calibration settings, explanation method and configuration, random seeds, reference calculations, output schema, scoring rules, and software versions.

---

# 10. Cross-Task Methodological Quality Requirements

These requirements apply across all eight benchmark task families.

## 10.1 Explicit Estimand and Target Population

Every task must specify the target population and analytical objective.

The benchmark must distinguish:

- Population-level estimation.
- Population-relevant prediction.
- Sample-level prediction.
- Statistical inference.

Answers must be evaluated against the objective specified in the task.

## 10.2 Separate Weighting Decisions

The benchmark must evaluate separately:

1. Sampling weights during model fitting.
2. Sampling weights during predictive performance evaluation.
3. Strata and PSUs during design-aware uncertainty assessment.

Handling one component does not automatically address the others.

## 10.3 Context-Dependent Method Selection

Multiple statistically defensible approaches must be accepted when permitted by the task specification.

Reference solutions must document assumptions, software limitations, conditions of applicability, and reasons for rejecting alternatives.

## 10.4 Insufficient Information and Abstention

Some tasks may intentionally omit necessary design information.

Models should receive credit for identifying missing information, explaining why it matters, requesting clarification when appropriate, and avoiding unsupported recommendations.

## 10.5 Grader Reliability

Scoring must distinguish machine-verifiable requirements from methodological judgments.

Structured output, schema validity, and numerical calculations should be checked deterministically wherever possible.

Ambiguous explanations should use documented human-review rubrics.

Inter-rater agreement and disagreement resolution should be recorded for human-reviewed tasks.

## 10.6 Trial-Level Reproducibility

Each evaluation must preserve:

- Exact model identifier and version.
- Prompt and task version.
- Run date and execution settings.
- Random seed where applicable.
- Raw model response.
- Individual task score.
- Grader version.
- Execution time and cost where available.

## 10.7 Benchmark Fairness

The benchmark must use consistent task instructions, input formats, scoring rules, and evaluation conditions across compared models.

Model-specific configuration and tool access must be documented.

Tasks must not unintentionally reward proprietary interfaces or undocumented capabilities.

## 10.8 Human Review and Expert Validation

Reference answers and grading rubrics must be reviewed by an appropriate statistical or machine learning expert.

Ambiguous responses and disagreements must be documented.

The benchmark must preserve the distinction between automated grading and expert methodological assessment.

---

# 11. Overall Benchmark Scoring Framework

Each task family has an initial maximum score of 10 points.

| Task ID | Task Family | Maximum Points |
|---|---|---:|
| T01 | Complex Survey Design | 10 |
| T02 | Survey-Weighted Modelling | 10 |
| T03 | Data Leakage | 10 |
| T04 | Validation Strategy | 10 |
| T05 | Class Imbalance | 10 |
| T06 | External Validation | 10 |
| T07 | Missing Data | 10 |
| T08 | Calibration and Interpretability | 10 |
| **Total** | **Eight task families** | **80** |

The task-level scores may be aggregated for descriptive comparison, but the benchmark must also report task-level performance.

An overall score must not hide severe weaknesses in an individual methodological area.

Repeated trials should be analysed separately to assess consistency.

Pass@k and pass^k may be reported only when their success criteria and trial design are explicitly defined.

## 11.1 Grading Reliability

The benchmark will distinguish:

- Deterministic grading.
- Reference-based semantic grading.
- Code execution checks.
- Human expert review.

The grading system should document accepted alternatives and resolve ambiguous cases through predefined rubrics.

## 11.2 Performance Reporting

Model reports should include:

- Overall score.
- Task-level score.
- Criterion-level score.
- Trial-level performance.
- Failure categories.
- Output validity.
- Execution time.
- Cost where available.
- Uncertainty estimates where appropriate.

---

# 12. Current Task Design Status

| Task ID | Task Family | Design Status |
|---|---|---|
| T01 | Complex Survey Design and Weight Interpretation | Initial design drafted |
| T02 | Survey-Weighted Predictive Modelling | Initial design drafted |
| T03 | Data Leakage Detection and Prevention | Initial design drafted |
| T04 | Validation Strategy Selection | Initial design drafted |
| T05 | Class Imbalance and Performance Evaluation | Initial design drafted |
| T06 | External Validation and Distribution Shift | Initial design drafted |
| T07 | Missing Data and Statistical Uncertainty | Initial design drafted |
| T08 | Model Calibration and Interpretability | Initial design drafted |

## 13. Next Development Stage

The next implementation stage will include:

- Concrete benchmark task instances.
- Synthetic datasets.
- Human-reviewed reference answers.
- Executable grading scripts.
- Unit tests.
- Model evaluation protocols.
- Repeated-trial experiments.
- Grader reliability assessment.
- Documentation of model versions and execution settings.

The task specifications in this document are design proposals. Their empirical difficulty, reliability, and effectiveness must be assessed during implementation and experimentation.

---

**Document Status:** Initial design specifications for all eight benchmark task families. Reference answers, executable task instances, and empirical validation remain pending.