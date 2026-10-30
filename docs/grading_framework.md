mkdir -p docs
cat > docs/grading_framework.md <<'EOF'
# SurveyML-Eval: Grading Framework

**Document status:** Proposed grading specification
**Project:** SurveyML-Eval
**Benchmark:** Evaluating Large Language Models on Survey-Weighted Machine Learning Under Distribution Shift
**Version:** 1.0
**Scoring structure:** 8 task families × 10 points = 80 points

---

## 1. Purpose and Grading Philosophy

The grading framework defines a consistent, transparent, and reproducible method for evaluating model responses across the eight SurveyML-Eval task families.

The framework is designed to assess whether a model can correctly reason about:

- Complex survey design and sampling weights.
- Survey-weighted predictive modelling.
- Data leakage and prevention.
- Validation strategy selection.
- Class imbalance and performance evaluation.
- External validation and distribution shift.
- Missing data and statistical uncertainty.
- Model calibration and interpretability.

The benchmark evaluates both the correctness of the final answer and the methodological reasoning used to reach it.

### 1.1 Core grading principles

1. **Correctness:** Responses must be statistically and methodologically correct.
2. **Reproducibility:** The same response evaluated against the same grading specification should receive the same score.
3. **Transparency:** Every score must be traceable to explicit grading criteria.
4. **Partial credit:** Correct components should receive credit even when the complete answer is not correct.
5. **No unsupported assumptions:** Models should not receive credit for inventing data, assumptions, results, or methodological details.
6. **Methodological validity:** A numerically correct result obtained through an invalid procedure must not receive full credit.
7. **Human oversight:** Expert review must be available for ambiguous, borderline, and methodologically complex responses.
8. **Fairness:** Equivalent scientifically valid approaches should receive equivalent credit.

### 1.2 What the framework does not assume

- Fluent language automatically indicates correct reasoning.
- A longer response is necessarily better.
- A model's confidence indicates correctness.
- An LLM-based judge is automatically reliable.
- One specific statistical software package is mandatory unless a task explicitly requires it.
- A single numerical answer is sufficient when the task also requires methodological justification.

---

## 2. Overall Benchmark Scoring Structure

SurveyML-Eval contains eight task families.

Each task family contributes a maximum of 10 points.

| Task ID | Task Family | Maximum Points |
|---|---|---:|
| T01 | Complex Survey Design and Weight Interpretation | 10 |
| T02 | Survey-Weighted Predictive Modelling | 10 |
| T03 | Data Leakage Detection and Prevention | 10 |
| T04 | Validation Strategy Selection | 10 |
| T05 | Class Imbalance and Performance Evaluation | 10 |
| T06 | External Validation and Distribution Shift | 10 |
| T07 | Missing Data and Statistical Uncertainty | 10 |
| T08 | Model Calibration and Interpretability | 10 |
| **Total** | **Complete Benchmark** | **80** |

### 2.1 Overall score

For a single model response across all eight task families:

\[
S_{\text{total}} = \sum_{i=1}^{8} S_i
\]

where:

- \(S_i\) represents the score obtained in task family \(i\).
- \(0 \leq S_i \leq 10\).
- \(0 \leq S_{\text{total}} \leq 80\).

### 2.2 Normalised score

For comparison across benchmark reports:

\[
S_{\text{normalised}} =
\frac{S_{\text{total}}}{80}\times 100
\]

The normalised score is expressed as a percentage.

### 2.3 Interpretation of scores

The following categories are descriptive reporting bands, not universal measures of model capability.

| Normalised Score | Descriptive Category |
|---|---|
| 90–100 | Excellent benchmark performance |
| 80–89.99 | Strong benchmark performance |
| 70–79.99 | Good benchmark performance |
| 60–69.99 | Moderate benchmark performance |
| 40–59.99 | Limited benchmark performance |
| Below 40 | Weak benchmark performance |

These categories must not replace task-level scores, error analysis, or uncertainty estimates.

---

## 3. General Task-Level Scoring Rubric

Each task is evaluated using four dimensions.

| Dimension | Maximum Points |
|---|---:|
| Statistical or technical correctness | 4 |
| Methodological reasoning | 3 |
| Interpretation and justification | 2 |
| Completeness and clarity | 1 |
| **Total** | **10** |

