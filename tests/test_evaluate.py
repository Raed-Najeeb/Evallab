
from pathlib import Path

from evallab.evaluate import run_evaluation


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


def test_run_evaluation_returns_one_result_per_case():
    report = run_evaluation(DATA_DIR)

    assert report["dataset_size"] == 4
    assert len(report["results"]) == 4


def test_run_evaluation_records_abstention_behavior():
    report = run_evaluation(DATA_DIR)

    abstention_result = report["results"][3]

    assert abstention_result["question_id"] == "eval004"
    assert abstention_result["should_abstain"] is True
    assert abstention_result["abstained"] is True
    assert abstention_result["retrieved_passage_ids"] == []


def test_run_evaluation_calculates_expected_metrics():
    report = run_evaluation(DATA_DIR)

    metrics = report["metrics"]

    assert metrics["mean_recall_at_2"] == 0.75
    assert metrics["mean_precision_at_2"] == 0.375
    assert metrics["mean_reciprocal_rank"] == 0.75
    assert metrics["abstention_accuracy"] == 1.0
