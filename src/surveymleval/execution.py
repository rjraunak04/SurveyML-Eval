from __future__ import annotations

import json
import os
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Mapping, Sequence

from .engine import BenchmarkTask, TaskLoader


class ModelExecutionError(RuntimeError):
    """Raised when model execution fails for a task."""


class ProviderConfigurationError(ModelExecutionError):
    """Raised when a model provider is not configured or its env secrets are missing."""


class TransientProviderError(ModelExecutionError):
    """Raised for transient provider issues such as timeouts or rate limits."""


class InvalidProviderResponseError(ModelExecutionError):
    """Raised when a provider returns malformed or unusable output."""


@dataclass(frozen=True)
class ExecutionSettings:
    provider: str = "mock"
    model_id: str = "mock-model"
    temperature: float = 0.0
    max_output_tokens: int = 512
    timeout_seconds: float = 30.0
    trial_count: int = 1
    max_retries: int = 2
    seed: int | None = None
    dry_run: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def run_id(self) -> str:
        namespace = uuid.NAMESPACE_URL
        identity = f"SurveyML-Eval::{self.provider}::{self.model_id}::{self.seed if self.seed is not None else 'default'}"
        return uuid.uuid5(namespace, identity).hex


@dataclass(frozen=True)
class PromptRequest:
    task: BenchmarkTask
    prompt_payload: dict[str, Any]
    system_prompt: str
    user_prompt: str
    response_schema: dict[str, Any]


@dataclass
class ExecutionRecord:
    run_id: str
    task_id: str
    task_instance_id: str
    provider: str
    model_id: str
    trial: int
    attempt: int
    started_at: str
    completed_at: str | None = None
    status: str = "pending"
    prompt: dict[str, Any] | None = None
    raw_response: Any = None
    structured_response: dict[str, Any] | None = None
    provider_metadata: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    latency_ms: int | None = None
    token_usage: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "task_id": self.task_id,
            "task_instance_id": self.task_instance_id,
            "provider": self.provider,
            "model_id": self.model_id,
            "trial": self.trial,
            "attempt": self.attempt,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "status": self.status,
            "prompt": self.prompt,
            "raw_response": self.raw_response,
            "structured_response": self.structured_response,
            "provider_metadata": self.provider_metadata,
            "metadata": self.metadata,
            "latency_ms": self.latency_ms,
            "token_usage": self.token_usage,
            "error": self.error,
        }


class PromptBuilder:
    """Construct model-facing prompts that exclude protected reference material."""

    _FORBIDDEN_TEXT_SNIPPETS = (
        "hidden answers",
        "hidden reference answers",
        "protected outcome columns",
        "protected columns",
        "leakage labels",
        "Do not expose hidden answers",
        "Never disclose hidden reference answers",
        "Do not expose hidden answers, leakage labels, or protected outcome columns",
        "Never disclose hidden reference answers, grading metadata, or protected outcome columns",
    )

    @classmethod
    def _sanitize_model_text(cls, value: Any) -> str:
        cleaned = str(value or "")
        for snippet in cls._FORBIDDEN_TEXT_SNIPPETS:
            cleaned = cleaned.replace(snippet, "")
        cleaned = " ".join(cleaned.split())
        return cleaned or "Use only the public model-visible data and return JSON matching the required response schema."

    @staticmethod
    def build(task: BenchmarkTask) -> PromptRequest:
        prompt_info = task.prompt if isinstance(task.prompt, Mapping) else {}
        required_fields = list(task.response_schema.get("required_fields", []))
        raw_prompt_text = str(prompt_info.get("text", "")).strip() or (
            f"Task {task.task_id} ({task.task_instance_id}) with family {task.task_family}. "
            "Return JSON matching the required schema."
        )
        prompt_text = PromptBuilder._sanitize_model_text(raw_prompt_text)
        model_visible_input = task.model_visible_input if isinstance(task.model_visible_input, Mapping) else {}
        safe_payload = {
            "description": PromptBuilder._sanitize_model_text(model_visible_input.get("description", "")),
            "allowed_columns": list(model_visible_input.get("allowed_columns", [])),
            "inputs_are_public": bool(model_visible_input.get("inputs_are_public", True)),
            "reference_files": list(model_visible_input.get("reference_files", [])),
            "dataset_refs": [ref.as_dict() for ref in task.dataset_refs],
        }
        system_prompt = (
            "You are completing a SurveyML-Eval benchmark task. "
            "Use only model-visible public task content. "
            "Return valid JSON matching the required response schema."
        )
        user_prompt = json.dumps(
            {
                "benchmark_id": task.benchmark_id,
                "benchmark_version": task.benchmark_version,
                "task_id": task.task_id,
                "task_instance_id": task.task_instance_id,
                "title": task.title,
                "task_family": task.task_family,
                "difficulty": task.difficulty,
                "model_visible_input": safe_payload,
                "prompt": prompt_text,
                "required_fields": required_fields,
            },
            sort_keys=True,
        )
        return PromptRequest(
            task=task,
            prompt_payload={
                "benchmark_id": task.benchmark_id,
                "benchmark_version": task.benchmark_version,
                "task_id": task.task_id,
                "task_instance_id": task.task_instance_id,
                "title": task.title,
                "task_family": task.task_family,
                "difficulty": task.difficulty,
                "model_visible_input": safe_payload,
                "required_fields": required_fields,
                "prompt": prompt_text,
            },
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_schema=task.response_schema,
        )