### 3.1 Statistical or technical correctness — 4 points

Assesses whether the response provides correct concepts, calculations, statistical interpretations, code logic, or technical recommendations.

Scoring guidance:

- 4: Fully correct.
- 3: Mostly correct with a minor non-critical error.
- 2: Partially correct; one or more important components are missing or incorrect.
- 1: Limited correctness; only a small part is valid.
- 0: Incorrect, irrelevant, or unsupported.

### 3.2 Methodological reasoning — 3 points

Assesses whether the response selects and applies an appropriate statistical or machine learning method.

Scoring guidance:

- 3: Appropriate method with sound reasoning.
- 2: Generally appropriate method with a minor methodological weakness.
- 1: Partially appropriate method with a significant weakness.
- 0: Invalid method or no meaningful methodological reasoning.

### 3.3 Interpretation and justification — 2 points

Assesses whether the response correctly explains the implications of its answer.

Scoring guidance:

- 2: Correct interpretation with relevant justification.
- 1: Partially correct interpretation or insufficient justification.
- 0: Incorrect interpretation or no meaningful explanation.

### 3.4 Completeness and clarity — 1 point

Assesses whether the response addresses the requested components in an understandable manner.

Scoring guidance:

- 1: Addresses all required components clearly.
- 0.5: Understandable but incomplete.
- 0: Does not meaningfully address the requested output.

Half-point scoring may be used where the task rubric permits it.

---

## 4. Task-Specific Grading Rubrics

The general rubric provides a common structure. The following criteria define the task-specific evidence required for each task family.

### 4.1 T01 — Complex Survey Design and Weight Interpretation

**Maximum score: 10 points**

Evaluation objective:

Determine whether a model understands the implications of complex survey sampling, including sampling weights, strata, clusters, and population-level inference.

| Criterion | Points | Expected Evidence |
|---|---:|---|
| Identification of survey design components | 2 | Correct identification of weights, strata, and primary sampling units where applicable. |
| Interpretation of sampling weights | 2 | Correct explanation of the role of weights and their relationship to the target population. |
| Recognition of design effects | 2 | Understanding of clustering, stratification, and their implications for variance estimation. |
| Selection of appropriate analytical approach | 2 | Appropriate use of survey-aware estimation or inference methods. |
| Interpretation and limitations | 2 | Correct interpretation of estimates and relevant limitations. |
| **Total** | **10** | |

**Critical error examples:**

- Treating survey weights as ordinary frequency counts without justification.
- Ignoring clustering or stratification when these are relevant to the task.
- Claiming that an unweighted estimate necessarily represents the target population.
- Confusing sample size with effective sample size.

A critical error should be recorded separately. Its scoring consequence must follow the applicable criterion rather than an automatic blanket penalty.

### 4.2 T02 — Survey-Weighted Predictive Modelling

**Maximum score: 10 points**

Evaluation objective:

Assess whether a model can develop or recommend a predictive modelling approach that appropriately considers survey design and sampling weights.

| Criterion | Points | Expected Evidence |
|---|---:|---|
| Problem formulation | 2 | Correct identification of the prediction target, outcome, and analytical objective. |
| Weight-aware modelling strategy | 3 | Appropriate discussion or implementation of weights in model training or estimation. |
| Model selection and workflow | 2 | Suitable model choice and logically structured modelling workflow. |
| Performance evaluation | 2 | Appropriate evaluation strategy that considers the intended population and analytical objective. |
| Limitations and assumptions | 1 | Recognition of modelling and survey-design limitations. |
| **Total** | **10** | |

**Critical error examples:**

- Ignoring the survey design when it materially affects the modelling objective.
- Claiming that every machine learning algorithm automatically supports survey weights.
- Using an unsupported weighting implementation and presenting it as valid.
- Confusing predictive performance with design-based population inference.

A model must distinguish between weighted training, weighted evaluation, and population-level inference. These are related but not interchangeable.

### 4.3 T03 — Data Leakage Detection and Prevention

**Maximum score: 10 points**

Evaluation objective:

Determine whether a model can identify leakage risks and propose a valid leakage-safe modelling workflow.

