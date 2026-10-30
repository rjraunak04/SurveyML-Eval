# SurveyML-Eval: Evaluation Protocol

## 1. Evaluation Objectives

### 1.1 Primary Objective

The primary objective is to evaluate the reliability and methodological correctness of Large Language Models (LLMs) when solving statistical reasoning and survey-aware predictive machine learning tasks.

The evaluation will examine whether models can:

- Interpret complex survey designs.
- Handle survey weights appropriately.
- Recommend defensible predictive modelling workflows.
- Detect data leakage.
- Select appropriate validation strategies.
- Evaluate imbalanced classification.
- Assess external generalization.
- Reason about missing data and uncertainty.
- Interpret calibration and explainable ML outputs.

### 1.2 Secondary Objectives

The evaluation will also examine:

1. Consistency across repeated trials.
2. Differences across benchmark task families.
3. Structured output validity.
4. Numerical correctness.
5. Methodological failure patterns.
6. Execution time and cost.
7. Sensitivity to prompt and configuration changes, where tested.

### 1.3 Evaluation Scope

The initial benchmark contains eight task families, each with a maximum task score of 10 points.

The aggregate maximum score across all eight task families is 80 points.

Actual evaluation will require multiple task instances within each task family. A task-family score must not be treated as a single independent experimental observation when analysing uncertainty.

---

## 2. Experimental Design

### 2.1 Evaluation Unit

The primary experimental record is one model execution on one versioned benchmark task instance.

Each execution must have a unique trial identifier.

The experiment will preserve the relationship between:

- Model.
- Task family.
- Task instance.
- Prompt version.
- Trial.
- Grader version.
- Execution configuration.

### 2.2 Benchmark Structure

The evaluation hierarchy is:

```text
Benchmark
   |
   +-- Task Family
          |
          +-- Task Instance
                 |
                 +-- Model
                        |
                        +-- Trial 1
                        +-- Trial 2
                        +-- Trial 3
                        +-- Additional Trials
```

### 2.3 Controlled Comparison

Models should receive equivalent task inputs, instructions, output schemas, and grading criteria.

Any unavoidable differences in API settings, model capabilities, or tool access must be recorded.

Model comparisons must not silently mix different evaluation conditions.

### 2.4 Pilot Evaluation

A pilot experiment should be conducted before the main evaluation.

The pilot should examine:

- Task clarity.
- Input validity.
- Output schema reliability.
- Grader correctness.
- Scoring ambiguity.
- Execution failures.
- Approximate runtime and cost.
- Trial-to-trial variability.

Pilot tasks or results should be clearly labelled.

If pilot runs are excluded from the final analysis, the exclusion must be documented.

---

## 3. Model Selection and Identification

### 3.1 Selection Criteria

Models may be selected according to:

- Relevance to statistical reasoning.
- Availability of documented model identifiers.
- Reproducible access.
- Practical execution cost.
- Supported generation settings.
- Availability of raw responses.
- Suitability for the benchmark tasks.

### 3.2 Model Categories

The benchmark may include:

- General-purpose instruction-following models.
- Reasoning-oriented models.
- Open-weight language models.
- Tool-enabled models, where relevant.

Model categories should be reported separately when capabilities or execution conditions are materially different.

### 3.3 Model Metadata

For every evaluated model, record:

| Field | Description |
|---|---|
| provider | Model provider |
| model_id | Exact model identifier |
| model_version | Version or snapshot |
| access_method | API, local inference, or supported interface |
| evaluation_date | Date of execution |
| temperature | Configured temperature, if supported |
| top_p | Configured sampling parameter, if supported |
| max_tokens | Configured output limit |
| reasoning_setting | Documented reasoning configuration, if available |
| tool_access | Enabled tools |
| api_version | API version, where relevant |

Unavailable or unsupported settings must be recorded as unavailable rather than invented.

### 3.4 Version Stability

A model name may refer to changing underlying versions.

The evaluation must use the most precise model identifier exposed by the provider.

If an exact snapshot cannot be obtained, the evaluation record must state that limitation.

---

## 4. Prompt Standardisation

### 4.1 Prompt Design

All benchmark tasks should follow a consistent prompt structure.

The prompt should contain:

1. Task identifier.
2. Problem statement.
3. Dataset or scenario.
4. Variable definitions.
5. Analytical objective.
6. Relevant survey-design metadata.
7. Required output format.
8. Explicit constraints.

### 4.2 Prompt Versioning

Each prompt must have a version identifier.

For example:

```text
prompt_version: v1.0
```

Any modification to instructions, task wording, examples, or output requirements must result in a documented version change.

