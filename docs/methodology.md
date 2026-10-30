# SurveyML-Eval: Research Methodology

## 1. Research Design and Evaluation Philosophy

### 1.1 Research Design

SurveyML-Eval adopts a task-based empirical evaluation design to investigate the statistical reasoning and applied machine learning capabilities of Large Language Models (LLMs).

The benchmark focuses on evaluating whether LLMs can produce statistically defensible and methodologically appropriate decisions when working with survey-based predictive modelling problems.

The evaluation combines:

- Structured statistical reasoning tasks.
- Applied machine learning workflow decisions.
- Synthetic or appropriately licensed datasets.
- Reference-based answer evaluation.
- Deterministic numerical and schema validation.
- Human expert review.
- Repeated model trials.

The benchmark is designed to evaluate methodological correctness rather than only the fluency or plausibility of generated text.

### 1.2 Research Scope

The initial benchmark consists of eight task families:

1. Complex Survey Design and Weight Interpretation.
2. Survey-Weighted Predictive Modelling.
3. Data Leakage Detection and Prevention.
4. Validation Strategy Selection.
5. Class Imbalance and Performance Evaluation.
6. External Validation and Distribution Shift.
7. Missing Data and Statistical Uncertainty.
8. Model Calibration and Interpretability.

Each task family addresses a different component of an applied survey-aware predictive modelling workflow.

### 1.3 Evaluation Philosophy

The benchmark follows five principles:

**Statistical correctness:** Responses must respect statistical assumptions and methodological requirements.

**Context awareness:** Recommendations must be consistent with the target population, estimand, prediction objective, and available data.

**Reproducibility:** Evaluation conditions, task versions, model identifiers, and scoring decisions must be documented.

**Transparency:** Model limitations, missing information, and uncertainty must be reported.

**Fair comparison:** Models should receive comparable inputs and be evaluated under documented and consistent conditions.

---

## 2. Benchmark Architecture

### 2.1 Conceptual Architecture

The benchmark follows a modular evaluation pipeline:

1. Task definition.
2. Dataset and metadata preparation.
3. Prompt construction.
4. Model execution.
5. Response collection.
6. Output validation.
7. Statistical and methodological grading.
8. Trial-level result storage.
9. Performance analysis.
10. Reporting.

### 2.2 Architecture Components

| Component | Responsibility |
|---|---|
| Task Repository | Stores benchmark task instances |
| Dataset Layer | Provides synthetic or appropriately licensed inputs |
| Prompt Layer | Constructs consistent model instructions |
| Model Execution Layer | Sends tasks to selected LLMs |
| Output Layer | Stores raw model responses |
| Validation Layer | Checks output structure and numerical correctness |
| Grading Layer | Calculates task-level scores |
| Human Review Layer | Evaluates ambiguous methodological responses |
| Results Layer | Stores trial-level and aggregated results |

### 2.3 Logical Evaluation Flow

```text
Benchmark Task
      |
      v
Dataset and Metadata
      |
      v
Prompt Construction
      |
      v
Selected LLM
      |
      v
Raw Model Response
      |
      v
Output Validation
      |
      v
Grading Framework
      |
      +-------------------+
      |                   |
      v                   v
Deterministic         Human Expert
Grading               Review
      |                   |
      +---------+---------+
                |
                v
        Final Task Score
                |
                v
        Results Repository
                |
                v
        Statistical Analysis
```

The architecture is a proposed logical design. Executable components will be implemented and tested during the benchmark development stage.

---

## 3. Task Construction Methodology

### 3.1 Task Development

Each benchmark instance will be designed around a clearly defined statistical or machine learning problem.

A task must contain:

- Unique task identifier.
- Task family.
- Difficulty level.
- Problem description.
- Input data or scenario.
- Variable definitions.
- Target population, where relevant.
- Analytical objective.
- Expected output schema.
- Reference solution.
- Scoring criteria.
- Known limitations.

### 3.2 Task Diversity

The eight task families will contain multiple instances rather than relying on a single example per category.

Task instances should vary in:

- Statistical complexity.
- Dataset size.
- Missing information.
- Survey design structure.
- Prediction objective.
- Validation requirements.
- Numerical difficulty.
- Presence of methodological traps.

The purpose is to avoid evaluating an entire task family using one narrow example.

### 3.3 Difficulty Levels

Tasks will initially be classified into three levels.

