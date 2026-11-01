from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from surveymleval.engine import EvaluationEngine, TaskLoader, TaskValidationError

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_task_loader_loads_all_eight_task_families() -> None:
    loader = TaskLoader(REPO_ROOT)
    tasks = loader.load_all_tasks()
    task_ids = [task.task_id for task in tasks]
    assert task_ids == sorted(task_ids)
    assert task_ids == ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08"]
    assert len(tasks) == 8
    assert {task.task_family for task in tasks} == {
        "survey_design",
        "survey_weighted_prediction",
        "data_leakage",
        "validation_strategy",
        "class_imbalance",
        "external_validation",
        "missing_data",
        "calibration_interpretability",
    }


def test_task_loader_filters_and_orders_deterministically() -> None:
    loader = TaskLoader(REPO_ROOT)
    by_family = loader.filter_tasks(task_family="survey_design")
    by_ids = loader.filter_tasks(task_ids=["T08", "T01"])
    by_difficulty = loader.filter_tasks(difficulty="intermediate")

    assert [task.task_id for task in by_family] == ["T01"]
    assert [task.task_id for task in by_ids] == ["T01", "T08"]
    assert {task.task_id for task in by_difficulty} == {"T01", "T04"}


def test_task_loader_returns_public_task_views_without_hidden_reference() -> None:
    loader = TaskLoader(REPO_ROOT)
    public = loader.public_task_view("T03")
    assert "hidden_reference" not in public
    assert public["task_id"] == "T03"
    assert public["dataset_refs"][0]["path"] == "data/synthetic/DS-02/preprocessing_leakage.csv"
    assert "grading_mode" not in public
    assert "must_identify" not in public


def test_task_loader_validates_missing_files_and_invalid_ids() -> None:
    loader = TaskLoader(REPO_ROOT)

    with pytest.raises(TaskValidationError, match="Unknown task_id"):
        loader.load_task("T99")

    with pytest.raises(TaskValidationError, match="Missing task manifest"):
        TaskLoader(REPO_ROOT / "missing-root").load_task("T01")


def test_task_loader_rejects_malformed_or_protected_input_schema() -> None:
    with tempfile.TemporaryDirectory(dir=str(REPO_ROOT)) as tmpdir:
        root = Path(tmpdir) / "bench"
        root.mkdir()
        (root / "tasks").mkdir()
        (root / "reference_answers").mkdir()
        (root / "tasks" / "T01").mkdir()
        (root / "reference_answers" / "T01").mkdir()

        task_payload = {
            "benchmark_id": "SurveyML-Eval",
            "benchmark_version": "1.0.0",
            "task_id": "T01",
            "task_instance_id": "T01-001",
            "title": "Broken task",
            "task_family": "survey_design",
            "difficulty": "invalid",
            "dataset_refs": [{"dataset_id": "DS-01", "path": "data/synthetic/DS-01/core_sample.csv", "purpose": "bad"}],
            "model_visible_input": {"allowed_columns": ["outcome"], "description": "bad"},
            "response_schema": {"required_fields": ["answer"]},
            "provenance": {"source": "x"},
        }
        (root / "tasks" / "T01" / "task_instance.json").write_text(json.dumps(task_payload), encoding="utf-8")
        (root / "tasks" / "manifest.json").write_text(json.dumps({"benchmark_id": "SurveyML-Eval", "task_count": 1, "tasks": [{"task_id": "T01", "task_instance_id": "T01-001", "title": "Broken task", "task_family": "survey_design", "difficulty": "invalid", "dataset_refs": [{"dataset_id": "DS-01", "path": "data/synthetic/DS-01/core_sample.csv", "purpose": "bad"}]}]}), encoding="utf-8")
        (root / "reference_answers" / "T01" / "reference_answer.json").write_text(json.dumps({"task_id": "T01", "task_instance_id": "T01-001"}), encoding="utf-8")

        with pytest.raises(TaskValidationError):
            TaskLoader(root).load_task("T01")


def test_evaluation_engine_reports_execution_plan_and_task_count() -> None:
    engine = EvaluationEngine(REPO_ROOT)
    plan = engine.build_execution_plan(task_ids=["T01", "T08"])
    assert engine.task_count == 8
    assert [item["task_id"] for item in plan] == ["T01", "T08"]
    assert engine.public_model_task("T01")["task_id"] == "T01"
    assert engine.hidden_reference("T01")["task_id"] == "T01"
