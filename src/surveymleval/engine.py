from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


class TaskValidationError(ValueError):
    """Raised when a task manifest, task definition, or dataset reference is invalid."""


VALID_DIFFICULTIES = {"intermediate", "advanced"}
PROTECTED_COLUMNS = {
    "outcome",
    "target_leak_direct",
    "post_outcome_telemetry",
    "psu_outcome_label",
    "target_probability_proxy",
}


@dataclass(frozen=True)
class DatasetReference:
    dataset_id: str
    path: str
    purpose: str
    exists: bool = True
    sha256: str | None = None

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "DatasetReference":
        if not isinstance(mapping, Mapping):
            raise TaskValidationError("Dataset reference must be an object.")
        dataset_id = str(mapping.get("dataset_id", "")).strip()
        path = str(mapping.get("path", "")).strip()
        purpose = str(mapping.get("purpose", "")).strip()
        exists = bool(mapping.get("exists", True))
        sha256 = mapping.get("sha256")
        if not dataset_id:
            raise TaskValidationError("Dataset reference is missing a dataset_id.")
        if not path:
            raise TaskValidationError(f"Dataset {dataset_id!r} is missing a path.")
        if not purpose:
            raise TaskValidationError(f"Dataset {dataset_id!r} is missing a purpose.")
        return cls(dataset_id=dataset_id, path=path, purpose=purpose, exists=exists, sha256=sha256 if sha256 is not None else None)

    def as_dict(self) -> dict[str, Any]:
        payload = {
            "dataset_id": self.dataset_id,
            "path": self.path,
            "purpose": self.purpose,
            "exists": self.exists,
        }
        if self.sha256 is not None:
            payload["sha256"] = self.sha256
        return payload


@dataclass(frozen=True)
class BenchmarkTask:
    benchmark_id: str
    benchmark_version: str
    task_id: str
    task_instance_id: str
    title: str
    task_family: str
    difficulty: str
    dataset_refs: tuple[DatasetReference, ...]
    model_visible_input: dict[str, Any]
    hidden_reference: dict[str, Any]
    response_schema: dict[str, Any]
    provenance: dict[str, Any]
    prompt: dict[str, Any] = field(default_factory=dict)

    def public_payload(self) -> dict[str, Any]:
        payload = {
            "benchmark_id": self.benchmark_id,
            "benchmark_version": self.benchmark_version,
            "task_id": self.task_id,
            "task_instance_id": self.task_instance_id,
            "title": self.title,
            "task_family": self.task_family,
            "difficulty": self.difficulty,
            "dataset_refs": [ref.as_dict() for ref in self.dataset_refs],
            "model_visible_input": self.model_visible_input,
            "response_schema": self.response_schema,
            "provenance": self.provenance,
        }
        if self.prompt:
            payload["prompt"] = self.prompt
        return payload


