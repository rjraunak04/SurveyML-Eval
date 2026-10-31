# Execution Architecture Specification

**Project:** SurveyML-Eval
**Document:** Execution Architecture Specification
**Version:** 1.0
**Status:** Proposed architecture
**Checkpoint:** CP-06D

---

## 1. Purpose

This document defines the execution architecture for SurveyML-Eval.

The execution architecture specifies how benchmark tasks are prepared, submitted to large language models (LLMs), executed across multiple trials, and recorded for subsequent grading and statistical analysis.

It establishes a provider-independent execution pipeline that supports consistent evaluation across different model providers and model versions.

The architecture prioritizes reproducibility, traceability, execution reliability, and fair comparison.

## 2. Execution Design Principles

The execution architecture follows these principles:

1. **Provider independence:** Benchmark execution must not depend on a single LLM provider.
2. **Consistency:** Equivalent benchmark tasks must be presented consistently across models.
3. **Reproducibility:** Every execution must preserve its model configuration and execution conditions.
4. **Traceability:** Each response must be traceable to its task, model, trial, and execution record.
5. **Response preservation:** Original model responses must be retained without modification.
6. **Failure transparency:** API failures, timeouts, and incomplete executions must be recorded.
7. **Controlled retries:** Retry policies must not silently create additional benchmark trials.
8. **Usage tracking:** Token consumption, runtime, and cost should be recorded when available.
9. **Security:** API credentials must be managed outside source code and benchmark data.
10. **Research integrity:** Failed or incomplete executions must not be represented as successful model responses.

## 3. High-Level Execution Architecture

The proposed execution pipeline contains the following components:

1. Benchmark configuration loader.
2. Task loader.
3. Dataset and input loader.
4. Prompt construction module.
5. Model provider adapter.
6. Execution engine.
7. Trial manager.
8. Response storage module.
9. Execution metadata logger.
10. Grading pipeline interface.

The execution engine coordinates these components without embedding provider-specific logic into benchmark task definitions.

## 4. Proposed Execution Flow

The benchmark execution process follows this sequence:

1. Load benchmark configuration.
2. Load the selected task instances.
3. Validate task and dataset references.
4. Select the model and provider configuration.
5. Construct the model-facing prompt.
6. Submit the request through the appropriate provider adapter.
7. Receive the model response or execution error.
8. Record raw response and usage metadata.
9. Repeat according to the configured trial policy.
10. Store execution records.
11. Pass eligible responses to the grading pipeline.

Only successfully completed responses should be treated as completed model outputs.

Failed and incomplete executions must remain visible in execution records.

## 5. Model Provider Adapter Architecture

Provider-specific communication must be isolated behind a common interface.

### 5.1 Common Model Adapter Responsibilities

Every adapter should support:

- Model identification.
- Request preparation.
- Prompt submission.
- Response retrieval.
- Usage metadata extraction.
- Error normalization.
- Timeout handling.
- Provider-specific configuration.

### 5.2 Provider Independence

The benchmark task definition must not contain provider-specific API calls.

The execution engine should communicate with a common adapter interface.

Provider-specific implementations may be developed for:

- OpenAI models.
- Anthropic models.
- Google models.
- Other supported APIs.
- Locally hosted models, where applicable.

Actual provider support will depend on implementation and API availability.

### 5.3 Model Identification

Every model configuration should record:

- Provider name.
- Model identifier.
- Exact model version or snapshot, when available.
- API or interface version, where relevant.
- Configuration identifier.
- Access date.

A changing model alias must not be treated as an immutable model version.

If an exact version is unavailable, the limitation must be documented.

## 6. Prompt Construction

The prompt builder converts an approved benchmark task definition into a model-facing request.

It must:

- Retrieve the public task definition.
- Include the appropriate input data.
- Preserve the intended task instructions.
- Apply a consistent response-format specification.
- Exclude hidden reference answers.
- Exclude private grading rubrics.
- Record the final submitted prompt or a reproducible prompt representation.

System instructions, user instructions, and any provider-specific message formatting must be documented.

Differences introduced by provider adapters must not change the substantive task requirements.

## 7. Trial Management

Multiple trials are required to assess variation in model responses.

The trial manager must distinguish between:

- Task instance.
- Model configuration.
- Trial.
- Execution attempt.
- Retry.