| Criterion | Points | Expected Evidence |
|---|---:|---|
| Leakage identification | 3 | Correct detection of target leakage, preprocessing leakage, temporal leakage, or related risks relevant to the task. |
| Explanation of leakage mechanism | 2 | Correct explanation of how information enters the training process improperly. |
| Prevention strategy | 2 | Appropriate train/test separation and pipeline-based preprocessing or other safeguards. |
| Validation integrity | 2 | Correct protection of validation and test data from model development decisions. |
| Practical implementation clarity | 1 | Clear and actionable prevention procedure. |
| **Total** | **10** | |

**Critical error examples:**

- Fitting preprocessing transformations on the complete dataset before splitting.
- Allowing target information to enter predictors.
- Using future information to predict past outcomes.
- Selecting a model using the final test set and reporting the same test performance as unbiased evaluation.

### 4.4 T04 — Validation Strategy Selection

**Maximum score: 10 points**

Evaluation objective:

Assess whether a model can select a validation design that reflects the data structure, prediction target, and intended deployment setting.

| Criterion | Points | Expected Evidence |
|---|---:|---|
| Understanding of data structure | 2 | Recognition of independent, clustered, grouped, temporal, or hierarchical observations as applicable. |
| Validation strategy selection | 3 | Appropriate selection of random, stratified, grouped, temporal, nested, or other validation strategies. |
| Leakage prevention | 2 | Recognition of dependence and information leakage risks in the chosen design. |
| Justification | 2 | Explanation of why the validation strategy matches the intended generalisation target. |
| Limitations | 1 | Recognition of uncertainty and limitations of the validation design. |
| **Total** | **10** | |

**Critical error examples:**

- Random splitting when the task requires future-period prediction and temporal leakage would result.
- Splitting repeated observations from the same individual across training and test sets when this violates the evaluation target.
- Using the same data for model selection and final unbiased performance reporting without appropriate safeguards.

### 4.5 T05 — Class Imbalance and Performance Evaluation

**Maximum score: 10 points**

Evaluation objective:

Evaluate whether a model can select appropriate methods and metrics for imbalanced classification problems.

| Criterion | Points | Expected Evidence |
|---|---:|---|
| Imbalance diagnosis | 2 | Correct recognition of class proportions and their implications. |
| Metric selection | 3 | Appropriate use and explanation of metrics such as precision, recall, F1-score, balanced accuracy, ROC-AUC, or PR-AUC. |
| Resampling or weighting strategy | 2 | Appropriate discussion of class weighting, resampling, or other justified approaches. |
| Threshold and decision analysis | 2 | Recognition that classification thresholds depend on the decision context and error costs. |
| Interpretation | 1 | Correct communication of limitations and performance implications. |
| **Total** | **10** | |

**Critical error examples:**

- Using accuracy alone to claim strong performance in a severely imbalanced problem.
- Applying oversampling or undersampling before splitting data in a way that contaminates evaluation.
- Treating ROC-AUC, PR-AUC, precision, and recall as interchangeable.
- Ignoring the operational costs of false positives and false negatives when these are specified.

### 4.6 T06 — External Validation and Distribution Shift

**Maximum score: 10 points**

Evaluation objective:

Determine whether a model can evaluate performance on an external population or dataset and identify relevant forms of distribution shift.

| Criterion | Points | Expected Evidence |
|---|---:|---|
| External validation design | 2 | Correct definition of the external validation population and evaluation procedure. |
| Shift identification | 2 | Recognition of covariate shift, label shift, concept drift, or other relevant changes. |
| Performance comparison | 2 | Appropriate comparison of internal and external performance. |
| Statistical interpretation | 2 | Correct interpretation of performance differences and uncertainty. |
| Generalisation and limitations | 2 | Appropriate discussion of transportability, applicability, and limitations. |
| **Total** | **10** | |

**Critical error examples:**

- Calling a random holdout from the same source an external validation dataset without justification.
- Treating a performance decline as proof of one specific type of distribution shift without evidence.
- Ignoring differences in outcome definitions, measurement, or population composition.
- Claiming generalisation to populations that were not evaluated.

### 4.7 T07 — Missing Data and Statistical Uncertainty

