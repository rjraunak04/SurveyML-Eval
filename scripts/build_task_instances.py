from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from surveymleval.tasks import build_task_manifest


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_task_files(repo_root: Path | str = ".") -> None:
    root = Path(repo_root).resolve()
    manifest = build_task_manifest(root)
    tasks_dir = root / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)

    for task in manifest["tasks"]:
        task_dir = tasks_dir / task["task_id"]
        task_dir.mkdir(parents=True, exist_ok=True)
        task_payload = {
            "benchmark_id": task["benchmark_id"],
            "benchmark_version": task["benchmark_version"],
            "task_id": task["task_id"],
            "task_instance_id": task["task_instance_id"],
            "title": task["title"],
            "task_family": task["task_family"],
            "difficulty": task["difficulty"],
            "dataset_refs": task["dataset_refs"],
            "model_visible_input": task["model_visible_input"],
            "response_schema": task["response_schema"],
            "prompt": {
                "text": (
                    f"You are given a synthetic benchmark task for {task['title']}. "
                    f"Use only the public model-visible data. Do not expose hidden answers, leakage labels, or protected outcome columns. "
                    f"Return JSON matching the required response schema."
                ),
                "required_fields": task["response_schema"]["required_fields"],
            },
            "provenance": task["provenance"],
        }
        write_json(task_dir / "task_instance.json", task_payload)

        hidden_reference = {
            "task_id": task["task_id"],
            "task_instance_id": task["task_instance_id"],
            "title": task["title"],
            "must_identify": task["hidden_reference"]["must_identify"],
            "grading_mode": task["hidden_reference"]["grading_mode"],
            "exposure_policy": "Never expose this reference in model-facing inputs.",
        }
        write_json(task_dir / "hidden_reference.json", hidden_reference)

        ref_dir = root / "reference_answers" / task["task_id"]
        ref_dir.mkdir(parents=True, exist_ok=True)
        write_json(ref_dir / "reference_answer.json", hidden_reference)

    write_json(tasks_dir / "manifest.json", manifest)

    readme = [
        "# Benchmark task instances",
        "",
        f"This repository contains {manifest['task_count']} benchmark task instances for the approved CP-08 task families.",
        "",
        "## Task families",
        "",
    ]
    for task in manifest["tasks"]:
        readme.append(f"- {task['task_id']}: {task['title']} ({task['difficulty']})")
    (tasks_dir / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    reference_readme = [
        "# Reference answers",
        "",
        "Reference answers are stored separately from model-visible task inputs and must never be exposed to benchmark models.",
    ]
    (root / "reference_answers" / "README.md").write_text("\n".join(reference_readme) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build_task_files()