class ModelProviderAdapter(ABC):
    """Provider-independent API contract for LLM providers."""

    name: str

    @abstractmethod
    def execute(
        self,
        prompt: PromptRequest,
        *,
        settings: ExecutionSettings,
        trial: int,
        attempt: int,
    ) -> tuple[Any, dict[str, Any]]:
        """Return a raw response payload and provider metadata."""

    @classmethod
    def supported_providers(cls) -> tuple[str, ...]:
        return tuple()


class MockModelProviderAdapter(ModelProviderAdapter):
    """A deterministic mock execution path used for tests and dry-run benchmarking."""

    name = "mock"

    def __init__(self, *, failures: Sequence[Exception] | None = None, responses: Sequence[Any] | None = None) -> None:
        self._failures = list(failures or [])
        self._responses = list(responses or [])

    @classmethod
    def supported_providers(cls) -> tuple[str, ...]:
        return ("mock",)

    def execute(
        self,
        prompt: PromptRequest,
        *,
        settings: ExecutionSettings,
        trial: int,
        attempt: int,
    ) -> tuple[Any, dict[str, Any]]:
        if self._failures:
            exc = self._failures.pop(0)
            raise exc
        if self._responses:
            response = self._responses.pop(0)
        else:
            response = {
                "task_id": prompt.task.task_id,
                "task_instance_id": prompt.task.task_instance_id,
                "response": {field: f"mock_{field}" for field in prompt.response_schema.get("required_fields", [])},
            }
        metadata = {
            "provider": self.name,
            "model_id": settings.model_id,
            "trial": trial,
            "attempt": attempt,
            "dry_run": settings.dry_run,
            "fake_latency_ms": 12,
            "request_type": "mock",
        }
        return response, metadata


class OpenAICompatibleAdapter(ModelProviderAdapter):
    """Generic OpenAI-compatible adapter with a dry-run guard for live calls."""

    name = "openai"

    @classmethod
    def supported_providers(cls) -> tuple[str, ...]:
        return ("openai", "azure-openai")

    def _credential_name(self) -> str:
        return "OPENAI_API_KEY"

    def _read_key(self) -> str:
        key = os.environ.get(self._credential_name())
        if not key:
            raise ProviderConfigurationError(f"Missing required environment variable {self._credential_name()}.")
        return key

    def execute(
        self,
        prompt: PromptRequest,
        *,
        settings: ExecutionSettings,
        trial: int,
        attempt: int,
    ) -> tuple[Any, dict[str, Any]]:
        if not (os.environ.get("SURVEYML_ALLOW_LIVE_MODEL_CALLS", "").lower() in {"1", "true", "yes"}):
            raise ProviderConfigurationError(
                "Live OpenAI calls are disabled. Set SURVEYML_ALLOW_LIVE_MODEL_CALLS=true and OPENAI_API_KEY to enable them."
            )
        self._read_key()
        raise ModelExecutionError("Live model execution is intentionally disabled in this repository. Use the mock provider for dry-run validation.")


class AnthropicAdapter(ModelProviderAdapter):
    name = "anthropic"

    @classmethod
    def supported_providers(cls) -> tuple[str, ...]:
        return ("anthropic",)

    def execute(
        self,
        prompt: PromptRequest,
        *,
        settings: ExecutionSettings,
        trial: int,
        attempt: int,
    ) -> tuple[Any, dict[str, Any]]:
        if not (os.environ.get("SURVEYML_ALLOW_LIVE_MODEL_CALLS", "").lower() in {"1", "true", "yes"}):
            raise ProviderConfigurationError(
                "Live Anthropic calls are disabled. Set SURVEYML_ALLOW_LIVE_MODEL_CALLS=true and ANTHROPIC_API_KEY to enable them."
            )
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise ProviderConfigurationError("Missing required environment variable ANTHROPIC_API_KEY.")
        raise ModelExecutionError("Live model execution is intentionally disabled in this repository. Use the mock provider for dry-run validation.")