**Maximum score: 10 points**

Evaluation objective:

Assess whether a model can identify missing-data mechanisms, choose appropriate handling strategies, and communicate uncertainty.

| Criterion | Points | Expected Evidence |
|---|---:|---|
| Missingness diagnosis | 2 | Appropriate understanding of MCAR, MAR, and MNAR where relevant. |
| Handling strategy | 3 | Justified use of complete-case analysis, imputation, or other suitable approaches. |
| Uncertainty estimation | 2 | Appropriate consideration of standard errors, confidence intervals, bootstrap methods, or multiple-imputation uncertainty. |
| Validation integrity | 2 | Leakage-safe handling of missing values within the validation workflow. |
| Interpretation and limitations | 1 | Clear explanation of assumptions and limitations. |
| **Total** | **10** | |

**Critical error examples:**

- Assuming missingness is MCAR without evidence or justification.
- Treating imputed values as observed values without acknowledging uncertainty.
- Performing imputation using information from held-out evaluation data in a leakage-prone workflow.
- Reporting confidence intervals without a defensible uncertainty-estimation procedure.

### 4.8 T08 — Model Calibration and Interpretability

**Maximum score: 10 points**

Evaluation objective:

Evaluate whether a model can distinguish discrimination from calibration and provide valid, appropriately qualified interpretations of model behaviour.

| Criterion | Points | Expected Evidence |
|---|---:|---|
| Calibration understanding | 2 | Correct distinction between discrimination and calibration. |
| Calibration assessment | 2 | Appropriate selection or interpretation of calibration curves, Brier score, calibration intercept, slope, or other suitable methods. |
| Calibration improvement | 2 | Appropriate discussion of recalibration methods where required. |
| Interpretability method | 2 | Appropriate selection and interpretation of SHAP, permutation importance, or other relevant methods. |
| Limitations and responsible interpretation | 2 | Recognition of uncertainty, feature dependence, and limitations of explanations. |
| **Total** | **10** | |

**Critical error examples:**

- Treating a high ROC-AUC as evidence of good probability calibration.
- Claiming that feature importance proves causality.
- Interpreting SHAP values as causal effects without an appropriate causal design.
- Evaluating calibration on training data and presenting it as independent validation.

---

## 5. Scoring Rules and Partial Credit

### 5.1 Criterion-level scoring

Each task must be scored at the criterion level rather than assigned a score based only on an overall impression.

For each criterion, the grader must record:

- Maximum available points.
- Points awarded.
- Evidence from the model response.
- Reason for any deduction.
- Whether expert review is required.

### 5.2 Partial credit

Partial credit is awarded when a response contains a valid component but does not fully satisfy the criterion.

Examples:

- Correctly identifying survey weights but failing to discuss clustering may receive partial credit in T01.
- Correctly identifying target leakage but suggesting an incomplete prevention strategy may receive partial credit in T03.
- Correctly identifying class imbalance but relying only on accuracy may receive partial credit in T05.
- Correctly identifying external performance degradation but incorrectly attributing its cause may receive partial credit in T06.

### 5.3 Unsupported claims

A claim must not receive credit merely because it sounds technically plausible.

Unsupported claims include:

- Invented numerical results.
- Unreported model performance.
- Fabricated dataset properties.
- Unjustified causal conclusions.
- Incorrect references to statistical procedures.
- Claims that a software package supports a feature without evidence when the task requires implementation-specific accuracy.

### 5.4 Alternative valid answers

The reference answer is a grading anchor, not necessarily the only acceptable answer.

An alternative answer may receive full credit if it:

1. Is statistically or technically valid.
2. Addresses the task objective.
3. Satisfies the stated constraints.
4. Uses defensible assumptions.
5. Does not introduce unsupported claims.

The reason for accepting a materially different answer should be documented.

### 5.5 No double penalty

A single underlying error should not automatically cause repeated deductions across unrelated criteria.

However, separate consequences may be scored independently when the error genuinely affects multiple distinct requirements.

For example, leakage may affect both leakage identification and validation integrity if the task explicitly assesses both.

---

## 6. Critical Errors and Failure Classification

Critical errors are serious failures that can invalidate a methodological conclusion or materially mislead the user of the analysis.

