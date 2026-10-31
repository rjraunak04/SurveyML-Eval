# Benchmark Task Schema

This document defines the benchmark task schema used for SurveyML-Eval task-instance construction.

## Purpose

The benchmark task schema standardizes the metadata, provenance, public inputs, hidden reference material, and output requirements for each benchmark task family T01–T08.

## Required fields

Each task instance must include:

- `task_id`: unique task family identifier such as `T01`.
- `task_instance_id`: unique instance identifier, typically `T01-001`.
- `title`: human-readable task name.
- `task_family`: algorithmic family identifier.
- `difficulty`: difficulty label such as `intermediate` or `advanced`.
- `dataset_refs`: list of synthetic datasets used by the task.
- `model_visible_input`: public model-facing description and safe column list.
- `hidden_reference`: grading reference and must-identify criteria.
- `response_schema`: expected JSON response structure.
- `provenance`: dataset-origin and reproducibility metadata.

## Model-visible requirements

Model-visible inputs must exclude hidden target variables, leakage labels, protected audit columns, and out-of-scope records. The benchmark must separate public task data from hidden evaluation material.

## Hidden reference requirements

Reference answers should contain the criteria that a valid answer must identify and a grading policy that preserves the benchmark's scientific assumptions.

## Reproducibility requirements

All task definitions must be traceable to the synthetic benchmark datasets, generated with documented seeds and metadata, and must not be reported as empirical findings.
