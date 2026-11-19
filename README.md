# EvalLab

An evaluation harness for retrieval-augmented question answering. It answers the question most RAG demos skip: when the retrieved context doesn't contain the answer, does the system say so?

EvalLab runs a fixed question set through a system under test, computes retrieval and abstention metrics case by case, aggregates them, and writes a structured JSON report.

## Metrics

- *Recall@2:* Fraction of relevant passages retrieved in the top two results.
- *Precision@2:* Fraction of the top two retrieval slots occupied by relevant passages.
- *Mean Reciprocal Rank (MRR):* Average reciprocal rank of the first relevant result.
- *Abstention Accuracy:* Fraction of cases where the system's abstention decision matches the expected label.

Retrieval metrics treat unanswerable questions as contributing zero. Precision@2 uses a fixed denominator of two even when fewer than two passages are retrieved, so a system that retrieves nothing scores zero rather than undefined.

## How It Works

1. Loads a fixed document corpus and evaluation dataset.
2. Runs each question through a deterministic, keyword-overlap System Under Test (SUT).
3. Calculates retrieval and abstention metrics for each case.
4. Aggregates metrics across the dataset.
5. Saves a structured JSON evaluation report.

## Project Structure

- data/, Document corpus and evaluation dataset.
- docs/, System contract and evaluation requirements.
- src/evallab/, Schemas, data loading, SUT, metrics, evaluation runner, report writer, and CLI.
- tests/, Automated tests.
- reports/, Generated evaluation report.

## Run

Install the project in editable mode if needed:

cmd
python -m pip install -e .


Run the evaluation from the project root:

cmd
python -m evallab.cli


The report is written to reports/evaluation_report.json.

Run the tests:

cmd
python -m pytest -q


## Design Notes

The system under test is a deterministic keyword-overlap ranker that returns its top passage. It is a control, not a competitor: keeping the SUT fixed and inspectable means the metrics themselves stay testable, so a wrong number points at the harness rather than at a model.

Abstention is scored separately from retrieval because a system can retrieve the right passage and still answer when it shouldn't, and averaging the two hides exactly that failure.

The evaluation dataset is small by design at this stage. It proves the pipeline computes the right numbers; it does not establish retrieval performance, and this README does not claim it does.

## What's Next

- Replace the keyword baseline with a real retriever and re-run the same question set, so the numbers become comparable.
- Grow the question set to fifty, split between answerable and unanswerable.
- Report abstention accuracy per category, so failure modes are visible instead of averaged away.
- Run pytest and the evaluation on every push.

## Status

Pipeline implemented and tested, 18 tests passing. Documentation and reproducibility cleanup in progress.
