from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd

from surveymleval.config import (
    CLEAN_MODEL_COLUMNS,
    EXPECTED_CORE_SAMPLE_SIZE,
    MASTER_SEED,
    MAX_PSU_SIZE,
    MIN_PSU_SIZE,
    NUM_STRATA,
    PSUS_PER_STRATUM,
    SELECTED_PSUS_PER_STRATUM,
    TARGET_PREVALENCE,
    UNITS_PER_SELECTED_PSU,
)


def sigmoid(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-x))


def _logit(p: float) -> float:
    p = float(np.clip(p, 1e-8, 1.0 - 1e-8))
    return np.log(p / (1.0 - p))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")


def _variable_dictionary() -> Dict[str, Any]:
    return {
        "respondent_id": {"role": "identifier", "type": "string", "description": "Unique respondent identifier within the benchmark dataset."},
        "stratum_id": {"role": "survey_design", "type": "categorical", "description": "Synthetic sampling stratum identifier.", "categories": [f"STR-{i:02d}" for i in range(1, NUM_STRATA + 1)]},
        "psu_id": {"role": "survey_design", "type": "identifier", "description": "Synthetic primary sampling unit identifier."},
        "age": {"role": "feature", "type": "integer", "description": "Age in years.", "range": [18, 85]},
        "sex": {"role": "feature", "type": "categorical", "description": "Binary sex assignment.", "categories": ["female", "male"]},
        "education_level": {"role": "feature", "type": "categorical", "description": "Education category.", "categories": ["none", "primary", "secondary", "tertiary"]},
        "wealth_index": {"role": "feature", "type": "float", "description": "Synthetic socioeconomic ranking on a latent scale.", "range": [-3.0, 3.0]},
        "residence_type": {"role": "feature", "type": "categorical", "description": "Urban-rural residence type.", "categories": ["rural", "urban"]},
        "employment_status": {"role": "feature", "type": "categorical", "description": "Employment status category.", "categories": ["unemployed", "employed", "student", "retired"]},
        "household_size": {"role": "feature", "type": "integer", "description": "Household size.", "range": [1, 12]},
        "media_access": {"role": "feature", "type": "binary", "description": "Access to media or information resources (1=yes)."},
        "health_access": {"role": "feature", "type": "binary", "description": "Access to health services (1=yes)."},
        "outcome": {"role": "target", "type": "binary", "description": "Synthetic binary outcome used for predictive tasks.", "values": [0, 1]},
        "survey_weight": {"role": "survey_design", "type": "float", "description": "Inverse-probability weight from the two-stage stratified design.", "positive": True},
        "pi1": {"role": "survey_design", "type": "float", "description": "First-stage inclusion probability of the selected PSU."},
        "pi2": {"role": "survey_design", "type": "float", "description": "Second-stage inclusion probability for each sampled unit within a selected PSU."},
        "pi": {"role": "survey_design", "type": "float", "description": "Overall inclusion probability."},
        "base_weight": {"role": "survey_design", "type": "float", "description": "Base inverse-probability weight computed as 1/pi."},
    }


class RandomStreams:
    def __init__(self, master_seed: int = MASTER_SEED) -> None:
        root = np.random.SeedSequence(master_seed)
        seeds = root.spawn(8)
        self.population = np.random.default_rng(seeds[0])
        self.sample = np.random.default_rng(seeds[1])
        self.leakage = np.random.default_rng(seeds[2])
        self.missingness = np.random.default_rng(seeds[3])
        self.imbalance = np.random.default_rng(seeds[4])
        self.external = np.random.default_rng(seeds[5])
        self.validation = np.random.default_rng(seeds[6])
        self.audit = np.random.default_rng(seeds[7])


def _education_code(level: str) -> int:
    mapping = {"none": 0, "primary": 1, "secondary": 2, "tertiary": 3}
    return mapping[level]


def _education_from_latent(value: float) -> str:
    if value < -0.85:
        return "none"
    if value < 0.10:
        return "primary"
    if value < 1.25:
        return "secondary"
    return "tertiary"