They must be explicitly recorded even when partial credit is awarded.

### 6.1 Critical error categories

| Error Code | Category | Description |
|---|---|---|
| CE01 | Survey design failure | Incorrect treatment or interpretation of a relevant survey-design component. |
| CE02 | Weighting failure | Incorrect or unjustified use of sampling weights. |
| CE03 | Data leakage | Use of information that would not legitimately be available at prediction time. |
| CE04 | Validation failure | Invalid evaluation split or contaminated test data. |
| CE05 | Metric misuse | Inappropriate metric selection or interpretation. |
| CE06 | External validation failure | Unsupported external generalisation or invalid population comparison. |
| CE07 | Missing-data failure | Invalid missing-data assumption or handling procedure. |
| CE08 | Uncertainty failure | Misleading or unsupported uncertainty estimates. |
| CE09 | Calibration failure | Incorrect calibration interpretation or evaluation. |
| CE10 | Interpretability overclaim | Unsupported causal or explanatory claim. |
| CE11 | Fabrication | Invented numerical results, data properties, or experimental evidence. |
| CE12 | Reproducibility failure | Missing or incorrect information that prevents the requested procedure from being reproduced. |

### 6.2 Severity classification

| Severity | Meaning |
|---|---|
| Critical | Invalidates a major conclusion or creates a serious methodological error. |
| Major | Materially weakens the answer but does not necessarily invalidate the complete task. |
| Minor | Limited issue that does not materially change the conclusion. |

### 6.3 Penalty policy

Critical-error flags must be reported separately from the numerical score.

A score deduction must occur through the relevant criterion unless a task-specific rule explicitly defines an additional penalty.

This avoids arbitrary double penalties and preserves score interpretability.

No universal automatic zero-score rule is applied to every critical error. The severity and scoring consequence must be specified in the task rubric.

---

## 7. Grader Architecture

The grading process separates objective evaluation from expert judgment.

### 7.1 Grading layers

**Layer 1 — Machine-checkable grading**

Used for criteria with objectively verifiable outcomes, such as:

- Exact numerical answers with defined tolerances.
- Required output structure.
- Valid JSON or CSV format.
- Presence of required fields.
- Reproducible code execution.
- Expected values from deterministic calculations.
- Explicitly defined pass/fail conditions.

**Layer 2 — Rule-based methodological grading**

Used for criteria that can be checked against predefined rules, such as:

- Correct identification of leakage.
- Selection of an appropriate validation strategy.
- Recognition of survey-design components.
- Correct interpretation of a specified statistical metric.

**Layer 3 — Human expert grading**

Used when evaluation requires methodological interpretation, such as:

- Assessing the quality of statistical justification.
- Evaluating whether assumptions are defensible.
- Reviewing alternative valid approaches.
- Determining whether an explanation overstates its evidence.

### 7.2 LLM-assisted judging

An LLM-based judge may be used as an auxiliary evaluation instrument.

It must not be treated as ground truth.

If used, the evaluation record must identify:

- Judge model and exact version.
- Prompt or grading instructions.
- Date of evaluation.
- Input response.
- Criterion-level scores.
- Human verification procedure.
- Disagreement resolution process.

LLM-judge scores must be compared with human judgments on an appropriate subset before they are used for large-scale grading.

---

## 8. Human Review and Inter-Rater Reliability

Human expert review is important for criteria that cannot be evaluated reliably through deterministic checks.

### 8.1 Independent review

Where feasible:

1. At least two reviewers independently assess selected responses.
2. Reviewers use the same written rubric.
3. Reviewers record criterion-level scores.
4. Reviewers provide evidence for deductions.
5. Disagreements are identified before final adjudication.

### 8.2 Inter-rater reliability

The agreement between reviewers should be quantified using a statistic appropriate to the scoring design.

Potential measures include:

- Cohen's kappa for suitable categorical judgments with two raters.
- Weighted kappa for suitable ordinal ratings.
- Intraclass correlation coefficient for numerical ratings where its assumptions and design are appropriate.
- Percentage agreement as a descriptive supplementary measure.

The chosen statistic, assumptions, and calculation method must be documented.

