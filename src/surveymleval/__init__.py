"""SurveyML-Eval benchmark package."""

from .engine import BenchmarkTask, DatasetReference, EvaluationEngine, TaskLoader, TaskValidationError
from .execution import (
    AnthropicAdapter,
    ExecutionRecord,
    ExecutionSettings,
    GoogleGenerativeAdapter,
    InvalidProviderResponseError,
    MockModelProviderAdapter,
    ModelExecutionEngine,
    ModelExecutionError,
    ModelProviderAdapter,
    OpenAICompatibleAdapter,
    PromptBuilder,
    PromptRequest,
    ProviderConfigurationError,
    TransientProviderError,
)
from .generator import generate_all, generate_core_sample, generate_external_population, generate_finite_population

__all__ = [
    "AnthropicAdapter",
    "BenchmarkTask",
    "DatasetReference",
    "ExecutionRecord",
    "ExecutionSettings",
    "EvaluationEngine",
    "GoogleGenerativeAdapter",
    "InvalidProviderResponseError",
    "MockModelProviderAdapter",
    "ModelExecutionEngine",
    "ModelExecutionError",
    "ModelProviderAdapter",
    "OpenAICompatibleAdapter",
    "PromptBuilder",
    "PromptRequest",
    "ProviderConfigurationError",
    "TaskLoader",
    "TaskValidationError",
    "TransientProviderError",
    "generate_all",
    "generate_finite_population",
    "generate_core_sample",
    "generate_external_population",
]
