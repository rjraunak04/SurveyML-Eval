"""Configuration and constants for the SurveyML-Eval synthetic generator."""

MASTER_SEED = 42
TARGET_PREVALENCE = 0.27
NUM_STRATA = 8
PSUS_PER_STRATUM = 20
SELECTED_PSUS_PER_STRATUM = 10
UNITS_PER_SELECTED_PSU = 125
MIN_PSU_SIZE = 180
MAX_PSU_SIZE = 320
EXPECTED_CORE_SAMPLE_SIZE = NUM_STRATA * SELECTED_PSUS_PER_STRATUM * UNITS_PER_SELECTED_PSU
CLEAN_MODEL_COLUMNS = [
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
]
