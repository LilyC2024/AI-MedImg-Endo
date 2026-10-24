# Contributing

[Setup](docs/SETUP.md) · [Architecture](docs/ARCHITECTURE.md) · [Security](SECURITY.md)

## Change workflow

1. Read the active [PLAN](PLAN.md) phase; finish and test it before the next.
2. Reuse `.venv`, inspect installed versions and preserve explicit local inference.
3. Keep contracts, data preparation, model execution, workspaces and UI separate.
4. Reproduce a material defect with artificial data before repairing it. Include
   rejected inputs and stale/cancelled work, not tests that only mirror code.
5. Run [validation](docs/VALIDATION.md); record actual results and limitations in
   [EVALUATION](EVALUATION.md). Label scripted inference separately from actual CV.
6. Update the linked guide/API entry and keep the root README concise.

## Cross-repository changes

`src/endo_contracts` is copied byte-for-byte into LOVISA. Change the producer and
consumer intentionally, run both suites and exact sync checks, then test the
producer/receiver pair. Preserve old synthetic/public evidence unless an explicit
versioned migration is documented. Update LOVISA's tested producer CI pin only
after the producer commit exists. Do not rename a schema to bypass validation.

Do not tune on the frozen test split, invent negative labels or claim patient
independence from image hashing. New public data need explicit terms/overlap review.
No ordinary code change justifies retraining or promoting a model automatically.

## Publication

Inspect the full diff and `scripts/check_publication.py`. Commit source, deliberately
artificial fixtures and permitted aggregate metadata; exclude images, models and
runtime reviews. Preserve third-party terms. Describe the concrete bug, new
behavior, tests and residual limitations. A source publication is not deployment
of a clinical service and adds no runtime LLM agents.

Review [branch decisions](docs/BRANCH_REVIEW.md) before changing interoperability.
Run the configured mypy/coverage gates and dependency audit in addition to tests.
Shared signature source must remain identical across all three projects. Source
code is MIT; dataset/model permissions remain separate.
