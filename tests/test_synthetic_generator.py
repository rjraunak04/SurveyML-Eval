from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from surveymleval.config import EXPECTED_CORE_SAMPLE_SIZE
from surveymleval.generator import generate_all


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data" / "synthetic"


def test_synthetic_generator_outputs() -> None:
    results = generate_all(DATA_DIR)
    population = results["population"]
    sample = results["sample"]

    assert len(population) > 0
    assert population["stratum_id"].nunique() == 8
    assert population["psu_id"].nunique() == 160
    assert population["outcome"].isin([0, 1]).all()
    assert abs(population["outcome"].mean() - 0.27) < 0.08

    assert len(sample) == EXPECTED_CORE_SAMPLE_SIZE
    assert sample["stratum_id"].nunique() == 8
    stratum_psu_counts = sample.groupby(["stratum_id", "psu_id"]).size()
    assert stratum_psu_counts.groupby(level=0).count().eq(10).all()
    assert sample["survey_weight"].gt(0).all()
    assert sample["pi"].between(0.0, 1.0).all()
    assert sample["pi1"].nunique() == 1
    assert np.isclose(sample["pi1"].unique()[0], 0.5)
    assert sample["outcome"].isin([0, 1]).all()
    assert sample["age"].between(18, 85).all()
    assert sample["education_level"].isin(["none", "primary", "secondary", "tertiary"]).all()
    assert sample["base_weight"].gt(0).all()

    assert (DATA_DIR / "DS-01" / "finite_population.csv").exists()
    assert (DATA_DIR / "DS-01" / "core_sample.csv").exists()
    assert (DATA_DIR / "DS-02" / "direct_target_leakage.csv").exists()
    assert (DATA_DIR / "DS-02" / "identifier_leakage.csv").exists()
    assert (DATA_DIR / "DS-02" / "preprocessing_leakage.csv").exists()
    assert (DATA_DIR / "DS-02" / "post_outcome_information.csv").exists()
    assert (DATA_DIR / "DS-03" / "mcar_05pct.csv").exists()
    assert (DATA_DIR / "DS-03" / "mar_30pct.csv").exists()
    assert (DATA_DIR / "DS-03" / "mnar_20pct.csv").exists()
    assert (DATA_DIR / "DS-03" / "class_imbalance_05pct.csv").exists()
    assert (DATA_DIR / "DS-04" / "external_population.csv").exists()
    assert (DATA_DIR / "DS-04" / "external_validation_sample.csv").exists()

    manifest = json.loads((DATA_DIR / "manifest.json").read_text(encoding="utf-8"))
    assert "files" in manifest and len(manifest["files"]) > 0

    external_population = pd.read_csv(DATA_DIR / "DS-04" / "external_population.csv")
    external_sample = pd.read_csv(DATA_DIR / "DS-04" / "external_validation_sample.csv")
    assert external_population["outcome"].isin([0, 1]).all()
    assert len(external_population) > len(external_sample)
    assert external_sample["survey_weight"].gt(0).all()

    ds03_files = [DATA_DIR / "DS-03" / name for name in [
        "mcar_05pct.csv",
        "mcar_10pct.csv",
        "mcar_20pct.csv",
        "mcar_30pct.csv",
        "mar_05pct.csv",
        "mar_10pct.csv",
        "mar_20pct.csv",
        "mar_30pct.csv",
        "mnar_05pct.csv",
        "mnar_10pct.csv",
        "mnar_20pct.csv",
        "mnar_30pct.csv",
        "class_imbalance_40pct.csv",
        "class_imbalance_20pct.csv",
        "class_imbalance_10pct.csv",
        "class_imbalance_05pct.csv",
    ]]
    for path in ds03_files:
        assert path.exists(), f"Missing required file: {path.name}"


def test_generated_dataset_metadata_uses_repo_relative_paths() -> None:
    ds02_metadata = json.loads((DATA_DIR / "DS-02" / "metadata.json").read_text(encoding="utf-8"))
    ds03_metadata = json.loads((DATA_DIR / "DS-03" / "metadata.json").read_text(encoding="utf-8"))

    for mapping in (ds02_metadata["scenarios"], ds03_metadata["missingness_scenarios"], ds03_metadata["class_imbalance_scenarios"]):
        for value in mapping.values():
            path = Path(value)
            assert not path.is_absolute(), value
            assert (DATA_DIR / path).exists(), value