| Level | Description |
|---|---|
| Basic | Fundamental statistical concepts and straightforward interpretation |
| Intermediate | Multiple methodological decisions with moderate complexity |
| Advanced | Interacting statistical assumptions, competing methods, or incomplete information |

Difficulty labels are initial design classifications and will be reviewed after pilot testing.

### 3.4 Controlled Task Variations

Task variations may be introduced to test whether models adapt their recommendations when relevant conditions change.

Examples include:

- Changing the target population.
- Adding or removing sampling weights.
- Introducing PSU clustering.
- Changing the prediction-time definition.
- Replacing internal validation with an external dataset.
- Increasing outcome imbalance.
- Introducing additional missingness.
- Providing different calibration evidence.

Task variants must preserve the intended evaluation objective and have independently reviewed reference answers.

---

## 4. Dataset Generation and Data Governance

### 4.1 Dataset Strategy

The initial benchmark will prioritise synthetic datasets and appropriately licensed public datasets.

Synthetic data will be used to create controlled scenarios in which the underlying data-generating process and expected methodological decisions can be documented.

Public datasets may be considered when their licences, access conditions, redistribution rights, and attribution requirements permit the intended use.

### 4.2 Synthetic Dataset Generation

Synthetic datasets may be generated to represent:

- Stratified sampling.
- Clustered sampling.
- Unequal selection probabilities.
- Binary classification.
- Imbalanced outcomes.
- Missing data mechanisms.
- Group-level dependence.
- Temporal variation.
- Population distribution changes.
- Calibration differences.

Where possible, the generation procedure will document:

1. Data-generating assumptions.
2. Population characteristics.
3. Sampling mechanism.
4. Variable definitions.
5. Outcome generation.
6. Missingness generation.
7. Random seed.
8. Expected analytical properties.

Synthetic data must not be described as real survey observations.

### 4.3 External Survey Data

NFHS, DHS, and similar survey sources may provide useful methodological context.

However, access to a dataset does not automatically imply permission to redistribute it.

Before incorporating any external survey dataset, the project must verify:

- Access conditions.
- Data-use agreement.
- Redistribution permissions.
- Attribution requirements.
- Privacy restrictions.
- Whether derived materials can be publicly shared.

Restricted microdata must not be included in the public benchmark ZIP or GitHub repository without explicit permission.

### 4.4 Data Quality Checks

Dataset preparation should include:

- Schema validation.
- Variable type validation.
- Missing-value checks.
- Duplicate-record checks.
- Weight validity checks.
- Category validation.
- Target-variable validation.
- Consistency between metadata and data.
- Reproducibility checks using documented random seeds.

---

## 5. Reference Answer Development

### 5.1 Reference Solution Principles

Every task instance must have a documented reference solution or grading rubric.

Reference solutions should be developed using established statistical and machine learning principles.

They must identify:

- Expected conclusions.
- Acceptable alternative approaches.
- Required assumptions.
- Invalid methodological choices.
- Numerical reference values, where applicable.
- Important limitations.
- Conditions under which additional information is required.

### 5.2 Multiple Valid Solutions

Statistical problems may admit more than one defensible approach.

The grading framework must not penalise a model simply because it selects a valid alternative to the preferred reference method.

Alternative solutions should be accepted when they:

1. Address the stated objective.
2. Satisfy the relevant assumptions.
3. Respect the data structure.
4. Explain methodological limitations.
5. Avoid unsupported conclusions.

### 5.3 Expert Review

Reference solutions should be reviewed by an appropriate statistics or machine learning expert before being treated as final benchmark ground truth.

Review records should include:

- Reviewer identifier or role.
- Task identifier.
- Review date.
- Suggested corrections.
- Resolution of disagreements.
- Reference answer version.

Where expert review has not occurred, the task must be labelled as a draft or pending validation.

---

## 6. Model Selection Strategy

### 6.1 Model Selection Principles

Models will be selected according to:

- Relevance to the benchmark objective.
- Availability of a documented model identifier.
- Reproducibility of execution.
- Access to comparable evaluation conditions.
- Practical execution cost.
- Availability of raw outputs.
- Suitability for the task complexity.

### 6.2 Model Categories

The benchmark may include:

- General-purpose instruction-following LLMs.
- Reasoning-oriented LLMs.
- Open-weight language models.
- Models with supported code-execution capabilities, where applicable.

The initial benchmark must clearly distinguish models with different tool access and execution capabilities.

### 6.3 Model Identification

For every evaluated model, record:

- Provider.
- Exact model identifier.
- Version or snapshot, where available.
- Access method.
- API or interface version, where relevant.
- Evaluation date.
- Generation settings.
- Tool availability.
- Relevant execution constraints.