### 4.3 Prompt Fairness

Prompts must not provide one model with additional methodological hints unless the experiment explicitly tests different prompting strategies.

The default comparison should use the same prompt content across models.

### 4.4 Structured Output Instructions

Tasks requiring JSON must specify:

- Required keys.
- Expected value types.
- Allowed categorical values.
- Null handling.
- Whether additional keys are permitted.
- Numerical precision requirements, where applicable.

The evaluator should distinguish invalid JSON from incorrect statistical reasoning.

### 4.5 Prompt Sensitivity

Prompt sensitivity may be investigated as a supplementary experiment.

Such experiments should use separately versioned prompts and should not be mixed with the primary standardised evaluation.

---

## 5. Trial Configuration and Execution

### 5.1 Initial Trial Plan

The initial experimental plan proposes three to five repeated trials for each task-instance/model combination.

This is a starting point, not a guarantee of adequate statistical precision.

The final number of trials should be informed by:

- Pilot variability.
- API cost.
- Model availability.
- Execution constraints.
- Required precision of performance estimates.

### 5.2 Trial Identification

Each execution should receive a unique identifier.

Example:

```text
experiment_id: EXP_001
task_id: T01_001
model_id: provider_model_version
prompt_version: v1.0
trial_id: TRIAL_001
```

### 5.3 Generation Settings

The evaluation should record:

- Temperature, where supported.
- Top-p, where supported.
- Maximum output tokens.
- Seed, where supported.
- Reasoning configuration, where exposed.
- Tool access.
- Timeout settings.

If a provider does not expose a setting, it must not be assumed to have a particular value.

### 5.4 Randomness and Repeated Runs

Repeated calls may produce different responses because of sampling, model-side variation, or changing provider infrastructure.

A fixed random seed does not necessarily guarantee identical outputs across all providers.

The benchmark should document the extent to which execution is reproducible.

### 5.5 Execution Failure Handling

The following statuses should be distinguished:

| Status | Meaning |
|---|---|
| success | Valid model execution completed |
| invalid_output | Response failed required output validation |
| timeout | Execution exceeded the time limit |
| api_error | Provider or API error |
| refusal | Model declined the request |
| incomplete | Response was truncated or incomplete |
| grader_error | Evaluation system failed |

An API failure is not automatically a model reasoning failure.

Invalid model output should be scored according to predefined benchmark rules.

Retries must be logged and must not silently replace the original failed execution.

---

## 6. Evaluation Metrics

### 6.1 Task-Level Score

Each task instance is scored using its predefined grading rubric.

For task instance \(i\), let:

\[
S_i\in[0,10]
\]

where 10 represents the maximum score.

### 6.2 Task-Family Score

For task family \(j\), with \(N_j\) evaluated instances:

\[
\bar S_j=
\frac{1}{N_j}
\sum_{i=1}^{N_j}S_{ij}
\]

Task-family results should be reported separately.

### 6.3 Overall Score

The initial benchmark contains eight task families with a maximum score of 10 points each.

The aggregate score is:

\[
S_{\text{total}}=
\sum_{j=1}^{8}S_j
\]

The maximum aggregate score is 80 points.

For multi-instance experiments, the reporting procedure must specify how task instances and task-family scores are aggregated.

An equal-weighted task-family average may be reported as a macro-average:

\[
S_{\text{macro}}=
\frac{1}{8}
\sum_{j=1}^{8}\bar S_j
\]

The macro-average gives equal importance to each task family regardless of the number of instances in that family.

### 6.4 Output Validity

Report:

- Valid JSON percentage.
- Required-key completion.
- Type validity.
- Missing-field frequency.
- Invalid numerical outputs.
- Unparseable response frequency.

Output validity must remain distinct from methodological correctness.

### 6.5 Numerical Correctness

For tasks containing reference numerical results, evaluate:

- Exact agreement where appropriate.
- Absolute error.
- Relative error.
- Tolerance-based agreement.

The tolerance must be defined for each numerical task based on its statistical meaning and numerical precision.

### 6.6 Methodological Correctness

Methodological scoring should assess:

- Correct identification of assumptions.
- Appropriate method selection.
- Recognition of limitations.
- Correct handling of survey design.
- Avoidance of leakage.
- Valid interpretation.
- Recognition of insufficient information.

### 6.7 Consistency

Repeated-trial mean and standard deviation should be reported separately for each task-instance/model combination where sufficient valid runs exist.

Consistency must not be confused with correctness: a model can consistently produce an incorrect answer.

---

## 7. Pass@k and Pass^k

### 7.1 Pass@k