class TaskLoader:
    """Loads and validates benchmark tasks from the repository task manifests and task files."""

    def __init__(self, repo_root: str | Path | None = None) -> None:
        self.repo_root = Path(repo_root).resolve() if repo_root is not None else Path(__file__).resolve().parents[2]
        self.tasks_root = self.repo_root / "tasks"
        self.reference_root = self.repo_root / "reference_answers"
        self.manifest_path = self.tasks_root / "manifest.json"

    def _read_json(self, file_path: Path, *, description: str) -> Any:
        try:
            with file_path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError as exc:  # pragma: no cover - validated by callers
            raise TaskValidationError(f"Missing {description}: {file_path}") from exc
        except json.JSONDecodeError as exc:
            raise TaskValidationError(f"Malformed JSON in {description}: {file_path}: {exc.msg}") from exc

    def _validate_manifest(self, manifest: Mapping[str, Any]) -> dict[str, Any]:
        tasks = manifest.get("tasks")
        if not isinstance(tasks, list):
            raise TaskValidationError("Task manifest is missing the 'tasks' list.")
        seen_ids: set[str] = set()
        for entry in tasks:
            if not isinstance(entry, Mapping):
                raise TaskValidationError("Each task manifest entry must be an object.")
            task_id = str(entry.get("task_id", "")).strip()
            if not task_id:
                raise TaskValidationError("Task manifest contains a task with no task_id.")
            if task_id in seen_ids:
                raise TaskValidationError(f"Duplicate task_id in manifest: {task_id}")
            seen_ids.add(task_id)
            if not str(entry.get("task_instance_id", "")).strip():
                raise TaskValidationError(f"Task {task_id} is missing a task_instance_id.")
            if not str(entry.get("title", "")).strip():
                raise TaskValidationError(f"Task {task_id} is missing a title.")
            task_family = str(entry.get("task_family", "")).strip()
            if not task_family:
                raise TaskValidationError(f"Task {task_id} is missing a task_family.")
            difficulty = str(entry.get("difficulty", "")).strip()
            if difficulty not in VALID_DIFFICULTIES:
                raise TaskValidationError(
                    f"Task {task_id} has invalid difficulty {difficulty!r}; expected one of {sorted(VALID_DIFFICULTIES)}."
                )
            dataset_refs = entry.get("dataset_refs")
            if not isinstance(dataset_refs, list) or not dataset_refs:
                raise TaskValidationError(f"Task {task_id} must include at least one dataset_ref.")
            for ref in dataset_refs:
                DatasetReference.from_mapping(ref)
        return dict(manifest)

    def load_manifest(self) -> dict[str, Any]:
        manifest = self._read_json(self.manifest_path, description="task manifest")
        if not isinstance(manifest, dict):
            raise TaskValidationError("Task manifest must contain a JSON object.")
        return self._validate_manifest(manifest)

    def _validate_task_payload(self, task_payload: Mapping[str, Any], *, expected_id: str) -> None:
        if task_payload.get("task_id") != expected_id:
            raise TaskValidationError(f"Task file for {expected_id!r} declares task_id {task_payload.get('task_id')!r}.")
        task_instance_id = str(task_payload.get("task_instance_id", "")).strip()
        if not task_instance_id:
            raise TaskValidationError(f"Task {expected_id!r} is missing task_instance_id.")
        if not task_instance_id.startswith(f"{expected_id}-"):
            raise TaskValidationError(f"Task {expected_id!r} has mismatched task_instance_id {task_instance_id!r}.")
        difficulty = str(task_payload.get("difficulty", "")).strip()
        if difficulty not in VALID_DIFFICULTIES:
            raise TaskValidationError(f"Task {expected_id!r} has unsupported difficulty {difficulty!r}.")
        dataset_refs = task_payload.get("dataset_refs")
        if not isinstance(dataset_refs, list) or not dataset_refs:
            raise TaskValidationError(f"Task {expected_id!r} must list dataset_refs.")
        for ref in dataset_refs:
            dataset_ref = DatasetReference.from_mapping(ref)
            dataset_path = self.repo_root / dataset_ref.path
            if not dataset_path.exists():
                raise TaskValidationError(f"Task {expected_id!r} references missing dataset file: {dataset_ref.path}")
        model_visible = task_payload.get("model_visible_input")
        if not isinstance(model_visible, Mapping):
            raise TaskValidationError(f"Task {expected_id!r} is missing model_visible_input.")
        allowed_columns = model_visible.get("allowed_columns")
        if not isinstance(allowed_columns, list):
            raise TaskValidationError(f"Task {expected_id!r} model_visible_input is missing allowed_columns.")
        if set(PROTECTED_COLUMNS).intersection(allowed_columns):
            raise TaskValidationError(f"Task {expected_id!r} exposes protected columns in model_visible_input.")
        response_schema = task_payload.get("response_schema")
        if not isinstance(response_schema, Mapping):
            raise TaskValidationError(f"Task {expected_id!r} is missing response_schema.")
        required_fields = response_schema.get("required_fields")
        if not isinstance(required_fields, list) or not required_fields:
            raise TaskValidationError(f"Task {expected_id!r} response_schema is missing required_fields.")

    def _load_hidden_reference(self, task_id: str) -> dict[str, Any]:
        if not task_id:
            raise TaskValidationError("A task_id is required to load a hidden reference.")
        file_path = self.reference_root / task_id / "reference_answer.json"
        payload = self._read_json(file_path, description=f"hidden reference for {task_id}")
        if not isinstance(payload, dict):
            raise TaskValidationError(f"Hidden reference for {task_id!r} must be a JSON object.")
        if payload.get("task_id") not in {None, task_id}:
            raise TaskValidationError(f"Hidden reference for {task_id!r} declares a mismatched task_id.")
        if payload.get("task_instance_id") and not str(payload.get("task_instance_id", "")).startswith(f"{task_id}-"):
            raise TaskValidationError(f"Hidden reference for {task_id!r} has a malformed task_instance_id.")
        return payload

    def load_task(self, task_id: str) -> BenchmarkTask:
        task_id = str(task_id).strip()
        if not task_id:
            raise TaskValidationError("task_id must not be empty.")
        manifest = self.load_manifest()
        entries = [entry for entry in manifest["tasks"] if str(entry.get("task_id", "")).strip() == task_id]
        if not entries:
            raise TaskValidationError(f"Unknown task_id: {task_id}")
        if len(entries) > 1:
            raise TaskValidationError(f"Duplicate task_id in manifest: {task_id}")
        task_path = self.tasks_root / task_id / "task_instance.json"
        try:
            task_payload = self._read_json(task_path, description=f"task instance for {task_id}")
        except TaskValidationError:
            raise
        if not isinstance(task_payload, dict):
            raise TaskValidationError(f"Task {task_id!r} task_instance.json must contain a JSON object.")
        self._validate_task_payload(task_payload, expected_id=task_id)
        hidden_reference = self._load_hidden_reference(task_id)
        prompt = task_payload.get("prompt", {})
        if not isinstance(prompt, Mapping):
            raise TaskValidationError(f"Task {task_id!r} has a malformed prompt block.")
        return BenchmarkTask(
            benchmark_id=str(task_payload.get("benchmark_id", "SurveyML-Eval")),
            benchmark_version=str(task_payload.get("benchmark_version", "1.0.0")),
            task_id=str(task_payload["task_id"]),
            task_instance_id=str(task_payload["task_instance_id"]),
            title=str(task_payload.get("title", task_id)),
            task_family=str(task_payload.get("task_family", "unknown")),
            difficulty=str(task_payload["difficulty"]),
            dataset_refs=tuple(DatasetReference.from_mapping(ref) for ref in task_payload["dataset_refs"]),
            model_visible_input=dict(task_payload["model_visible_input"]),
            hidden_reference=hidden_reference,
            response_schema=dict(task_payload["response_schema"]),
            provenance=dict(task_payload.get("provenance", {})),
            prompt=dict(prompt),
        )

    def load_all_tasks(self) -> list[BenchmarkTask]:
        manifest = self.load_manifest()
        task_ids = sorted({str(entry.get("task_id", "")).strip() for entry in manifest["tasks"] if str(entry.get("task_id", "")).strip()})
        return [self.load_task(task_id) for task_id in task_ids]

    def filter_tasks(
        self,
        *,
        task_ids: Sequence[str] | None = None,
        task_family: str | None = None,
        difficulty: str | None = None,
    ) -> list[BenchmarkTask]:
        tasks = self.load_all_tasks()
        selected = tasks
        if task_ids is not None:
            requested = {str(item).strip() for item in task_ids}
            selected = [task for task in selected if task.task_id in requested]
        if task_family is not None:
            selected = [task for task in selected if task.task_family == task_family]
        if difficulty is not None:
            selected = [task for task in selected if task.difficulty == difficulty]
        selected.sort(key=lambda task: (task.task_id, task.task_instance_id))
        return selected

    def public_task_view(self, task_id: str) -> dict[str, Any]:
        task = self.load_task(task_id)
        payload = task.public_payload()
        payload.pop("hidden_reference", None)
        return payload

    def load_dataset_for_task(self, task_id: str) -> dict[str, pd.DataFrame]:
        task = self.load_task(task_id)
        payload: dict[str, pd.DataFrame] = {}
        for ref in task.dataset_refs:
            dataset_path = self.repo_root / ref.path
            if not dataset_path.exists():
                raise TaskValidationError(f"Task {task_id!r} dataset reference is missing: {ref.path}")
            payload[ref.dataset_id] = pd.read_csv(dataset_path)
        return payload