def _employment_from_covariates(age: int, wealth: float, education_level: str, sex: str, rng: np.random.Generator) -> str:
    if age < 22:
        if rng.random() < 0.6:
            return "student"
        return "unemployed"
    if age >= 65:
        if rng.random() < 0.5:
            return "retired"
        return "unemployed"
    if wealth > 0.6 and education_level in {"secondary", "tertiary"}:
        if rng.random() < 0.8:
            return "employed"
    if rng.random() < 0.55:
        return "employed"
    return "unemployed"


def _binary_from_prob(p: float, rng: np.random.Generator) -> int:
    return int(rng.random() < p)


def _calibrate_logistic_intercept(linear_component: np.ndarray, target_prevalence: float) -> float:
    low, high = -20.0, 20.0
    for _ in range(200):
        mid = 0.5 * (low + high)
        mean_prob = float(sigmoid(mid + linear_component).mean())
        if mean_prob < target_prevalence:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)


def generate_finite_population(seed: int = MASTER_SEED, *, return_metadata: bool = False) -> pd.DataFrame | Tuple[pd.DataFrame, Dict[str, Any]]:
    rng = np.random.default_rng(seed)
    rows: List[Dict[str, Any]] = []
    expected_prevalence = TARGET_PREVALENCE
    for stratum_num in range(1, NUM_STRATA + 1):
        stratum_label = f"STR-{stratum_num:02d}"
        stratum_effect = rng.normal(loc=(stratum_num - 4.5) * 0.22, scale=0.7)
        for psu_num in range(1, PSUS_PER_STRATUM + 1):
            psu_size = int(rng.integers(MIN_PSU_SIZE, MAX_PSU_SIZE + 1))
            psu_effect = rng.normal(loc=stratum_effect, scale=0.65)
            for _ in range(psu_size):
                age = int(np.clip(round(rng.normal(loc=44 + stratum_effect * 10.0, scale=15.0), 0), 18, 85))
                sex = "male" if rng.random() < 0.52 else "female"
                wealth_index = float(rng.normal(loc=0.15 * stratum_num + psu_effect, scale=1.1))
                residence_type = "urban" if rng.random() < (0.32 + 0.08 * (stratum_num >= 5) + 0.10 * (wealth_index > 0.5)) else "rural"
                media_access = int(rng.random() < (0.52 + 0.22 * (residence_type == "urban") + 0.18 * (wealth_index > 0.2)))
                health_access = int(rng.random() < (0.48 + 0.18 * (residence_type == "urban") + 0.16 * (wealth_index > 0.0)))
                education_latent = 0.9 * wealth_index + 0.12 * (age >= 35) + rng.normal(0.0, 0.95) - 0.25 * (sex == "male")
                education_level = _education_from_latent(education_latent)
                employment_status = _employment_from_covariates(age=age, wealth=wealth_index, education_level=education_level, sex=sex, rng=rng)
                household_size = int(np.clip(round(rng.poisson(lam=4.0 + 0.25 * (stratum_num - 1) + max(0.0, wealth_index)), 0), 1, 12))
                rows.append(
                    {
                        "dataset_id": "DS-01",
                        "respondent_id": f"DS01-{stratum_label}-{psu_num:02d}-{len(rows) + 1:05d}",
                        "stratum_id": stratum_label,
                        "psu_id": f"{stratum_label}-PSU-{psu_num:02d}",
                        "age": age,
                        "sex": sex,
                        "education_level": education_level,
                        "wealth_index": wealth_index,
                        "residence_type": residence_type,
                        "employment_status": employment_status,
                        "household_size": household_size,
                        "media_access": media_access,
                        "health_access": health_access,
                    }
                )

    population = pd.DataFrame(rows)
    education_map = {k: _education_code(k) for k in ["none", "primary", "secondary", "tertiary"]}
    population["education_code"] = population["education_level"].map(education_map)
    population["wealth_z"] = (population["wealth_index"] - population["wealth_index"].mean()) / (population["wealth_index"].std(ddof=1) or 1.0)
    population["age_z"] = (population["age"] - population["age"].mean()) / (population["age"].std(ddof=1) or 1.0)
    population["household_size_z"] = (population["household_size"] - population["household_size"].mean()) / (population["household_size"].std(ddof=1) or 1.0)
    population["sex_male"] = (population["sex"] == "male").astype(int)
    population["urban"] = (population["residence_type"] == "urban").astype(int)
    population["employed"] = (population["employment_status"] == "employed").astype(int)

    linear_component = (
        -0.18
        + 0.85 * population["wealth_z"]
        + 0.42 * population["age_z"]
        + 0.58 * population["urban"]
        + 0.80 * population["media_access"]
        + 1.00 * population["health_access"]
        + 0.36 * population["sex_male"]
        + 0.42 * population["education_code"]
        + 0.22 * population["household_size_z"]
        + 0.24 * population["employed"]
    )
    intercept = _calibrate_logistic_intercept(linear_component.to_numpy(), expected_prevalence)
    population["linear_predictor"] = linear_component
    population["outcome_probability"] = sigmoid(intercept + linear_component)
    population["outcome"] = [int(v) for v in rng.binomial(1, population["outcome_probability"].to_numpy())]
    population["population_prevalence"] = expected_prevalence
    population["source_type"] = "synthetic"
    population["sample_stage"] = "finite_population"
    population["sampled"] = 0
    population["survey_weight"] = np.nan
    population["pi1"] = np.nan
    population["pi2"] = np.nan
    population["pi"] = np.nan
    population["base_weight"] = np.nan
    population = population[[
        "dataset_id",
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
        "outcome",
        "survey_weight",
        "pi1",
        "pi2",
        "pi",
        "base_weight",
        "population_prevalence",
        "source_type",
        "sample_stage",
        "sampled",
        "linear_predictor",
        "outcome_probability",
    ]]
    if return_metadata:
        metadata = {
            "dataset_id": "DS-01",
            "dataset_name": "Core Synthetic Survey Population",
            "purpose": "Finite population used for survey design, two-stage sampling, and predictive benchmarking.",
            "n_strata": NUM_STRATA,
            "psus_per_stratum": PSUS_PER_STRATUM,
            "expected_prevalence": expected_prevalence,
            "population_record_count": int(len(population)),
            "seed": seed,
            "sampling_design": {
                "type": "two_stage_stratified_cluster_sampling",
                "first_stage_psu_selection": {
                    "m_h": SELECTED_PSUS_PER_STRATUM,
                    "M_h": PSUS_PER_STRATUM,
                    "pi1": SELECTED_PSUS_PER_STRATUM / PSUS_PER_STRATUM,
                },
                "second_stage_unit_selection": {
                    "units_per_selected_psu": UNITS_PER_SELECTED_PSU,
                },
            },
        }
        return population, metadata
    return population


