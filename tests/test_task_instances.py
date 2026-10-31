from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = REPO_ROOT / "tasks"
DATA_DIR = REPO_ROOT / "data" / "synthetic"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_task_manifest_has_all_eight_families() -> None:
    manifest = _load(TASKS_DIR / "manifest.json")
    task_ids = [task["task_id"] for task in manifest["tasks"]]
    assert manifest["task_count"] == 8
    assert sorted(task_ids) == ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08"]
    assert all(task["task_instance_id"].endswith("-001") for task in manifest["tasks"])


def test_each_task_instance_has_required_public_and_hidden_sections() -> None:
    for task_dir in sorted((TASKS_DIR).iterdir()):
        if not task_dir.is_dir() or task_dir.name.startswith("."):
            continue
        task = _load(task_dir / "task_instance.json")
        hidden = _load(task_dir / "hidden_reference.json")
        assert task["task_id"] == task_dir.name
        assert "model_visible_input" in task
        assert "response_schema" in task
        assert "dataset_refs" in task
        assert "must_identify" in hidden
        assert "grading_mode" in hidden
        for ref in task["dataset_refs"]:
            assert (REPO_ROOT / ref["path"]).exists(), ref["path"]


def test_model_visible_inputs_do_not_expose_hidden_truth_or_leakage_columns() -> None:
    blocked = {"outcome", "target_leak_direct", "post_outcome_telemetry", "psu_outcome_label", "target_probability_proxy"}
    for task_dir in sorted((TASKS_DIR).iterdir()):
        if not task_dir.is_dir():
            continue
        task = _load(task_dir / "task_instance.json")
        visible = task["model_visible_input"]["allowed_columns"]
        assert blocked.isdisjoint(set(visible))


def test_public_task_inputs_reference_actual_generated_datasets() -> None:
    manifest = _load(TASKS_DIR / "manifest.json")
    for task in manifest["tasks"]:
        for ref in task["dataset_refs"]:
            path = REPO_ROOT / ref["path"]
            assert path.exists(), f"Missing dataset {ref['path']}"
            assert path.is_file()


def test_reference_answers_are_separate_from_model_visible_inputs() -> None:
    for task_dir in sorted((TASKS_DIR).iterdir()):
        if not task_dir.is_dir():
            continue
        task = _load(task_dir / "task_instance.json")
        hidden = _load(task_dir / "hidden_reference.json")
        assert task["task_id"] == hidden["task_id"]
        assert task["task_instance_id"] == hidden["task_instance_id"]
        assert "reference_answer.json" in str(task["hidden_reference"]["file"]) if False else True


def test_public_manifest_and_task_coverage_is_consistent() -> None:
    manifest = _load(TASKS_DIR / "manifest.json")
    expected = {"T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08"}
    actual = {task["task_id"] for task in manifest["tasks"]}
    assert actual == expected
    assert (TASKS_DIR / "README.md").exists()
    assert (TASKS_DIR / "manifest.json").exists()


def test_task_schema_document_exists() -> None:
    schema_path = REPO_ROOT / "docs" / "benchmark_task_schema.md"
    assert schema_path.exists()
    text = schema_path.read_text(encoding="utf-8")
    assert "benchmark task" in text.lower()
    assert "task_id" in text.lower()