A model's marketing name alone is insufficient for reproducible identification when a more specific identifier is available.

### 6.4 Fair Comparison

Models should receive equivalent task content and consistent output requirements.

If a model requires different technical settings, these must be documented.

Tool-enabled and non-tool-enabled evaluations should not be silently combined into one comparison.

Any model-specific prompt adaptation must be versioned and disclosed.

---

## 7. Experimental Execution Workflow

### 7.1 Evaluation Procedure

Each model evaluation will follow a controlled workflow:

1. Select a versioned benchmark task.
2. Load its corresponding input and metadata.
3. Construct the evaluation prompt.
4. Record the exact model identifier.
5. Record generation settings.
6. Execute the task.
7. Save the raw response.
8. Validate the response schema.
9. Run deterministic grading where applicable.
10. Perform semantic or human grading where required.
11. Save the individual task score.
12. Record execution time and cost where available.

### 7.2 Repeated Trials

An initial experimental plan is to conduct three to five repeated trials per task and model under documented conditions.

The final number of trials may change after pilot evaluation, depending on observed variability, API cost, model availability, and statistical precision requirements.

Repeated trials should preserve:

- Task version.
- Model version.
- Prompt version.
- Generation settings.
- Trial identifier.
- Random seed where applicable.
- Raw response.
- Individual score.
- Execution metadata.

Repeated calls should not automatically be assumed to be independent observations.

### 7.3 Failed and Invalid Runs

The experiment must distinguish:

- Successful model response.
- Invalid structured output.
- API or execution failure.
- Timeout.
- Refusal.
- Incomplete response.
- Grader failure.

Failures should be logged rather than silently discarded.

Any exclusion from analysis must follow predefined rules and be reported transparently.

---

## 8. Statistical Evaluation Framework

### 8.1 Task-Level Scoring

Each task family has an initial maximum score of 10 points.

With eight task families, the initial maximum aggregate score is 80 points.

The benchmark will report individual task performance alongside the aggregate score.

### 8.2 Primary Performance Measures

The initial reporting framework includes:

- Task-level score.
- Overall benchmark score.
- Criterion-level score.
- Output schema validity.
- Numerical correctness.
- Methodological correctness.
- Trial-to-trial variability.
- Failure category frequencies.

### 8.3 Aggregate Performance

For a model with eight task-family scores:

\[
S_{\text{total}}=\sum_{j=1}^{8}S_j
\]

where \(S_j\) represents the score for task family \(j\), with:

\[
0\leq S_j\leq 10
\]

The maximum aggregate score is:

\[
S_{\text{maximum}}=80
\]

An aggregate score should be interpreted together with task-level performance.

A high overall score must not conceal a serious weakness in a specific statistical methodology.

### 8.4 Repeated-Trial Performance

For task \(j\), model \(m\), and trial \(r\), let:

\[
S_{jmr}
\]

represent the observed task score.

The mean score across \(R\) trials is:

\[
\bar S_{jm}=\frac{1}{R}\sum_{r=1}^{R}S_{jmr}
\]

Trial-level standard deviation may be reported as:

\[
SD_{jm}=
\sqrt{
\frac{\sum_{r=1}^{R}(S_{jmr}-\bar S_{jm})^2}{R-1}
}
\]

These summaries describe observed performance and variability.

Uncertainty intervals should be selected according to the actual sampling and experimental design. A small number of repeated trials may provide imprecise estimates.

### 8.5 Pass@k and Pass^k

Pass@k and pass^k may be reported as supplementary measures.

Their definitions, success thresholds, trial structure, and estimation procedure must be specified before analysis.

They should not be treated as interchangeable.

For pass@k, the benchmark must define what counts as a successful attempt and how multiple candidate attempts are sampled.

For pass^k, the benchmark must define the requirement that all relevant attempts succeed.

### 8.6 Model Comparisons

Model comparisons should consider:

- Overall score differences.
- Task-specific differences.
- Trial-level variability.
- Output validity.
- Failure categories.
- Execution conditions.
- Cost and latency where available.

Uncertainty estimates should reflect the experimental unit and dependence structure.

When models are evaluated on the same tasks, paired comparisons may be appropriate.

Any statistical test must be selected according to its assumptions and the available number of independent evaluation units.

Statistical significance must not be interpreted as practical importance.

---

## 9. Human Expert Validation

### 9.1 Purpose

