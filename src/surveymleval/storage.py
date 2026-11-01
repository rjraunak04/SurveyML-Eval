from __future__ import annotations

import json
import os
import tempfile
import uuid
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Mapping, Sequence

if TYPE_CHECKING:
    from .execution import ExecutionRecord


class ResponseStorageError(ValueError):
    """Raised when response storage or experiment metadata is invalid."""


_FORBIDDEN_TEXT_SNIPPETS = (
    "hidden_reference",
    "must_identify",
    "protected outcome columns",
    "target_probability_proxy",
    "post_outcome_telemetry",
    "psu_outcome_label",
    "target_leak_direct",
    "api_key",
    "authorization",
    "secret",
    "password",
    "bearer ",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sanitize_secret_keys(value: Any) -> Any:
    if isinstance(value, Mapping):
        cleaned: dict[str, Any] = {}
        for key, item in value.items():
            lowered = str(key).lower()
            if any(token in lowered for token in ("api_key", "apikey", "token", "secret", "password", "authorization", "cookie", "bearer")):
                continue
            cleaned[str(key)] = _sanitize_secret_keys(item)
        return cleaned
    if isinstance(value, list):
        return [_sanitize_secret_keys(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_sanitize_secret_keys(item) for item in value)
    return value


def _contains_forbidden_material(value: Any) -> bool:
    if value is None:
        return False
    text = json.dumps(value, sort_keys=True)
    lowered = text.lower()
    return any(snippet in lowered for snippet in _FORBIDDEN_TEXT_SNIPPETS)


@dataclass(frozen=True)
class ExperimentManifest:
    experiment_id: str
    benchmark_id: str
    benchmark_version: str
    created_at: str
    provider: str
    model_id: str
    model_version: str | None = None
    task_family: str | None = None
    task_ids: tuple[str, ...] = ()
    trial_count: int = 1
    seed: int | None = None
    settings: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    runs: tuple[dict[str, Any], ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "benchmark_id": self.benchmark_id,
            "benchmark_version": self.benchmark_version,
            "created_at": self.created_at,
            "provider": self.provider,
            "model_id": self.model_id,
            "model_version": self.model_version,
            "task_family": self.task_family,
            "task_ids": list(self.task_ids),
            "trial_count": self.trial_count,
            "seed": self.seed,
            "settings": self.settings,
            "metadata": self.metadata,
            "runs": [dict(run) for run in self.runs],
        }


class ResponseStorage:
    """Persist raw model responses and execution metadata in a versioned results tree."""

    def __init__(self, repo_root: str | os.PathLike[str] | None = None) -> None:
        root = Path(repo_root).resolve() if repo_root is not None else Path(__file__).resolve().parents[2]
        self.repo_root = root
        self.results_root = self.repo_root / "results"
        self.raw_outputs_root = self.results_root / "raw_outputs"
        self.experiments_root = self.results_root / "experiments"
        self.logs_root = self.results_root / "execution_logs"

    def _ensure_dirs(self) -> None:
        self.raw_outputs_root.mkdir(parents=True, exist_ok=True)
        self.experiments_root.mkdir(parents=True, exist_ok=True)
        self.logs_root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _safe_json_value(value: Any) -> Any:
        return _sanitize_secret_keys(value)

    @staticmethod
    def _record_key(record: Mapping[str, Any]) -> str:
        return str(record.get("run_id") or record.get("execution_id") or record.get("task_id") or "unknown")

    def _atomic_write_json(self, path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
        self._ensure_dirs()
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
        try:
            with os.fdopen(temp_fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, sort_keys=True)
                handle.write("\n")
            os.replace(temp_name, path)
        except Exception:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:
                pass
            raise

    def _read_json_if_present(self, path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, dict):
            raise ResponseStorageError(f"Expected a JSON object in {path}.")
        return data

    def _manifest_path(self, experiment_id: str) -> Path:
        return self.experiments_root / experiment_id / "manifest.json"

    def _record_path(self, task_id: str, run_id: str) -> Path:
        return self.raw_outputs_root / task_id / f"{run_id}.json"

    def create_experiment(
        self,
        experiment_id: str | None = None,
        *,
        benchmark_id: str = "SurveyML-Eval",
        benchmark_version: str = "1.0.0",
        provider: str = "mock",
        model_id: str = "mock-model",
        model_version: str | None = None,
        task_family: str | None = None,
        task_ids: Sequence[str] | None = None,
        trial_count: int = 1,
        seed: int | None = None,
        settings: Mapping[str, Any] | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        resolved_experiment_id = str(experiment_id or f"EXP-{uuid.uuid4().hex[:12]}").strip()
        if not resolved_experiment_id:
            raise ResponseStorageError("experiment_id must not be empty.")
        existing = self._read_json_if_present(self._manifest_path(resolved_experiment_id))
        manifest = existing or {
            "experiment_id": resolved_experiment_id,
            "benchmark_id": benchmark_id,
            "benchmark_version": benchmark_version,
            "created_at": _utc_now(),
            "provider": provider,
            "model_id": model_id,
            "model_version": model_version,
            "task_family": task_family,
            "task_ids": list(task_ids or []),
            "trial_count": int(trial_count),
            "seed": seed,
            "settings": dict(settings or {}),
            "metadata": dict(metadata or {}),
            "runs": [],
        }
        manifest["experiment_id"] = resolved_experiment_id
        manifest["benchmark_id"] = benchmark_id
        manifest["benchmark_version"] = benchmark_version
        manifest["provider"] = provider
        manifest["model_id"] = model_id
        if model_version is not None:
            manifest["model_version"] = model_version
        if task_family is not None:
            manifest["task_family"] = task_family
        if task_ids is not None:
            manifest["task_ids"] = [str(item) for item in task_ids]
        manifest["trial_count"] = int(trial_count)
        manifest["seed"] = seed
        manifest["settings"] = self._safe_json_value(dict(settings or {}))
        manifest["metadata"] = self._safe_json_value(dict(metadata or {}))
        manifest["created_at"] = manifest.get("created_at") or _utc_now()
        manifest["runs"] = list(manifest.get("runs", []))
        self._atomic_write_json(self._manifest_path(resolved_experiment_id), manifest)
        return manifest

    def _load_experiment_manifest(self, experiment_id: str | None) -> dict[str, Any]:
        if not experiment_id:
            return {}
        manifest = self._read_json_if_present(self._manifest_path(experiment_id))
        if manifest is None:
            return {}
        return manifest

    def _validate_record(self, record: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(record, Mapping):
            raise ResponseStorageError("Execution record must be a mapping.")
        required = ["run_id", "task_id", "task_instance_id", "provider", "model_id", "status"]
        missing = [field for field in required if not record.get(field)]
        if missing:
            raise ResponseStorageError(f"Execution record is missing required fields: {', '.join(missing)}")
        if _contains_forbidden_material(record):
            raise ResponseStorageError("Execution record contains hidden benchmark material or secrets and cannot be persisted.")
        if "api_key" in str(record):
            raise ResponseStorageError("Execution record includes API credential material and cannot be persisted.")
        return dict(record)

    def persist_execution(
        self,
        record: "ExecutionRecord" | Mapping[str, Any],
        *,
        experiment_id: str | None = None,
    ) -> dict[str, Any]:
        from .execution import ExecutionRecord

        if isinstance(record, ExecutionRecord):
            payload = dict(record.as_dict())
        else:
            payload = dict(record)
        payload.setdefault("execution_status", "completed" if payload.get("status") == "success" else payload.get("status", "failed"))
        payload.setdefault("started_at", _utc_now())
        payload.setdefault("completed_at", _utc_now())
        payload["metadata"] = self._safe_json_value(dict(payload.get("metadata") or {}))
        if experiment_id:
            payload["metadata"]["experiment_id"] = str(experiment_id)
        elif payload.get("metadata", {}).get("experiment_id"):
            experiment_id = str(payload["metadata"]["experiment_id"])
        if not experiment_id:
            experiment_id = payload.get("metadata", {}).get("experiment_id") or "EXP-default"
        payload = self._validate_record(payload)
        payload["metadata"] = self._safe_json_value(payload.get("metadata") or {})
        payload["provider_metadata"] = self._safe_json_value(payload.get("provider_metadata") or {})
        payload["token_usage"] = self._safe_json_value(payload.get("token_usage") or {})
        payload["structured_response"] = self._safe_json_value(payload.get("structured_response") or {})
        payload["prompt"] = self._safe_json_value(payload.get("prompt") or {})
        payload["raw_response"] = self._safe_json_value(payload.get("raw_response"))
        payload["execution_status"] = "completed" if payload.get("status") == "success" else payload.get("status", "failed")
        if not payload.get("run_id"):
            payload["run_id"] = str(uuid.uuid4())

        run_id = str(payload["run_id"])
        task_id = str(payload["task_id"])
        task_path = self._record_path(task_id, run_id)
        if task_path.exists():
            existing = json.loads(task_path.read_text(encoding="utf-8"))
            if existing.get("run_id") == run_id:
                return existing

        self._atomic_write_json(task_path, payload)

        manifest = self.create_experiment(
            experiment_id,
            benchmark_id=str(payload.get("benchmark_id") or "SurveyML-Eval"),
            benchmark_version=str(payload.get("benchmark_version") or "1.0.0"),
            provider=str(payload.get("provider") or "mock"),
            model_id=str(payload.get("model_id") or "mock-model"),
            model_version=(payload.get("provider_metadata") or {}).get("model_version") or (payload.get("metadata") or {}).get("model_version"),
            task_family=str(payload.get("task_family") or payload.get("metadata", {}).get("task_family") or "unknown"),
            task_ids=[task_id],
            trial_count=int((payload.get("metadata") or {}).get("trial_count") or 1),
            seed=(payload.get("metadata") or {}).get("seed"),
            settings=self._safe_json_value((payload.get("metadata") or {}).get("settings") or {}),
            metadata={
                **(self._safe_json_value((payload.get("metadata") or {}) or {})),
                "task_instance_id": payload.get("task_instance_id"),
                "run_id": run_id,
            },
        )
        manifest_data = self._read_json_if_present(self._manifest_path(experiment_id)) or manifest
        runs = list(manifest_data.get("runs", []))
        run_entry = {
            "run_id": run_id,
            "task_id": task_id,
            "task_instance_id": payload.get("task_instance_id"),
            "status": payload.get("status", "failed"),
            "execution_status": payload.get("execution_status"),
            "started_at": payload.get("started_at"),
            "completed_at": payload.get("completed_at"),
            "trial": payload.get("trial"),
            "attempt": payload.get("attempt"),
            "provider": payload.get("provider"),
            "model_id": payload.get("model_id"),
            "response_path": str(task_path.relative_to(self.repo_root)),
        }
        if not any(existing_entry.get("run_id") == run_id for existing_entry in runs):
            runs.append(run_entry)
        manifest_data["runs"] = runs
        manifest_data["task_ids"] = sorted({str(item) for item in manifest_data.get("task_ids", []) + [task_id]})
        self._atomic_write_json(self._manifest_path(str(experiment_id)), manifest_data)
        return payload

    def list_experiments(self) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        for path in sorted(self.experiments_root.glob("*/manifest.json")):
            manifest = self._read_json_if_present(path)
            if manifest:
                items.append(manifest)
        return items

    def list_records(
        self,
        *,
        experiment_id: str | None = None,
        task_family: str | None = None,
        task_id: str | None = None,
        provider: str | None = None,
        model_id: str | None = None,
        trial: int | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        matches: list[dict[str, Any]] = []
        for path in sorted(self.raw_outputs_root.glob("**/*.json")):
            if path.name.startswith("."):
                continue
            with path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            if not isinstance(data, dict):
                continue
            metadata = data.get("metadata") or {}
            if experiment_id and str(metadata.get("experiment_id") or "").strip() != str(experiment_id).strip():
                continue
            if task_id and str(data.get("task_id") or "").strip() != str(task_id).strip():
                continue
            if provider and str(data.get("provider") or "").strip().lower() != str(provider).strip().lower():
                continue
            if model_id and str(data.get("model_id") or "").strip() != str(model_id).strip():
                continue
            if trial is not None and int(data.get("trial") or -1) != int(trial):
                continue
            if status and str(data.get("status") or "").strip().lower() != str(status).strip().lower():
                continue
            if task_family:
                task_family_value = str(metadata.get("task_family") or "")
                if task_family_value != str(task_family):
                    continue
            matches.append(data)
        return matches

    def load_record(self, run_id: str) -> dict[str, Any]:
        for entry in self.list_records():
            if str(entry.get("run_id") or "") == str(run_id):
                return entry
        raise ResponseStorageError(f"No persisted record found for run_id {run_id!r}.")

    def raw_output_path(self, task_id: str, run_id: str) -> Path:
        return self._record_path(str(task_id), str(run_id))


__all__ = [
    "ExperimentManifest",
    "ResponseStorage",
    "ResponseStorageError",
]