def generate_core_sample(population: pd.DataFrame, seed: int = MASTER_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    selected_rows: List[Dict[str, Any]] = []
    for stratum_label, stratum_df in population.groupby("stratum_id", sort=True):
        psu_ids = sorted(stratum_df["psu_id"].unique())
        chosen_psus = rng.choice(psu_ids, size=SELECTED_PSUS_PER_STRATUM, replace=False)
        for psu_id in chosen_psus:
            psu_df = stratum_df[stratum_df["psu_id"] == psu_id].copy()
            n_hj = len(psu_df)
            sampled_psu = psu_df.sample(n=UNITS_PER_SELECTED_PSU, replace=False, random_state=int(rng.integers(0, 1_000_000_000)))
            pi1 = SELECTED_PSUS_PER_STRATUM / PSUS_PER_STRATUM
            pi2 = UNITS_PER_SELECTED_PSU / n_hj
            pi = pi1 * pi2
            sampled_psu["pi1"] = pi1
            sampled_psu["pi2"] = pi2
            sampled_psu["pi"] = pi
            sampled_psu["base_weight"] = 1.0 / pi
            sampled_psu["survey_weight"] = sampled_psu["base_weight"]
            sampled_psu["sampled"] = 1
            sampled_psu["sample_stage"] = "selected_sample"
            selected_rows.append(sampled_psu)

    sample = pd.concat(selected_rows, ignore_index=True)
    sample["dataset_id"] = "DS-01"
    sample["respondent_id"] = sample["respondent_id"].str.replace("DS01-", "DS01-SAMPLE-")
    sample["source_type"] = "synthetic"
    sample["sampled"] = 1
    sample["survey_weight"] = sample["base_weight"].astype(float)
    sample["outcome_probability"] = np.nan
    sample["linear_predictor"] = np.nan
    sample = sample[[
        col for col in CLEAN_MODEL_COLUMNS if col in sample.columns
    ] + [
        c for c in [
            "pi1",
            "pi2",
            "pi",
            "base_weight",
            "population_prevalence",
            "source_type",
            "sample_stage",
            "sampled",
            "linear_predictor",
            "outcome_probability",
        ] if c in sample.columns
    ]]
    if len(sample) != EXPECTED_CORE_SAMPLE_SIZE:
        raise ValueError(f"Expected {EXPECTED_CORE_SAMPLE_SIZE} records but generated {len(sample)}.")
    return sample


def _write_dataset_csv(path: Path, df: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def _build_manifest(base_dir: Path) -> Dict[str, Any]:
    manifest_rows: List[Dict[str, Any]] = []
    for path in sorted(base_dir.rglob("*.csv")):
        relative = path.relative_to(base_dir).as_posix()
        manifest_rows.append({"path": relative, "sha256": _sha256(path), "bytes": path.stat().st_size})
    for path in sorted(base_dir.rglob("*.json")):
        relative = path.relative_to(base_dir).as_posix()
        if relative.endswith("manifest.json"):
            continue
        manifest_rows.append({"path": relative, "sha256": _sha256(path), "bytes": path.stat().st_size})
    return {"files": sorted(manifest_rows, key=lambda item: item["path"])}


def _prepare_leakage_views(sample: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    direct = sample.copy()
    direct["target_leak_direct"] = direct["outcome"]
    direct["target_probability_proxy"] = direct["survey_weight"] * (1.0 + direct["outcome"])
    direct["outcome_rank"] = direct["outcome"].rank(method="first")

    identifier_leak = sample.copy()
    identifier_leak["respondent_id_hash"] = identifier_leak["respondent_id"].str.slice(stop=12) + "-leak"
    identifier_leak["psu_outcome_label"] = identifier_leak["psu_id"] + "|" + identifier_leak["outcome"].astype(str)

    preprocessing = sample.copy()
    preprocessing["employment_outcome_mean"] = preprocessing.groupby("employment_status")["outcome"].transform("mean")
    preprocessing["wealth_outcome_ratio"] = preprocessing["wealth_index"] * preprocessing["outcome"]

    post_outcome = sample.copy()
    post_outcome["post_outcome_telemetry"] = post_outcome["outcome"].map({0: "no_event", 1: "event"})
    post_outcome["post_outcome_flag"] = post_outcome["outcome"] + (post_outcome["health_access"] * 2)
    post_outcome["feature_after_target"] = post_outcome["wealth_index"] + 0.5 * post_outcome["outcome"]

    return {
        "direct_target_leakage": direct,
        "identifier_leakage": identifier_leak,
        "preprocessing_leakage": preprocessing,
        "post_outcome_information": post_outcome,
    }


def _add_missingness(df: pd.DataFrame, mechanism: str, dropout_rate: float, rng: np.random.Generator) -> pd.DataFrame:
    result = df.copy()
    if mechanism == "MCAR":
        missing_probability = np.full(len(result), dropout_rate, dtype=float)
    elif mechanism == "MAR":
        score = -0.9 + 1.5 * (result["wealth_index"] > 0.0).astype(float) + 1.2 * result["media_access"] + 0.8 * (result["residence_type"] == "urban")
        missing_probability = np.clip(sigmoid(score) * (dropout_rate / 0.55), 0.0, 1.0)
    elif mechanism == "MNAR":
        score = -1.7 + 2.4 * result["outcome"].astype(float) + 0.9 * (result["health_access"] == 1).astype(float)
        missing_probability = np.clip(sigmoid(score) * (dropout_rate / 0.45), 0.0, 1.0)
    else:
        raise ValueError(f"Unknown missing-data mechanism: {mechanism}")

    mask = rng.random(len(result)) < missing_probability
    result.loc[mask, "health_access"] = np.nan
    result.loc[mask, "media_access"] = np.nan
    result["missingness_mechanism"] = mechanism
    result["missingness_rate"] = dropout_rate
    return result


def generate_ds03(sample: pd.DataFrame, output_dir: Path) -> Dict[str, str]:
    file_map: Dict[str, str] = {}
    mechanisms = ["MCAR", "MAR", "MNAR"]
    rates = [0.05, 0.10, 0.20, 0.30]
    for mechanism in mechanisms:
        for rate in rates:
            name = f"{mechanism.lower()}_{int(rate * 100):02d}pct.csv"
            path = output_dir / name
            df = _add_missingness(sample, mechanism, rate, rng=np.random.default_rng(MASTER_SEED + 99 + len(file_map)))
            _write_dataset_csv(path, df)
            file_map[name] = str(path)

    for target_share in [0.40, 0.20, 0.10, 0.05]:
        positive = sample[sample["outcome"] == 1].copy()
        negative = sample[sample["outcome"] == 0].copy()
        target_positive_count = int(round(len(sample) * target_share))
        take_positive_with_replacement = target_positive_count > len(positive)
        take_negative_with_replacement = (len(sample) - target_positive_count) > len(negative)
        selected_positive = positive.sample(n=target_positive_count, replace=take_positive_with_replacement, random_state=MASTER_SEED + 1000)
        selected_negative = negative.sample(n=len(sample) - target_positive_count, replace=take_negative_with_replacement, random_state=MASTER_SEED + 2000)
        imbalance_df = pd.concat([selected_positive, selected_negative], ignore_index=True)
        imbalance_df["class_imbalance_target_rate"] = target_share
        path = output_dir / f"class_imbalance_{int(target_share * 100):02d}pct.csv"
        _write_dataset_csv(path, imbalance_df)
        file_map[f"class_imbalance_{int(target_share * 100):02d}pct.csv"] = str(path)
    return file_map


def generate_ds02(sample: pd.DataFrame, output_dir: Path) -> Dict[str, str]:
    file_map: Dict[str, str] = {}
    views = _prepare_leakage_views(sample)
    for name, df in views.items():
        filename = f"{name}.csv"
        path = output_dir / filename
        _write_dataset_csv(path, df)
        file_map[filename] = str(path)
    return file_map


def generate_external_population(seed: int = MASTER_SEED + 10) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows: List[Dict[str, Any]] = []
    for stratum_num in range(1, NUM_STRATA + 1):
        stratum_label = f"EXT-STR-{stratum_num:02d}"
        for psu_num in range(1, PSUS_PER_STRATUM + 1):
            psu_size = int(rng.integers(180, 320))
            for _ in range(psu_size):
                age = int(np.clip(round(rng.normal(loc=52 + 3 * (stratum_num - 1), scale=16.0), 0), 18, 85))
                sex = "male" if rng.random() < 0.54 else "female"
                wealth_index = float(rng.normal(loc=0.75 + 0.18 * stratum_num, scale=1.1))
                residence_type = "urban" if rng.random() < (0.58 + 0.10 * (stratum_num >= 5)) else "rural"
                media_access = int(rng.random() < (0.72 + 0.10 * (residence_type == "urban") + 0.10 * (wealth_index > 0.5)))
                health_access = int(rng.random() < (0.66 + 0.12 * (residence_type == "urban") + 0.10 * (wealth_index > 0.3)))
                education_latent = 1.1 * wealth_index + 0.14 * (age >= 35) + rng.normal(0.0, 0.9)
                education_level = _education_from_latent(education_latent)
                employment_status = _employment_from_covariates(age=age, wealth=wealth_index, education_level=education_level, sex=sex, rng=rng)
                household_size = int(np.clip(round(rng.poisson(lam=4.5 + 0.18 * stratum_num), 0), 1, 12))
                rows.append(
                    {
                        "dataset_id": "DS-04",
                        "respondent_id": f"DS04-{stratum_label}-{psu_num:02d}-{len(rows) + 1:05d}",
                        "stratum_id": stratum_label,
                        "psu_id": f"{stratum_label}-PSU-{psu_num:02d}",
                        "age": age,
                        "sex": sex,
                        "education_level": education_level,
                        "wealth_index": wealth_index,
                        "residence_type": residence_type,
                        "employment_status": employment_status,
                        "household_size": household_size,
                        "media_access": media_access,
                        "health_access": health_access,
                    }
                )

    population = pd.DataFrame(rows)
    education_map = {k: _education_code(k) for k in ["none", "primary", "secondary", "tertiary"]}
    population["education_code"] = population["education_level"].map(education_map)
    population["wealth_z"] = (population["wealth_index"] - population["wealth_index"].mean()) / (population["wealth_index"].std(ddof=1) or 1.0)
    population["age_z"] = (population["age"] - population["age"].mean()) / (population["age"].std(ddof=1) or 1.0)
    population["household_size_z"] = (population["household_size"] - population["household_size"].mean()) / (population["household_size"].std(ddof=1) or 1.0)
    population["sex_male"] = (population["sex"] == "male").astype(int)
    population["urban"] = (population["residence_type"] == "urban").astype(int)
    population["employed"] = (population["employment_status"] == "employed").astype(int)

    linear_component = (
        -0.20
        + 1.10 * population["wealth_z"]
        + 0.60 * population["age_z"]
        + 0.35 * population["urban"]
        + 0.52 * population["media_access"]
        + 0.88 * population["health_access"]
        + 0.45 * population["sex_male"]
        + 0.50 * population["education_code"]
        + 0.25 * population["household_size_z"]
        + 0.30 * population["employed"]
    )
    external_prevalence = 0.38
    intercept = _logit(external_prevalence) - float(linear_component.mean())
    population["linear_predictor"] = linear_component
    population["outcome_probability"] = sigmoid(intercept + linear_component)
    population["outcome"] = [int(v) for v in rng.binomial(1, population["outcome_probability"].to_numpy())]
    population["population_prevalence"] = external_prevalence
    population["survey_weight"] = np.nan
    population["pi1"] = np.nan
    population["pi2"] = np.nan
    population["pi"] = np.nan
    population["base_weight"] = np.nan
    population["source_type"] = "synthetic_external"
    population["sample_stage"] = "finite_population"
    population["sampled"] = 0
    return population


def generate_external_validation_sample(external_population: pd.DataFrame, seed: int = MASTER_SEED + 11) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = 3000
    sample = external_population.sample(n=n, replace=False, random_state=int(rng.integers(1_000_000)))
    sample = sample.copy()
    selection_prob = n / len(external_population)
    sample["survey_weight"] = 1.0 / selection_prob
    sample["pi1"] = selection_prob
    sample["pi2"] = 1.0
    sample["pi"] = selection_prob
    sample["base_weight"] = sample["survey_weight"]
    sample["sample_stage"] = "external_validation"
    sample["sampled"] = 1
    return sample


def _dataset_provenance() -> Dict[str, Any]:
    return {
        "project": "SurveyML-Eval",
        "checkpoint": "CP-07C",
        "status": "implemented",
        "master_seed": MASTER_SEED,
        "description": "All datasets are synthetic and designed for benchmark development and validation only.",
        "assumptions": [
            "Finite population is generated before sample selection.",
            "Two-stage stratified cluster sampling uses 8 strata and 20 PSUs per stratum.",
            "The selected sample takes 10 PSUs per stratum and 125 units per selected PSU.",
            "All inclusion probabilities and weights are computed from actual finite-population units.",
            "The synthetic outcome prevalence is a calibrated design parameter and not a real-world empirical estimate.",
        ],
        "known_design_limits": [
            "This benchmark uses synthetic populations and does not represent a real country survey.",
            "The external population is intentionally independent of the development population.",
            "Missing data and distribution-shift scenarios are synthetic and controlled.",
        ],
    }


def generate_all(output_root: Path | str = "data/synthetic") -> Dict[str, Any]:
    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    population, pop_meta = generate_finite_population(seed=MASTER_SEED, return_metadata=True)
    sample = generate_core_sample(population, seed=MASTER_SEED)
    ds01_dir = root / "DS-01"
    ds01_dir.mkdir(parents=True, exist_ok=True)
    _write_dataset_csv(ds01_dir / "finite_population.csv", population)
    _write_dataset_csv(ds01_dir / "core_sample.csv", sample)
    write_json(ds01_dir / "dataset_metadata.json", pop_meta)
    write_json(ds01_dir / "variable_dictionary.json", _variable_dictionary())

    ds02_dir = root / "DS-02"
    ds02_dir.mkdir(parents=True, exist_ok=True)
    ds02_files = generate_ds02(sample, ds02_dir)
    write_json(ds02_dir / "metadata.json", {"scenarios": {k: str(v) for k, v in ds02_files.items()}, "description": "Controlled leakage scenarios."})

    ds03_dir = root / "DS-03"
    ds03_dir.mkdir(parents=True, exist_ok=True)
    ds03_files = generate_ds03(sample, ds03_dir)
    write_json(ds03_dir / "metadata.json", {
        "missingness_scenarios": {k: str(v) for k, v in ds03_files.items() if "class_imbalance" not in k},
        "class_imbalance_scenarios": {k: str(v) for k, v in ds03_files.items() if "class_imbalance" in k},
        "rates": [0.05, 0.10, 0.20, 0.30],
        "target_prevalence_levels": [0.40, 0.20, 0.10, 0.05],
    })

    external_population = generate_external_population(seed=MASTER_SEED + 13)
    external_sample = generate_external_validation_sample(external_population, seed=MASTER_SEED + 17)
    ds04_dir = root / "DS-04"
    ds04_dir.mkdir(parents=True, exist_ok=True)
    _write_dataset_csv(ds04_dir / "external_population.csv", external_population)
    _write_dataset_csv(ds04_dir / "external_validation_sample.csv", external_sample)
    write_json(ds04_dir / "metadata.json", {
        "dataset_id": "DS-04",
        "description": "Independent external survey population and validation sample.",
        "covariate_shift": {
            "age_mean_shift": 7.0,
            "wealth_mean_shift": 0.75,
            "urban_rate_shift": 0.20,
            "media_access_shift": 0.18,
            "health_access_shift": 0.15,
        },
        "prevalence_shift": {"development_prevalence": TARGET_PREVALENCE, "external_prevalence": float(external_population["outcome"].mean())},
        "concept_shift": {
            "wealth_coefficient_increase": 0.25,
            "media_access_efficiency_change": -0.28,
            "target_name": "synthetic_binary_outcome",
        },
        "sample_size": int(len(external_sample)),
    })

    root_manifest = root / "manifest.json"
    manifest = _build_manifest(root)
    write_json(root_manifest, manifest)

    provenance = _dataset_provenance()
    write_json(root / "metadata" / "provenance.json", provenance)
    manifest = _build_manifest(root)
    write_json(root_manifest, manifest)
    provenance["generated_files"] = manifest["files"]
    write_json(root / "metadata" / "provenance.json", provenance)
    manifest = _build_manifest(root)
    write_json(root_manifest, manifest)
    return {
        "population": population,
        "sample": sample,
        "external_population": external_population,
        "external_sample": external_sample,
        "manifest": manifest,
    }


def main() -> None:
    generate_all()


if __name__ == "__main__":
    main()