### 8.3 Adjudication

When reviewers disagree:

1. Identify the disputed criterion.
2. Compare the response with the task-specific rubric.
3. Record the reason for disagreement.
4. Refer unresolved cases to an adjudicator.
5. Preserve original reviewer scores.
6. Store the final adjudicated score separately.

Adjudication must not silently overwrite the original assessments.

### 8.4 Reviewer documentation

The grading record should include:

- Reviewer identifier or anonymised reviewer code.
- Task ID and instance ID.
- Model response identifier.
- Criterion-level scores.
- Critical-error flags.
- Reviewer comments.
- Adjudication status.
- Final score.

---

## 9. Reference Answers and Grading Evidence

Each task instance should have a reference package.

### 9.1 Reference package components

Where applicable, a reference package should contain:

1. Task statement.
2. Input data or a description of the input.
3. Expected output or reference solution.
4. Accepted alternative approaches.
5. Criterion-level rubric.
6. Expected numerical values and tolerances.
7. Critical-error examples.
8. Assumptions and constraints.
9. Execution or validation instructions.

### 9.2 Reference answer principles

A reference answer should:

- Be technically valid.
- Address the task requirements.
- State necessary assumptions.
- Distinguish facts from interpretations.
- Avoid unsupported numerical claims.
- Include reproducible calculations or code when relevant.
- Allow scientifically defensible alternatives.

### 9.3 Evidence-based grading

Every awarded or deducted point should be supported by evidence from the model response or an execution result.

The grader should avoid statements such as:

- "The answer looks good."
- "The explanation is convincing."
- "The model seems knowledgeable."

Instead, grading comments should identify the specific requirement satisfied or missed.

---

## 10. Score Aggregation and Repeated Trials

The benchmark may contain multiple task instances within each task family and repeated model runs.

These levels must remain distinct.

### 10.1 Task-instance score

For task instance \(j\), task family \(i\), and model \(m\):

\[
S_{mij} \in [0,10]
\]

### 10.2 Mean task-family score

If task family \(i\) contains \(J_i\) evaluated instances:

\[
\bar{S}_{mi} =
\frac{1}{J_i}
\sum_{j=1}^{J_i} S_{mij}
\]

### 10.3 Mean benchmark score

For eight task families with equal task-family weighting:

\[
\bar{S}_{m} =
\sum_{i=1}^{8}\bar{S}_{mi}
\]

The maximum possible mean benchmark score remains 80.

### 10.4 Repeated-run aggregation

For a model evaluated over \(R\) repeated runs, report the mean and variability of the relevant scores.

\[
\bar{S}_{m} =
\frac{1}{R}\sum_{r=1}^{R}S_{mr}
\]

The exact aggregation unit must be stated.

Task-instance variability and repeated-run variability must not be treated as the same source of uncertainty.

### 10.5 Missing or invalid responses

A missing, truncated, or invalid response must be handled according to a predefined execution policy.

The record must distinguish:

- Model-generated incorrect response.
- Model refusal.
- API or infrastructure failure.
- Timeout.
- Invalid output format.
- Incomplete response.

Infrastructure failures should not automatically be interpreted as model reasoning failures.

Any exclusion, retry, or replacement rule must be applied consistently and reported.

---

## 11. Grader Reliability and Quality Assurance

The grading system must be evaluated before benchmark results are treated as reliable.

### 11.1 Quality assurance checks

- Verify that all eight task families have explicit rubrics.
- Confirm that every criterion has a defined maximum score.
- Check that task-level totals equal 10 points.
- Check that the benchmark total equals 80 points.
- Validate scoring scripts against known test cases.
- Check numerical tolerances.
- Review ambiguous rubric language.
- Verify that accepted alternatives are documented.
- Compare automated and human scores on a selected subset.
- Record grader disagreements and adjudications.

### 11.2 Grading audit

A grading audit should preserve:

- Original model response.
- Task and instance identifiers.
- Rubric version.
- Grader version.
- Raw criterion-level scores.
- Critical-error annotations.
- Human-review records.
- Final adjudicated score.
- Timestamp of grading.

### 11.3 Rubric changes

Any change to a rubric after evaluation begins must be version-controlled.