A trial represents one intended model response for a particular task and model configuration.

An execution attempt represents an API submission associated with that trial.

A retry is a repeated attempt to complete the same intended trial after a recoverable failure.

Retries must not automatically count as additional independent trials.

### 7.1 Trial Configuration

The benchmark configuration should define:

- Number of trials per task and model.
- Sampling parameters.
- Maximum output tokens.
- Timeout limits.
- Retry limits.
- Random seed, if supported.
- Execution order or randomization policy.

Where the provider does not support deterministic generation, the limitation must be documented.

## 8. Execution Configuration

Execution settings must be stored separately from task definitions.

Configuration may include:

- Benchmark version.
- Selected task families.
- Task instance identifiers.
- Model provider.
- Model identifier and version.
- Temperature.
- Top-p.
- Maximum output tokens.
- Timeout duration.
- Trial count.
- Retry policy.
- Output format.
- Execution date and time.
- Concurrency settings.

Every execution must reference the configuration used to generate it.

Configuration changes between benchmark runs must be recorded as distinct configurations.

## 9. Response Handling and Preservation

The response handler is responsible for storing the original model output.

Each completed response should preserve:

- Raw response text.
- Structured response content, where available.
- Model identifier.
- Task instance identifier.
- Trial identifier.
- Execution identifier.
- Response timestamp.
- Provider response metadata.
- Token usage, where available.
- Completion status.

Raw responses must not be silently edited, corrected, or rewritten before grading.

Any normalized representation used for automated grading must be stored separately from the original response.

## 10. Error Handling and Retry Policy

The execution system must identify and record common failure categories.

Examples include:

- Authentication failure.
- Rate-limit error.
- Network error.
- Request timeout.
- Provider service unavailable.
- Invalid request.
- Context-length limitation.
- Response parsing failure.
- Incomplete response.
- Unknown provider error.

### 10.1 Retry Handling

Retries may be permitted for recoverable errors, subject to configured limits.

Each retry must preserve:

- Original trial identifier.
- Attempt number.
- Failure category.
- Retry timestamp.
- Retry outcome.

Permanent failures must not be retried indefinitely.

Authentication and invalid-request errors should be investigated rather than repeatedly resubmitted.

### 10.2 Failed Executions

Failed executions must remain in the execution log.

They must not be silently excluded from benchmark reporting.

The final analysis must distinguish between model response failures and infrastructure or provider failures.

## 11. Token Usage, Runtime and Cost Tracking

The execution system should record usage and resource information where available.

| Metric | Description |
|---|---|
| input_tokens | Input token count |
| output_tokens | Output token count |
| total_tokens | Total reported token usage |
| latency_ms | Request-to-response duration |
| execution_status | Completed, failed, or incomplete |
| estimated_cost | Estimated execution cost |
| currency | Cost reporting currency |

Token counts should use provider-reported values when available.

Cost calculations must use documented pricing sources and the applicable model pricing version.

If token usage or cost is unavailable, it must be recorded as unavailable rather than estimated without evidence.

Execution timestamps should use ISO 8601 with timezone information.

## 12. Execution Record Structure

Every intended trial must have a traceable execution record.

The logical record should include:

- benchmark_id
- benchmark_version
- execution_id
- task_id
- task_instance_id
- model_id
- model_provider
- model_version
- trial_id
- attempt_number
- configuration_id
- started_at
- completed_at
- execution_status
- error_category
- input_tokens
- output_tokens
- latency_ms
- estimated_cost
- response_reference

The execution record must distinguish a trial from its individual API attempts.

## 13. Logical Execution Record Example

The following JSON illustrates a proposed execution record.

It is an example of record structure, not an actual API response or experimental result.

```json
{
  "benchmark_id": "SurveyML-Eval",
  "benchmark_version": "1.0.0",
  "execution_id": "EX-T01-001-M01-R01",
  "task_id": "T01",
  "task_instance_id": "T01-001",
  "model_id": "MODEL-001",
  "model_provider": "example_provider",
  "model_version": "example_model_version",
  "trial_id": "TR-T01-001-M01-01",
  "attempt_number": 1,
  "configuration_id": "CFG-001",
  "started_at": "2026-10-31T10:00:00+05:30",
  "completed_at": "2026-10-31T10:00:05+05:30",
  "execution_status": "completed",
  "error_category": null,
  "input_tokens": null,
  "output_tokens": null,
  "latency_ms": 5000,
  "estimated_cost": null,
  "response_reference": "results/raw_outputs/EX-T01-001-M01-R01.json"
}
```