class EvaluationEngine:
    """A thin, provider-independent benchmark execution facade for task selection and validation."""

    def __init__(self, repo_root: str | Path | None = None, task_loader: TaskLoader | None = None) -> None:
        self.loader = task_loader or TaskLoader(repo_root)

    @property
    def task_count(self) -> int:
        return len(self.loader.load_all_tasks())

    def available_task_ids(self) -> list[str]:
        return sorted(task.task_id for task in self.loader.load_all_tasks())

    def load_task(self, task_id: str) -> BenchmarkTask:
        return self.loader.load_task(task_id)

    def load_tasks(
        self,
        *,
        task_ids: Sequence[str] | None = None,
        task_family: str | None = None,
        difficulty: str | None = None,
    ) -> list[BenchmarkTask]:
        return self.loader.filter_tasks(task_ids=task_ids, task_family=task_family, difficulty=difficulty)

    def build_execution_plan(
        self,
        *,
        task_ids: Sequence[str] | None = None,
        task_family: str | None = None,
        difficulty: str | None = None,
    ) -> list[dict[str, Any]]:
        tasks = self.load_tasks(task_ids=task_ids, task_family=task_family, difficulty=difficulty)
        return [
            {
                "task_id": task.task_id,
                "task_instance_id": task.task_instance_id,
                "title": task.title,
                "task_family": task.task_family,
                "difficulty": task.difficulty,
                "dataset_refs": [ref.as_dict() for ref in task.dataset_refs],
            }
            for task in tasks
        ]

    def public_model_task(self, task_id: str) -> dict[str, Any]:
        return self.loader.public_task_view(task_id)

    def hidden_reference(self, task_id: str) -> dict[str, Any]:
        return self.loader._load_hidden_reference(task_id)


__all__ = [
    "BenchmarkTask",
    "DatasetReference",
    "EvaluationEngine",
    "TaskLoader",
    "TaskValidationError",
]