If a material rubric change affects comparability, the affected responses should be re-evaluated using the same rubric version.

Results produced under different rubric versions must be clearly distinguished.

---

## 12. Required Grading Output Format

Each evaluated response should produce a structured grading record.

The following JSON illustrates the intended structure. Values are illustrative placeholders, not benchmark results.

```json
{
  "benchmark": "SurveyML-Eval",
  "rubric_version": "1.0",
  "model_id": "MODEL_ID_PLACEHOLDER",
  "task_id": "T01",
  "task_instance_id": "T01_INSTANCE_001",
  "trial_id": "TRIAL_001",
  "criteria": [
    {
      "criterion": "Identification of survey design components",
      "max_points": 2,
      "awarded_points": 2,
      "evidence": "Response correctly identifies the supplied design components.",
      "review_required": false
    },
    {
      "criterion": "Interpretation of sampling weights",
      "max_points": 2,
      "awarded_points": 1,
      "evidence": "Response explains weights but misses an important qualification.",
      "review_required": true
    }
  ],
  "task_score": 3,
  "task_max_score": 10,
  "critical_errors": [],
  "grading_method": "machine_assisted_with_human_review",
  "review_status": "pending",
  "final_adjudicated_score": null
}
```

## 13. Reporting Requirements

Every benchmark report must include:

1. Exact model identifier and version.
2. Evaluation date and configuration.
3. Scores for all eight task families.
4. Overall and normalised scores.
5. Number of task instances and repeated trials.
6. Criterion-level performance where available.
7. Critical-error frequency and failure categories.
8. Grading method and human-review procedure.
9. Missing, invalid, and excluded responses.
10. Relevant uncertainty estimates.

### 13.1 Overall performance table

| Model | T01 | T02 | T03 | T04 | T05 | T06 | T07 | T08 | Total / 80 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Model A | — | — | — | — | — | — | — | — | — |
| Model B | — | — | — | — | — | — | — | — | — |

No results should be populated until actual experiments and grading have been completed.

---

## 14. Limitations of the Grading Framework

1. Some statistical reasoning tasks may permit multiple valid approaches.
2. Expert judgments may vary even when reviewers use the same rubric.
3. Automated grading may fail to recognise a valid alternative explanation.
4. Numerical tolerances may need task-specific calibration.
5. A benchmark score cannot represent every aspect of real-world ML engineering ability.
6. Performance on this benchmark does not guarantee reliable performance on unseen datasets.
7. Equal task-family weighting is a design choice.
8. Changes in models, APIs, and prompting behaviour may affect comparability over time.

These limitations must be considered when interpreting benchmark results.

---

## 15. Alignment with Research and Hackathon Evaluation

| Evaluation Requirement | Grading Framework Contribution |
|---|---|
| Real-world relevance | Evaluates applied survey and predictive modelling decisions. |
| Task design | Provides eight task-specific scoring rubrics. |
| Grader reliability | Separates automated checks, rule-based grading, and human review. |
| Evidence of model limitations | Records critical errors and failure categories. |
| Reproducibility | Defines versioned rubrics and structured grading records. |
| Human expertise | Includes independent review and adjudication. |
| Research insight | Enables analysis of task-level strengths and weaknesses. |

---

## 16. Implementation Roadmap

The following activities remain necessary:

1. Convert task-specific rubrics into machine-readable configuration files.
2. Develop deterministic grading scripts.
3. Create reference-answer packages for each task instance.
4. Implement criterion-level score aggregation.
5. Create critical-error annotation support.
6. Develop structured grading output validation.
7. Establish human-review and adjudication workflows.
8. Test automated grading against manually verified examples.
9. Measure grader reliability.
10. Freeze and version the grading specification before the main evaluation.

These activities must not be represented as completed until verified.

---

## 17. Document Status

This document specifies the proposed grading framework for SurveyML-Eval.

The eight task families, task-level point allocations, criterion-level rubrics, critical-error categories, grader architecture, human-review procedures, and reporting requirements are defined as the intended evaluation specification.

The framework has not yet been empirically validated.

Actual grader reliability, automated-human agreement, and scoring performance must be established through implementation and testing.

No model performance results or experimental findings are claimed in this document.