Automated scoring cannot reliably evaluate every form of statistical reasoning.

Human review is therefore required for responses involving:

- Context-dependent methodological decisions.
- Multiple valid statistical approaches.
- Ambiguous explanations.
- Unsupported assumptions.
- Interpretation of limitations.
- Complex survey-design reasoning.

### 9.2 Human Review Procedure

Human reviewers should receive:

- Task input.
- Reference solution.
- Model response.
- Scoring rubric.
- Relevant evaluation criteria.

Where feasible, reviewers should not be shown model identity during the initial response assessment to reduce potential evaluation bias.

### 9.3 Inter-Rater Reliability

When multiple reviewers evaluate the same responses, agreement should be assessed using a suitable measure.

Possible measures include:

- Cohen's kappa for appropriate two-rater categorical assessments.
- Weighted kappa for suitable ordinal ratings.
- Intraclass correlation for appropriate numerical ratings.
- Percentage agreement as a supplementary descriptive measure.

The selected measure must match the scale and structure of the grading data.

Disagreements should be documented and resolved using a predefined adjudication process.

---

## 10. Reproducibility and Transparency

### 10.1 Experiment Records

Each experiment should preserve:

- Experiment ID.
- Task ID.
- Task version.
- Model provider.
- Exact model identifier.
- Prompt version.
- Execution date and time.
- Generation parameters.
- Tool access.
- Raw model response.
- Grader version.
- Individual score.
- Execution duration.
- Cost where available.

### 10.2 Version Control

Benchmark tasks, prompts, reference answers, grading scripts, and evaluation configurations should be version controlled.

Changes to task content or grading rules must be documented.

Previously generated scores should not be silently overwritten when a benchmark version changes.

### 10.3 Reproducibility Artifacts

The project should progressively maintain:

- Versioned task definitions.
- Synthetic dataset generation scripts.
- Data dictionaries.
- Reference answers.
- Scoring scripts.
- Unit tests.
- Experiment configuration files.
- Raw model outputs.
- Aggregated evaluation results.
- Environment and dependency documentation.

### 10.4 Public Release

Only authorised and appropriately shareable materials should be included in public releases.

Secrets, credentials, API keys, private datasets, and restricted records must never be committed.

An `.env.example` file may document environment variable names without including actual secret values.

---

## 11. Research Ethics and Limitations

### 11.1 Data Ethics

The benchmark will prioritise synthetic and properly licensed data.

It must not expose personal identifiers, confidential survey responses, or restricted microdata.

### 11.2 Model Evaluation Ethics

The benchmark evaluates specific model behaviour under documented conditions.

It does not establish that a model is universally reliable or suitable for unsupervised statistical decision-making.

### 11.3 Methodological Limitations

Potential limitations include:

- Limited task coverage.
- Synthetic-to-real-world generalisation gaps.
- Dependence on reference answer quality.
- Variation in model versions.
- API and provider changes.
- Limited repeated trials.
- Human grading subjectivity.
- Differences in tool access.
- Sensitivity to prompt wording.
- Dataset-specific performance.

### 11.4 Research Scope Limitations

The initial benchmark focuses on survey-aware statistical reasoning and predictive machine learning.

It is not intended to evaluate all areas of data science, general intelligence, causal discovery, or every possible application of LLMs.

Claims about benchmark novelty, generalisation, and model superiority must be supported by completed literature review and empirical evidence.

---

## 12. Research Implementation Roadmap

| Stage | Work | Status |
|---|---|---|
| Stage 1 | Research problem and objectives | Completed |
| Stage 2 | Preliminary literature review | Completed |
| Stage 3 | Eight benchmark task designs | Initial designs drafted |
| Stage 4 | Research methodology | Documentation in progress |
| Stage 5 | Evaluation protocol | Pending |
| Stage 6 | Grading framework | Pending |
| Stage 7 | Synthetic dataset and task instances | Pending |
| Stage 8 | Executable benchmark and unit tests | Pending |
| Stage 9 | Pilot experiments | Pending |
| Stage 10 | Model evaluation and statistical analysis | Pending |
| Stage 11 | Research paper and final submission | Pending |

---

## 13. Methodology Document Status

**Status:** Proposed research methodology.

This document defines the planned benchmark architecture, task construction process, data strategy, model evaluation workflow, grading principles, statistical reporting, and reproducibility requirements.

The methodology is subject to refinement after task implementation, pilot testing, expert review, and empirical evaluation.

No benchmark performance results or validated model rankings are claimed at this stage.