# AGENTS.md

## Project: SurveyML-Eval

SurveyML-Eval is a research benchmark for evaluating Large Language Models on survey-weighted machine learning, leakage-safe validation, external population validation, and distribution shift. This repository is organized around the approved research problem, objectives, benchmark task design, methodology, data schema, and grading framework captured in `README.md` and the documents under `docs/`.

## Required operating rules

1. Always inspect the relevant project documentation before implementing a task.
   - At minimum, review `README.md` and the most relevant files in `docs/` for the task area.
   - Read task, schema, methodology, and design documentation before changing code, data generation logic, or evaluation assets.
   - Do not treat the repository as a blank slate; treat the approved research objectives, task families, and evaluation design as the source of truth.

2. Preserve the approved research objectives, methodology, dataset schemas, and statistical assumptions.
   - Do not relax or reinterpret the benchmark conventions documented in the project files.
   - Keep the benchmark aligned with the cited design principles in the problem statement, methodology, task design, and schema documents.
   - Preserve task family structure, score definitions, evaluation assumptions, and dataset metadata expectations.

3. Maintain a lessons-learned and QA checklist.
   - Keep an explicit record of prior mistakes, corrected issues, and the associated fixes.
   - Never repeat previously corrected mistakes in new work.
   - Use a QA checklist before finalizing changes: correctness, reproducibility, validation, file hygiene, and documentation review.

4. Ensure mathematically correct survey sampling, inclusion probabilities, and inverse-probability weights.
   - Sampling design logic must be mathematically consistent with the chosen survey design.
   - Inclusion probabilities and weights must be derived from the actual design, not guessed or approximated without justification.
   - If weights are used, document their target and ensure they are consistent with the design assumptions.
   - Distinguish finite-population quantities from realized sample quantities.

5. Distinguish finite population from selected sample.
   - The finite population is the full target population that would exist before selection.
   - The selected sample is the subset drawn under the sampling design.
   - Do not conflate these objects in formulas, weights, or analysis logic.
   - When working on sample design tasks, keep the population and sample definitions separate in code, tests, and documentation.

6. Generate population predictors and outcomes before sample selection when required.
   - For synthetic survey tasks, generate the full finite population predictors and outcomes first when the design requires it.
   - Only then apply the sampling design to derive the observed sample.
   - Preserve the population-level information needed for external validation, design-based analysis, and distribution-shift checks.

7. Never invent research results, metrics, citations, or test outcomes.
   - Do not report performance numbers, benchmark results, model scores, citations, or findings that were not actually produced and validated.
   - If a result is not observed, do not claim it.
   - Be explicit about what is planned, what is synthetic, and what is verified.

8. Clearly identify all synthetic data and assumptions.
   - Synthetic data must be labeled as synthetic and must not be presented as empirical claims about real populations.
   - Document generation assumptions, data-generating mechanisms, and any simplified survey design assumptions.
   - Record assumptions in code comments, metadata, and task documentation when relevant.

9. Use reproducible random seeds and independent random streams.
   - All stochastic generation must be reproducible through fixed seeds.
   - Use independent streams for separate design components when needed (e.g., population generation, sample selection, missingness, outcome noise) so that each stochastic step remains traceable and reproducible.
   - Never rely on unspecified global randomness in a benchmark workflow.

10. Write modular, maintainable, and tested Python code.
   - Keep functionality separated by concern: data generation, sampling, validation, tasks, grading, and reporting.
   - Prefer clear functions, explicit dataclasses or typed structures, and small, reviewable code units.
   - Add or update relevant tests when code behavior changes.
   - Preserve repository readability and avoid unnecessary complexity.

11. Run relevant tests and inspect actual outputs before reporting completion.
   - Validate the smallest relevant test scope for the task.
   - Inspect real output, errors, and generated artifacts before claiming success.
   - Report actual test results, including failures, warnings, and unresolved issues.
   - Do not report success without evidence from execution and output inspection.

12. Check Markdown formatting, equations, whitespace, file completeness, and Git diffs.
   - Keep Markdown clear, consistent, and reviewable.
   - Ensure equations render correctly and are not malformed or missing symbols.
   - Check line breaks, spacing, and overall file completeness before finishing a task.
   - Review the Git diff and confirm only intended files changed.

13. Never overwrite unrelated user changes.
   - Before editing a file, inspect whether it already contains user work or local modifications.
   - Do not clobber unrelated edits, generated artifacts, or uncommitted work.
   - Keep changes narrow, specific, and directly tied to the requested task.

14. Never commit, push, merge, or delete branches without explicit approval.
   - Git workflows are restricted; do not perform commit, push, merge, or branch-deletion actions unless the user explicitly authorizes them.
   - If a destructive or repository-altering action is being considered, ask for permission before proceeding.

15. Work on one complete checkpoint at a time.
   - Do not jump ahead to future tasks or partially implemented checkpoints.
   - Complete the current checkpoint and verify the relevant outputs before moving on.
   - Keep each checkpoint scoped and reviewable.

## Workflow expectations

- Read the task requirement, the relevant design docs, and the associated schema before making a change.
- Validate assumptions against the project methodology rather than improvising a new interpretation.
- Keep notes on lessons learned and QA outcomes in the working process so that common errors are not repeated.
- If a task depends on multiple documentation sources, read the complementary ones together rather than in isolation.
- When the task involves data generation or sampling, treat finite populations, design probabilities, and weights as core methodological inputs, not incidental details.

## Documentation and repository standards

- Keep the repository aligned with the documented architecture in `docs/repository_architecture.md`.
- Preserve the benchmark task conventions defined in `docs/benchmark_task_design.md` and `docs/benchmark_task_schema.md`.
- Preserve the dataset schema and metadata conventions from `docs/dataset_schema.md` and `docs/dataset_inventory.md`.
- Maintain the distinction between synthetic, derived, and external datasets as described in the project documentation.
- Keep generated files, task artifacts, and outputs reproducible and clearly labeled.

## Change control and safety

- Ask permission before potentially destructive operations.
- Treat the repository as a research project with explicit design constraints, not a generic coding exercise.
- Keep changes limited to the current checkpoint and only to the files required for the approved task.
- Report changed files, test results, any failures, and unresolved issues in the final status update.

## Final instruction

Only create or modify the files explicitly required for the current approved task. Do not implement or expand beyond the approved checkpoint without direction. For this repository, the design and benchmark documentation are the authority; the benchmark implementation must remain faithful to them.