Pass@k measures the probability or estimated rate of obtaining at least one successful result among \(k\) attempts under a specified sampling procedure.

A success threshold must be defined before evaluation.

For example, success may require:

- A minimum task score.
- Valid output structure.
- Correct critical methodological decisions.

A common estimator for pass@k, when \(n\) candidate attempts are available and \(c\) of them are successful, is:

\[
\widehat{\text{pass@k}}=
1-
\frac{\binom{n-c}{k}}{\binom{n}{k}}
\]

for \(n\geq k\).

The estimator assumes the candidate attempts represent the sampling procedure being studied.

### 7.2 Pass^k

Pass^k measures the probability or observed rate that all \(k\) required attempts succeed under a defined trial procedure.

For a binary success indicator \(I_r\):

\[
\text{pass}^k=
\prod_{r=1}^{k}I_r
\]

The benchmark must define whether the estimate is based on grouped trial sets, repeated task executions, or another specified sampling procedure.

### 7.3 Interpretation

Pass@k and pass^k answer different questions.

- Pass@k concerns obtaining at least one successful attempt.
- Pass^k concerns obtaining success in every required attempt.

Both depend on the chosen success threshold and trial design.

They should be supplementary metrics rather than substitutes for task-level scores.

### 7.4 Reporting

Reports must state:

- Value of \(k\).
- Number of candidate attempts.
- Success threshold.
- Trial grouping.
- Estimation formula.
- Number of evaluated task instances.

---

## 8. Statistical Analysis

### 8.1 Sources of Variability

The evaluation recognises at least two important sources of variability:

**Task-instance variability:** Performance differences across different instances within a task family.

**Repeated-run variability:** Performance differences when the same model executes the same task instance multiple times.

These sources must be analysed separately where the experimental design permits.

### 8.2 Descriptive Statistics

The benchmark should report:

- Mean score.
- Standard deviation.
- Median score.
- Minimum and maximum.
- Valid execution count.
- Failure count.
- Task-family score distribution.

### 8.3 Uncertainty Estimation

Uncertainty intervals should reflect the evaluation hierarchy.

Where task instances are sampled from a broader task population, uncertainty estimation should account for task-instance variation.

Where repeated trials are conducted on the same task instance, those trials must not automatically be treated as independent task instances.

Possible approaches include:

- Cluster bootstrap over task instances.
- Hierarchical or mixed-effects models, when justified.
- Paired bootstrap comparisons.
- Appropriate confidence intervals for the defined experimental unit.

The selected method must be justified and documented.

### 8.4 Paired Comparisons

When two models are evaluated on the same task instances under comparable conditions, paired differences may be analysed.

For task instance \(i\):

\[
D_i=S_{i,A}-S_{i,B}
\]

The distribution of paired differences can be examined using descriptive summaries and suitable statistical procedures.

The test choice must reflect the number of independent task instances, score distribution, and experimental structure.

### 8.5 Statistical Tests

Potential methods include:

- Paired t-test, when its assumptions are reasonably supported.
- Wilcoxon signed-rank test, where appropriate.
- Bootstrap confidence intervals.
- Hierarchical modelling for nested data, when justified.

No test should be selected solely because it produces a smaller p-value.

### 8.6 Multiple Comparisons

When many models or task families are compared, multiple-comparison issues should be considered.

Where formal hypothesis testing is conducted, an appropriate adjustment procedure may be used.

Effect sizes and uncertainty intervals should be reported alongside p-values.

### 8.7 Practical Significance

A statistically detectable difference does not automatically represent a practically meaningful improvement.

Interpret results in relation to:

- Score difference.
- Task difficulty.
- Failure severity.
- Reliability.
- Cost.
- Latency.
- Intended application.

---

## 9. Model Comparison Protocol

### 9.1 Comparison Dimensions

Models should be compared on:

1. Overall benchmark score.
2. Task-family performance.
3. Methodological correctness.
4. Numerical correctness.
5. Output validity.
6. Repeated-trial consistency.
7. Failure frequency.
8. Execution cost.
9. Latency.

### 9.2 Comparable Conditions

A valid comparison should document:

- Exact model versions.
- Prompt version.
- Task version.
- Generation settings.
- Tool access.
- Trial count.
- Grader version.
- Evaluation date.

### 9.3 Model Ranking

Rankings should not rely solely on the aggregate score.

Reports should include task-family results and uncertainty information.

Models may exhibit different strengths across statistical and machine learning tasks.

The benchmark should avoid declaring a universally superior model from a limited task set.

### 9.4 Comparison Limitations

If models use different tools, reasoning settings, or execution environments, the comparison must disclose these differences.

