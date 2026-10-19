
# EvalLab

EvalLab is a small, reproducible evaluation framework for assessing retrieval quality and abstention behavior in a question-answering system.

## How It Works

1. Loads a fixed document corpus and evaluation dataset.
2. Runs each question through a deterministic, keyword-overlap System Under Test (SUT).
3. Calculates retrieval and abstention metrics for each case.
4. Aggregates metrics across the dataset.
5. Saves a structured JSON evaluation report.

## Metrics

- **Recall@2:** Fraction of relevant passages retrieved in the top two results.
- **Precision@2:** Fraction of the top two retrieval slots occupied by relevant passages.
- **Mean Reciprocal Rank (MRR):** Average reciprocal rank of the first relevant result.
- **Abstention Accuracy:** Fraction of cases where the system's abstention decision matches the expected label.

For this baseline, unanswerable questions contribute zero to retrieval metrics. Precision@2 uses a fixed denominator of two, even when fewer than two passages are retrieved.

## Project Structure

- `data/` — Document corpus and evaluation dataset.
- `docs/` — System contract and evaluation requirements.
- `src/evallab/` — Schemas, data loading, SUT, metrics, evaluation runner, report writer, and CLI.
- `tests/` — Automated tests.
- `reports/` — Generated evaluation report.

## Run

Activate the virtual environment and install the project in editable mode if needed:

```cmd
python -m pip install -e .
```

Run the evaluation from the project root:

```cmd
python -m evallab.cli
```

The report is written to `reports/evaluation_report.json`.

Run the tests:

```cmd
python -m pytest -q
```

## Limitations

The current SUT is deliberately simple: it ranks passages using token overlap and returns the top passage as its answer. It is a baseline for learning evaluation design, not a production-grade retrieval or question-answering system.

The evaluation dataset contains only four examples, so its metrics demonstrate the pipeline rather than establish general performance.

## Current Status

Foundational evaluation pipeline implemented. The next step is final validation, documentation review, and reproducible project cleanup.