All values are illustrative placeholders. They do not represent a real model execution.

## 14. Execution Storage Structure

The proposed storage structure is:

```text
results/
├── raw_outputs/
│   ├── T01/
│   ├── T02/
│   ├── T03/
│   ├── T04/
│   ├── T05/
│   ├── T06/
│   ├── T07/
│   └── T08/
├── execution_logs/
│   ├── benchmark_runs/
│   ├── attempts/
│   └── errors/
├── graded_outputs/
├── scores/
└── reports/
```

Raw responses and execution logs must remain separate from graded outputs.

The proposed directory structure does not indicate that these components have already been implemented.

## 15. Reproducibility Requirements

Every benchmark run should preserve:

- Benchmark version.
- Task definition versions.
- Dataset versions.
- Model identifiers and exact versions, where available.
- Prompt representation.
- Execution configuration.
- Trial count.
- Sampling parameters.
- Random seeds, where supported.
- Execution timestamps.
- Raw responses.
- Error records.
- Token usage.
- Runtime and cost information, where available.

Reproducibility does not guarantee identical outputs from nondeterministic model APIs.

Instead, it requires preserving sufficient information to understand and audit the conditions under which each result was obtained.

## 16. Security and Credential Management

The execution architecture must protect API credentials and confidential information.

Requirements include:

- Store credentials in environment variables.
- Exclude `.env` files from version control.
- Provide `.env.example` containing variable names only.
- Never write API keys into task definitions.
- Never include credentials in logs.
- Avoid exposing sensitive provider responses.
- Apply appropriate access restrictions to execution results.

Provider credentials must not be committed to the public repository.

## 17. Execution Validation and Testing

The execution pipeline should be tested at multiple levels.

### 17.1 Unit Testing

Test:

- Configuration parsing.
- Prompt construction.
- Model adapter interface.
- Response normalization.
- Error classification.
- Trial identifier generation.
- Usage metadata extraction.

### 17.2 Integration Testing

Test:

- Task loading and validation.
- Adapter communication.
- Execution orchestration.
- Response storage.
- Retry behavior.
- Execution metadata recording.

### 17.3 Failure Testing

Test controlled scenarios involving:

- Invalid configuration.
- Missing credentials.
- Rate limits.
- Timeouts.
- Malformed responses.
- Interrupted execution.
- Duplicate execution attempts.

Tests should use mocks or controlled fixtures where external API access is unnecessary.

## 18. Relationship with Other Components

The execution architecture integrates with:

- Repository architecture.
- Benchmark task schema.
- Dataset schema.
- Model provider adapters.
- Response storage.
- Grading architecture.
- Statistical evaluation pipeline.
- Reporting system.

The task schema defines what is evaluated.

The dataset schema defines the structure and provenance of inputs.

The execution architecture defines how models receive tasks and how their responses are recorded.

The grading architecture defines how the responses are assessed.

## 19. Implementation Boundaries

This checkpoint defines the logical execution architecture.

It does not implement:

- Production API integrations.
- Actual provider adapters.
- Automated benchmark runs.
- Retry and rate-limit code.
- Token or cost calculation services.
- Full response storage implementation.
- Experimental model comparisons.

These components will be developed incrementally after architecture approval.

## 20. Acceptance Criteria

CP-06D will be considered complete when:

1. The provider-independent execution design is documented.
2. The model adapter responsibilities are defined.
3. Prompt construction requirements are specified.
4. Trial and attempt identifiers are distinguished.
5. Execution configuration fields are documented.
6. Raw response preservation is specified.
7. Error and retry policies are defined.
8. Token, latency, and cost tracking are addressed.
9. A logical execution record example is provided.
10. Execution storage conventions are documented.
11. Security and reproducibility requirements are covered.
12. Testing requirements are documented.
13. The document passes content and formatting review.

## 21. Architecture Status

**Status:** Proposed execution architecture specification.

This document establishes the logical execution contract for SurveyML-Eval.

The architecture will be refined during implementation and validated through controlled execution tests before being treated as a stable benchmark execution specification.
