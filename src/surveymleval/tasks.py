from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

TASK_FAMILY_SPECS: Dict[str, Dict[str, Any]] = {
    "T01": {
        "title": "Complex Survey Design and Weight Interpretation",
        "family": "survey_design",
        "difficulty": "intermediate",
        "datasets": [
            {
                "dataset_id": "DS-01",
                "path": "data/synthetic/DS-01/core_sample.csv",
                "purpose": "survey-design interpretation and weight reasoning",
            }
        ],
        "columns": [
            "respondent_id",
            "stratum_id",
            "psu_id",
            "age",
            "sex",
            "education_level",
            "wealth_index",
            "residence_type",
            "employment_status",
            "household_size",
            "media_access",
            "health_access",
            "survey_weight",
        ],
        "prompt_focus": "Explain the purpose of sampling weights, distinguish strata from PSUs, and recommend a design-aware analysis workflow.",
        "expected_response": [
            "weight_purpose",
            "strata_role",
            "psu_role",
            "variance_method",
            "target_population",
            "recommended_workflow",
        ],
        "hidden_reference": {
            "must_identify": [
                "sampling weights reflect unequal selection probabilities",
                "strata are sampling subdivisions",
                "PSUs are selected at the first-stage cluster sampling step",
                "variance estimation should respect clustering and stratification",
            ]
        },
    },
    "T02": {
        "title": "Survey-Weighted Predictive Modelling",
        "family": "survey_weighted_prediction",
        "difficulty": "advanced",
        "datasets": [
            {
                "dataset_id": "DS-01",
                "path": "data/synthetic/DS-01/core_sample.csv",
                "purpose": "population-relevant predictive modelling with survey weights",
            }
        ],
        "columns": [
            "age",
            "sex",
            "education_level",
            "wealth_index",
            "residence_type",
            "employment_status",
            "household_size",
            "media_access",
            "health_access",
            "survey_weight",
            "outcome",
        ],
        "prompt_focus": "Recommend a statistically defensible modelling strategy that distinguishes sampling weights from class weights and evaluation design.",
        "expected_response": [
            "target_population",
            "estimand",
            "modelling_strategy",
            "weight_handling",
            "evaluation_metrics",
            "uncertainty_method",
        ],
        "hidden_reference": {
            "must_identify": [
                "weights represent design inclusion probabilities, not class imbalance adjustments",
                "training and evaluation should remain separate",
                "weighted metrics and design-aware uncertainty are different concerns",
            ]
        },
    },
    "T03": {
        "title": "Data Leakage Detection and Prevention",
        "family": "data_leakage",
        "difficulty": "advanced",
        "datasets": [
            {
                "dataset_id": "DS-02",
                "path": "data/synthetic/DS-02/preprocessing_leakage.csv",
                "purpose": "leakage-aware validation and feature engineering",
            },
            {
                "dataset_id": "DS-02",
                "path": "data/synthetic/DS-02/direct_target_leakage.csv",
                "purpose": "target leakage detection",
            },
            {
                "dataset_id": "DS-02",
                "path": "data/synthetic/DS-02/identifier_leakage.csv",
                "purpose": "record identity leakage",
            },
        ],
        "columns": [
            "respondent_id",
            "stratum_id",
            "psu_id",
            "age",
            "sex",
            "wealth_index",
            "employment_status",
            "health_access",
            "outcome",
        ],
        "prompt_focus": "Identify the leakage mechanism, explain why it violates benchmark integrity, and specify how to fix the pipeline.",
        "expected_response": [
            "leakage_type",
            "why_unsafe",
            "correction",
            "train_test_boundary",
            "protected_columns",
        ],
        "hidden_reference": {
            "must_identify": [
                "outcome and post-outcome variables must never be used for prediction",
                "identifier fields and group labels can leak signal if not isolated",
                "preprocessing must occur within each training split only",
            ]
        },
    },
    "T04": {
        "title": "Validation Strategy Selection",
        "family": "validation_strategy",
        "difficulty": "intermediate",
        "datasets": [
            {
                "dataset_id": "DS-01",
                "path": "data/synthetic/DS-01/core_sample.csv",
                "purpose": "baseline validation design",
            },
            {
                "dataset_id": "DS-02",
                "path": "data/synthetic/DS-02/preprocessing_leakage.csv",
                "purpose": "wrong-validation-design example",
            },
        ],
        "columns": [
            "stratum_id",
            "psu_id",
            "survey_weight",
            "wealth_index",
            "media_access",
            "health_access",
            "outcome",
        ],
        "prompt_focus": "Choose a validation design that respects the survey structure and avoids leakage, with explicit reasoning about the target population.",
        "expected_response": [
            "validation_design",
            "leakage_check",
            "strata_psu_consideration",
            "reporting_plan",
        ],
        "hidden_reference": {
            "must_identify": [
                "validation must separate training and evaluation data",
                "survey design and leakage constraints should influence the design choice",
                "external validation is distinct from random split validation",
            ]
        },
    },
    "T05": {
        "title": "Class Imbalance and Performance Evaluation",
        "family": "class_imbalance",
        "difficulty": "advanced",
        "datasets": [
            {
                "dataset_id": "DS-03",
                "path": "data/synthetic/DS-03/class_imbalance_10pct.csv",
                "purpose": "classification performance under controlled imbalance",
            }
        ],
        "columns": [
            "age",
            "sex",
            "wealth_index",
            "residence_type",
            "media_access",
            "health_access",
            "survey_weight",
            "outcome",
        ],
        "prompt_focus": "Evaluate classification performance under a controlled imbalance regime and explain which metrics and threshold choices are defensible.",
        "expected_response": [
            "imbalance_summary",
            "metric_choice",
            "threshold_reasoning",
            "resampling_consideration",
        ],
        "hidden_reference": {
            "must_identify": [
                "class imbalance changes the meaning of raw accuracy",
                "precision-recall, balanced accuracy, and calibration should be considered explicitly",
                "thresholds and prevalence should be interpreted carefully",
            ]
        },
    },
    "T06": {
        "title": "External Validation and Distribution Shift",
        "family": "external_validation",
        "difficulty": "advanced",
        "datasets": [
            {
                "dataset_id": "DS-04",
                "path": "data/synthetic/DS-04/external_population.csv",
                "purpose": "development-population comparison",
            },
            {
                "dataset_id": "DS-04",
                "path": "data/synthetic/DS-04/external_validation_sample.csv",
                "purpose": "external validation sample",
            },
        ],
        "columns": [
            "age",
            "sex",
            "wealth_index",
            "residence_type",
            "media_access",
            "health_access",
            "outcome",
            "survey_weight",
        ],
        "prompt_focus": "Assess whether the model generalises to an external population with shifted covariate prevalence and concept relationships.",
        "expected_response": [
            "shift_summary",
            "external_validity",
            "prevalence_comparison",
            "recommendation",
        ],
        "hidden_reference": {
            "must_identify": [
                "external validation is distinct from internal validation",
                "covariate and outcome distribution shifts can change predictive performance",
                "one cannot assume the same model calibration holds under shift",
            ]
        },
    },
    "T07": {
        "title": "Missing Data and Statistical Uncertainty",
        "family": "missing_data",
        "difficulty": "advanced",
        "datasets": [
            {
                "dataset_id": "DS-03",
                "path": "data/synthetic/DS-03/mcar_10pct.csv",
                "purpose": "MCAR scenario",
            },
            {
                "dataset_id": "DS-03",
                "path": "data/synthetic/DS-03/mar_10pct.csv",
                "purpose": "MAR scenario",
            },
            {
                "dataset_id": "DS-03",
                "path": "data/synthetic/DS-03/mnar_10pct.csv",
                "purpose": "MNAR scenario",
            },
        ],
        "columns": [
            "age",
            "sex",
            "wealth_index",
            "residence_type",
            "media_access",
            "health_access",
            "outcome",
            "survey_weight",
        ],
        "prompt_focus": "Reason about the missing-data mechanism, explain how it changes the analysis, and recommend an appropriate uncertainty-aware strategy.",
        "expected_response": [
            "missingness_mechanism",
            "assumption_check",
            "imputation_or_analysis_choice",
            "uncertainty_recommendation",
        ],
        "hidden_reference": {
            "must_identify": [
                "MNAR depends on the underlying value before masking",
                "MCAR and MAR have different implications for missingness handling",
                "analysis should document assumptions and uncertainty propagation",
            ]
        },
    },
    "T08": {
        "title": "Model Calibration and Interpretability",
        "family": "calibration_interpretability",
        "difficulty": "advanced",
        "datasets": [
            {
                "dataset_id": "DS-01",
                "path": "data/synthetic/DS-01/core_sample.csv",
                "purpose": "calibration assessment on development sample",
            },
            {
                "dataset_id": "DS-04",
                "path": "data/synthetic/DS-04/external_validation_sample.csv",
                "purpose": "calibration comparison under external shift",
            },
        ],
        "columns": [
            "age",
            "sex",
            "wealth_index",
            "residence_type",
            "media_access",
            "health_access",
            "survey_weight",
            "outcome",
        ],
        "prompt_focus": "Assess calibration, interpretability, and whether model explanations can be treated as causal effects or only descriptive associations.",
        "expected_response": [
            "calibration_summary",
            "calibration_method",
            "interpretability_method",
            "causal_limitation",
        ],
        "hidden_reference": {
            "must_identify": [
                "AUC and calibration are different properties",
                "recalibration should be fit on a dev set, not the test set",
                "SHAP values explain predictive contributions, not causal effects",
            ]
        },
    },
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _dataset_checksums(root: Path) -> Dict[str, str]:
    checksums: Dict[str, str] = {}
    for path in sorted((root / "data" / "synthetic").rglob("*.*")):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            checksums[rel] = _sha256(path)
    return checksums


def build_task_manifest(repo_root: Path | str = ".") -> Dict[str, Any]:
    root = Path(repo_root).resolve()
    data_root = root / "data" / "synthetic"
    checksums = _dataset_checksums(root)
    tasks: List[Dict[str, Any]] = []

    for task_id, spec in sorted(TASK_FAMILY_SPECS.items()):
        task_instance_id = f"{task_id}-001"
        datasets = []
        for dataset in spec["datasets"]:
            rel_path = dataset["path"]
            file_path = root / rel_path
            dataset_record = {
                "dataset_id": dataset["dataset_id"],
                "path": rel_path,
                "sha256": checksums.get(rel_path, ""),
                "purpose": dataset["purpose"],
                "exists": file_path.exists(),
            }
            datasets.append(dataset_record)

        public_columns = [
            column
            for column in spec["columns"]
            if column not in {"outcome", "target_leak_direct", "post_outcome_telemetry", "psu_outcome_label", "target_probability_proxy"}
        ]
        task = {
            "benchmark_id": "SurveyML-Eval",
            "benchmark_version": "1.0.0",
            "task_id": task_id,
            "task_instance_id": task_instance_id,
            "title": spec["title"],
            "task_family": spec["family"],
            "difficulty": spec["difficulty"],
            "model_visible_input": {
                "description": spec["prompt_focus"],
                "reference_files": [d["path"] for d in datasets],
                "allowed_columns": public_columns,
                "protected_columns": ["outcome", "target_leak_direct", "post_outcome_telemetry", "psu_outcome_label", "target_probability_proxy"],
                "inputs_are_public": True,
            },
            "hidden_reference": {
                "file": f"reference_answers/{task_id}/reference_answer.json",
                "must_identify": spec["hidden_reference"]["must_identify"],
                "grading_mode": "reference_and_human_review",
            },
            "response_schema": {
                "required_fields": spec["expected_response"],
                "output_format": "JSON object",
                "strictly_public": True,
            },
            "dataset_refs": datasets,
            "provenance": {
                "source": "synthetic benchmark generator",
                "checkpoint": "CP-08",
                "master_seed": 42,
                "generated_datasets": [d["path"] for d in datasets],
            },
        }
        tasks.append(task)

    return {
        "benchmark_id": "SurveyML-Eval",
        "benchmark_version": "1.0.0",
        "task_count": len(tasks),
        "tasks": tasks,
    }


def list_task_ids() -> Iterable[str]:
    return list(TASK_FAMILY_SPECS)