Results should be interpreted as performance under the tested conditions rather than intrinsic model capability.

---

## 10. Failure Analysis

### 10.1 Purpose

Failure analysis identifies recurring methodological weaknesses that may not be apparent from aggregate scores.

### 10.2 Failure Categories

Responses may be classified into:

- Survey-weight interpretation error.
- Strata and PSU confusion.
- Incorrect weighting strategy.
- Data leakage.
- Invalid validation design.
- Misleading metric selection.
- External validation misunderstanding.
- Missing-data misconception.
- Incorrect uncertainty interpretation.
- Calibration error.
- SHAP or interpretability misinterpretation.
- Unsupported assumptions.
- Invalid structured output.
- Numerical calculation error.

### 10.3 Failure Documentation

Each failure record should include:

- Experiment ID.
- Task ID.
- Model identifier.
- Trial ID.
- Failure category.
- Expected behaviour.
- Observed behaviour.
- Severity.
- Grader decision.
- Supporting response excerpt.

### 10.4 Severity

Failures may be classified as:

- Critical: A methodological error that invalidates the main analytical recommendation.
- Major: An important error that materially affects the workflow or interpretation.
- Minor: An incomplete explanation or limited non-critical omission.

Severity rules must be documented before comparative failure analysis.

---

## 11. Runtime and Cost Evaluation

### 11.1 Runtime

Record:

- Request start time.
- Request completion time.
- Total execution duration.
- Timeout status.
- Retry count.

Where available, distinguish model generation time from total pipeline time.

### 11.2 Cost

Record cost only when reliable provider billing or documented token-pricing information is available.

Potential cost components include:

- Input tokens.
- Output tokens.
- Reasoning tokens, where separately reported.
- Tool execution.
- Other provider charges.

### 11.3 Cost Comparison

Cost should be compared alongside performance.

The benchmark may report:

- Cost per successful task.
- Cost per benchmark run.
- Average cost per task instance.
- Performance relative to cost.

All pricing assumptions and evaluation dates must be recorded.

### 11.4 Missing Cost Information

If reliable pricing information is unavailable, report cost as unavailable.

Do not estimate precise costs from undocumented assumptions.

---

## 12. Reproducibility and Reporting

### 12.1 Required Experiment Metadata

Each execution should preserve:

| Field | Description |
|---|---|
| experiment_id | Unique experiment identifier |
| task_id | Benchmark task identifier |
| task_version | Task definition version |
| task_family | T01–T08 |
| model_provider | Provider |
| model_id | Exact model identifier |
| model_version | Version or snapshot |
| prompt_version | Prompt version |
| trial_id | Repeated-run identifier |
| execution_timestamp | Execution date and time |
| generation_settings | Supported generation parameters |
| tool_access | Enabled tools |
| raw_output | Original model response |
| output_status | Execution and validation status |
| grader_version | Grading implementation version |
| task_score | Individual score |
| runtime | Execution duration |
| cost | Cost, where available |

### 12.2 Result Storage

Raw outputs must be retained separately from aggregated scores.

Recommended logical structure:

```text
results/
    raw/
        model_a/
        model_b/
    scored/
        task_scores.csv
    summaries/
        model_summary.csv
        task_summary.csv
    metadata/
        experiment_config.json
```

The exact directory structure may be refined during implementation.

### 12.3 Reproducibility Checklist

Before reporting results, verify:

- [ ] Task versions are recorded.
- [ ] Prompt versions are recorded.
- [ ] Model identifiers are documented.
- [ ] Execution settings are recorded.
- [ ] Raw outputs are preserved.
- [ ] Failed runs are logged.
- [ ] Grader versions are recorded.
- [ ] Scores can be regenerated from saved outputs.
- [ ] Aggregation procedures are documented.
- [ ] Cost and runtime sources are documented.
- [ ] Restricted data and credentials are excluded.

### 12.4 Reporting Requirements

The final evaluation report should include:

1. Experimental setup.
2. Model identifiers and versions.
3. Benchmark task coverage.
4. Task-family performance.
5. Aggregate performance.
6. Output validity.
7. Repeated-trial variability.
8. Uncertainty estimates.
9. Failure analysis.
10. Runtime and cost.
11. Limitations.
12. Reproducibility details.

---

## 13. Evaluation Protocol Status

**Status:** Proposed evaluation protocol.

This document defines the planned experimental conditions, model identification, prompt standardisation, repeated-trial procedure, evaluation metrics, statistical analysis, failure reporting, and reproducibility requirements.

The protocol must be tested and refined during pilot experiments.

No model rankings, empirical scores, or performance claims are established by this document alone.