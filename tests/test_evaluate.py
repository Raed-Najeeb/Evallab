import json

from evallab.evaluate import (
    evaluate_dataset,
    load_dataset,
    run_evaluation,
    diagnose_retrieval,
    precision_at_k,
    reciprocal_rank,
)


def test_evaluation_returns_metrics():
    dataset = [
        {
            "question_id": "q001",
            "question": "How does RAG use external evidence?",
            "relevant_passage_ids": [
                "paper001/p001",
                "paper001/p002",
            ],
            "should_abstain": False,
        },
        {
            "question_id": "q002",
            "question": "What is the history of ancient Roman architecture?",
            "relevant_passage_ids": [],
            "should_abstain": True,
        },
    ]

    report = evaluate_dataset(dataset)

    assert report["dataset_size"] == 2
    assert 0.0 <= report["metrics"]["retrieval_recall_at_2"] <= 1.0
    assert 0.0 <= report["metrics"]["abstention_accuracy"] <= 1.0
    assert len(report["results"]) == 2


def test_dataset_rejects_duplicate_question_ids(tmp_path):
    dataset_path = tmp_path / "dataset.json"

    dataset_path.write_text(
        json.dumps(
            [
                {
                    "question_id": "duplicate",
                    "question": "Question one?",
                    "relevant_passage_ids": [],
                    "should_abstain": True,
                },
                {
                    "question_id": "duplicate",
                    "question": "Question two?",
                    "relevant_passage_ids": [],
                    "should_abstain": True,
                },
            ]
        ),
        encoding="utf-8",
    )

    import pytest

    with pytest.raises(ValueError, match="unique"):
        load_dataset(dataset_path)


def test_runner_writes_json_report(tmp_path):
    dataset_path = tmp_path / "dataset.json"
    report_path = tmp_path / "reports" / "report.json"

    dataset_path.write_text(
        json.dumps(
            [
                {
                    "question_id": "q001",
                    "question": "How does RAG use external evidence?",
                    "relevant_passage_ids": ["paper001/p001"],
                    "should_abstain": False,
                }
            ]
        ),
        encoding="utf-8",
    )

    report = run_evaluation(dataset_path, report_path)

    assert report_path.exists()

    saved_report = json.loads(
        report_path.read_text(encoding="utf-8")
    )

    assert saved_report == report


def test_precision_at_k_penalizes_irrelevant_results():
    retrieved = ["paper001/p001", "paper002/p001"]
    relevant = {"paper002/p001"}

    assert precision_at_k(retrieved, relevant, k=2) == 0.5


def test_reciprocal_rank_rewards_higher_ranked_evidence():
    retrieved = ["paper001/p001", "paper002/p001"]
    relevant = {"paper002/p001"}

    assert reciprocal_rank(retrieved, relevant) == 0.5


def test_retrieval_diagnosis_identifies_irrelevant_passages():
    retrieved = ["paper001/p001", "paper002/p001"]
    relevant = {"paper002/p001"}

    diagnosis = diagnose_retrieval(retrieved, relevant)

    assert "irrelevant_passages_retrieved" in diagnosis
    assert "retrieval_complete_and_clean" not in diagnosis


def test_reciprocal_rank_is_undefined_without_relevant_passages():
    assert reciprocal_rank(["paper001/p001"], set()) is None