class GoogleGenerativeAdapter(ModelProviderAdapter):
    name = "google"

    @classmethod
    def supported_providers(cls) -> tuple[str, ...]:
        return ("google", "gemini")

    def execute(
        self,
        prompt: PromptRequest,
        *,
        settings: ExecutionSettings,
        trial: int,
        attempt: int,
    ) -> tuple[Any, dict[str, Any]]:
        if not (os.environ.get("SURVEYML_ALLOW_LIVE_MODEL_CALLS", "").lower() in {"1", "true", "yes"}):
            raise ProviderConfigurationError(
                "Live Google model calls are disabled. Set SURVEYML_ALLOW_LIVE_MODEL_CALLS=true and GOOGLE_API_KEY to enable them."
            )
        key = os.environ.get("GOOGLE_API_KEY")
        if not key:
            raise ProviderConfigurationError("Missing required environment variable GOOGLE_API_KEY.")
        raise ModelExecutionError("Live model execution is intentionally disabled in this repository. Use the mock provider for dry-run validation.")


class ModelExecutionEngine:
    """Execute benchmark tasks through a provider-independent execution layer."""

    _provider_map: dict[str, type[ModelProviderAdapter]] = {
        "mock": MockModelProviderAdapter,
        "openai": OpenAICompatibleAdapter,
        "azure-openai": OpenAICompatibleAdapter,
        "anthropic": AnthropicAdapter,
        "google": GoogleGenerativeAdapter,
        "gemini": GoogleGenerativeAdapter,
    }

    def __init__(self, repo_root: str | None = None, loader: TaskLoader | None = None) -> None:
        self.loader = loader or TaskLoader(repo_root)
        from .storage import ResponseStorage
        self.storage = ResponseStorage(repo_root)

    @property
    def supported_providers(self) -> tuple[str, ...]:
        providers: set[str] = set()
        for provider_map in self._provider_map.values():
            providers.update(provider_map.supported_providers())
        return tuple(sorted(providers))

    @staticmethod
    def _utc_now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _provider_for(self, provider: str) -> ModelProviderAdapter:
        provider_name = (provider or "mock").strip().lower()
        adapter_cls = self._provider_map.get(provider_name)
        if adapter_cls is None:
            raise ProviderConfigurationError(f"Unsupported provider {provider!r}. Supported providers: {', '.join(self.supported_providers)}")
        return adapter_cls()

    def build_prompt_for_task(self, task_id: str) -> PromptRequest:
        task = self.loader.load_task(task_id)
        return PromptBuilder.build(task)

    @staticmethod
    def _normalize_provider_response(raw_response: Any, *, task: BenchmarkTask) -> dict[str, Any]:
        required_fields = list(task.response_schema.get("required_fields", []))
        payload: dict[str, Any]
        if isinstance(raw_response, str):
            try:
                payload = json.loads(raw_response)
            except json.JSONDecodeError as exc:
                raise InvalidProviderResponseError(f"Provider returned a non-JSON string for task {task.task_id}: {exc.msg}") from exc
        elif isinstance(raw_response, Mapping):
            payload = dict(raw_response)
        else:
            raise InvalidProviderResponseError(f"Provider returned an unsupported response type for task {task.task_id}: {type(raw_response).__name__}")

        if "response" in payload and isinstance(payload["response"], Mapping):
            nested = dict(payload["response"])
            payload = {**payload, **nested}
        if not isinstance(payload, dict):
            raise InvalidProviderResponseError(f"Provider response for task {task.task_id} is not a JSON object.")
        missing = [field for field in required_fields if field not in payload]
        if missing:
            raise InvalidProviderResponseError(
                f"Provider response for task {task.task_id} is missing required fields: {', '.join(missing)}"
            )
        return payload

    def _execute_with_retries(
        self,
        prompt: PromptRequest,
        *,
        settings: ExecutionSettings,
        trial: int,
    ) -> tuple[ExecutionRecord, Any]:
        adapter = self._provider_for(settings.provider)
        last_error: Exception | None = None
        for attempt in range(1, settings.max_retries + 2):
            started_at = self._utc_now()
            try:
                started_ms = time.time_ns() // 1_000_000
                raw_response, provider_metadata = adapter.execute(prompt, settings=settings, trial=trial, attempt=attempt)
                structured_response = self._normalize_provider_response(raw_response, task=prompt.task)
                completed_at = self._utc_now()
                latency_ms = max(0, (time.time_ns() // 1_000_000) - started_ms)
                normalized_response = dict(structured_response)
                if "status" not in normalized_response:
                    normalized_response["status"] = "success"
                if "task_id" not in normalized_response:
                    normalized_response["task_id"] = prompt.task.task_id
                if "task_instance_id" not in normalized_response:
                    normalized_response["task_instance_id"] = prompt.task.task_instance_id
                record = ExecutionRecord(
                    run_id=settings.run_id,
                    task_id=prompt.task.task_id,
                    task_instance_id=prompt.task.task_instance_id,
                    provider=settings.provider,
                    model_id=settings.model_id,
                    trial=trial,
                    attempt=attempt,
                    started_at=started_at,
                    completed_at=completed_at,
                    status="success",
                    prompt=prompt.prompt_payload,
                    raw_response=raw_response,
                    structured_response=normalized_response,
                    provider_metadata=provider_metadata,
                    metadata={"temperature": settings.temperature, "max_output_tokens": settings.max_output_tokens, "timeout_seconds": settings.timeout_seconds},
                    latency_ms=latency_ms,
                    token_usage=provider_metadata.get("usage", {}),
                )
                return record, normalized_response
            except TransientProviderError as exc:
                last_error = exc
                if attempt >= settings.max_retries + 1:
                    break
                delay_seconds = min(0.25 * 2 ** (attempt - 1), 2.0)
                time.sleep(delay_seconds)
            except ProviderConfigurationError:
                raise
            except (ModelExecutionError, InvalidProviderResponseError) as exc:
                last_error = exc
                break
        record = ExecutionRecord(
            run_id=settings.run_id,
            task_id=prompt.task.task_id,
            task_instance_id=prompt.task.task_instance_id,
            provider=settings.provider,
            model_id=settings.model_id,
            trial=trial,
            attempt=attempt,
            started_at=self._utc_now(),
            completed_at=self._utc_now(),
            status="failed",
            prompt=prompt.prompt_payload,
            error=str(last_error) if last_error is not None else "Model execution failed.",
            metadata={"temperature": settings.temperature, "max_output_tokens": settings.max_output_tokens, "timeout_seconds": settings.timeout_seconds},
        )
        raise ModelExecutionError(record.error)

    def execute_task(
        self,
        task_id: str,
        *,
        provider: str | None = None,
        model_id: str | None = None,
        temperature: float = 0.0,
        max_output_tokens: int = 512,
        timeout_seconds: float = 30.0,
        trial_count: int = 1,
        max_retries: int = 2,
        seed: int | None = None,
        dry_run: bool = True,
        metadata: Mapping[str, Any] | None = None,
    ) -> list[ExecutionRecord]:
        task = self.loader.load_task(task_id)
        provider_name = (provider or os.environ.get("SURVEYML_PROVIDER", "mock")).strip().lower()
        resolved_model_id = model_id or os.environ.get("SURVEYML_MODEL", f"{provider_name}-model")
        settings = ExecutionSettings(
            provider=provider_name,
            model_id=resolved_model_id,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            timeout_seconds=timeout_seconds,
            trial_count=trial_count,
            max_retries=max_retries,
            seed=seed,
            dry_run=dry_run,
            metadata=dict(metadata or {}),
        )
        records: list[ExecutionRecord] = []
        for trial in range(1, trial_count + 1):
            prompt = PromptBuilder.build(task)
            record, _ = self._execute_with_retries(prompt, settings=settings, trial=trial)
            records.append(record)
        return records

    def execute_all_tasks(
        self,
        *,
        task_ids: Sequence[str] | None = None,
        provider: str | None = None,
        model_id: str | None = None,
        temperature: float = 0.0,
        max_output_tokens: int = 512,
        timeout_seconds: float = 30.0,
        trial_count: int = 1,
        max_retries: int = 2,
        seed: int | None = None,
        dry_run: bool = True,
        metadata: Mapping[str, Any] | None = None,
    ) -> dict[str, list[ExecutionRecord]]:
        tasks = self.loader.filter_tasks(task_ids=list(task_ids) if task_ids is not None else None)
        results: dict[str, list[ExecutionRecord]] = {}
        for task in tasks:
            results[task.task_id] = self.execute_task(
                task.task_id,
                provider=provider,
                model_id=model_id,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                timeout_seconds=timeout_seconds,
                trial_count=trial_count,
                max_retries=max_retries,
                seed=seed,
                dry_run=dry_run,
                metadata=metadata,
            )
        return results


__all__ = [
    "AnthropicAdapter",
    "ExecutionRecord",
    "ExecutionSettings",
    "GoogleGenerativeAdapter",
    "MockModelProviderAdapter",
    "ModelExecutionEngine",
    "ModelExecutionError",
    "ModelProviderAdapter",
    "OpenAICompatibleAdapter",
    "PromptBuilder",
    "PromptRequest",
    "ProviderConfigurationError",
    "TransientProviderError",
    "InvalidProviderResponseError",
]
