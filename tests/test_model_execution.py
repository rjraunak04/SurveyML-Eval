from __future__ import annotations

import json
from pathlib import Path

import pytest

from surveymleval.execution import (
    ExecutionSettings,
    InvalidProviderResponseError,
    MockModelProviderAdapter,
    ModelExecutionEngine,
    OpenAICompatibleAdapter,
    PromptBuilder,
    ProviderConfigurationError,
    TransientProviderError,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_mock_execution_uses_only_model_visible_prompt_content() -> None:
    engine = ModelExecutionEngine(REPO_ROOT)
    task = engine.loader.load_task("T01")
    prompt = PromptBuilder.build(task)

    prompt_payload_text = json.dumps(prompt.prompt_payload, sort_keys=True)
    assert "hidden_reference" not in prompt_payload_text
    assert "must_identify" not in prompt_payload_text
    assert '"outcome"' not in prompt_payload_text
    assert "protected outcome columns" not in prompt_payload_text
    assert "Never disclose hidden reference answers" not in prompt_payload_text
    assert prompt.prompt_payload["model_visible_input"]["allowed_columns"]
    assert prompt.prompt_payload["required_fields"] == [
        "weight_purpose",
        "strata_role",
        "psu_role",
        "variance_method",
        "target_population",
        "recommended_workflow",
    ]


def test_execution_engine_creates_run_ids_and_success_records(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SURVEYML_PROVIDER", "mock")
    monkeypatch.setenv("SURVEYML_MODEL", "mock-model")
    engine = ModelExecutionEngine(REPO_ROOT)
    records = engine.execute_task("T01", provider="mock", model_id="mock-model", trial_count=1, max_retries=1)

    assert len(records) == 1
    assert records[0].status == "success"
    assert records[0].run_id
    assert records[0].structured_response["task_id"] == "T01"
    assert records[0].structured_response["status"] == "success"


def test_retry_handles_transient_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SURVEYML_PROVIDER", "mock")
    engine = ModelExecutionEngine(REPO_ROOT)
    task = engine.loader.load_task("T03")
    prompt = PromptBuilder.build(task)
    settings = ExecutionSettings(provider="mock", model_id="mock-model", max_retries=2)
    adapter = MockModelProviderAdapter(failures=[TransientProviderError("rate limited")])
    monkeypatch.setattr(engine, "_provider_for", lambda provider: adapter)

    record, _ = engine._execute_with_retries(prompt, settings=settings, trial=1)

    assert record.attempt == 2
    assert record.status == "success"


def test_live_provider_requires_env_configuration(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("SURVEYML_ALLOW_LIVE_MODEL_CALLS", raising=False)
    adapter = OpenAICompatibleAdapter()
    task = ModelExecutionEngine(REPO_ROOT).loader.load_task("T02")
    prompt = PromptBuilder.build(task)

    with pytest.raises(ProviderConfigurationError, match="OPENAI_API_KEY"):
        adapter.execute(prompt, settings=ExecutionSettings(provider="openai", model_id="gpt-4o"), trial=1, attempt=1)


def test_invalid_provider_response_is_rejected() -> None:
    engine = ModelExecutionEngine(REPO_ROOT)
    task = engine.loader.load_task("T04")
    with pytest.raises(InvalidProviderResponseError):
        engine._normalize_provider_response("not-json", task=task)


def test_model_execution_ignores_secret_material_in_logs(caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SURVEYML_PROVIDER", "mock")
    monkeypatch.setenv("SURVEYML_MODEL", "mock-model")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-secret-value")
    engine = ModelExecutionEngine(REPO_ROOT)
    records = engine.execute_task("T08", provider="mock", model_id="mock-model")

    assert records[0].status == "success"
    text = json.dumps(records[0].as_dict(), sort_keys=True)
    assert "sk-secret-value" not in text
