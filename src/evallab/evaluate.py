
from pathlib import Path

from evallab.data_loader import load_corpus, load_evaluation_dataset
from evallab.metrics import (
    abstention_correct,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)
from evallab.sut import SimpleSUT


def run_evaluation(data_dir: Path) -> dict:
    corpus = load_corpus(data_dir / "corpus" / "passages.json")
    cases = load_evaluation_dataset(data_dir / "evaluation_dataset.json")

    sut = SimpleSUT(corpus)

    results = []

    for case in cases:
        response = sut.answer(case)

        results.append(
            {
                "question_id": case.question_id,
                "retrieved_passage_ids": response.retrieved_passage_ids,
                "relevant_passage_ids": case.relevant_passage_ids,
                "abstained": response.abstained,
                "should_abstain": case.should_abstain,
                "recall_at_2": recall_at_k(
                    response.retrieved_passage_ids,
                    case.relevant_passage_ids,
                    2,
                ),
                "precision_at_2": precision_at_k(
                    response.retrieved_passage_ids,
                    case.relevant_passage_ids,
                    2,
                ),
                "reciprocal_rank": reciprocal_rank(
                    response.retrieved_passage_ids,
                    case.relevant_passage_ids,
                ),
                "abstention_correct": abstention_correct(
                    response.abstained,
                    case.should_abstain,
                ),
            }
        )

    if not results:
        raise ValueError("Evaluation dataset must contain at least one case")

    metrics = {
        "mean_recall_at_2": sum(
            result["recall_at_2"] for result in results
        ) / len(results),
        "mean_precision_at_2": sum(
            result["precision_at_2"] for result in results
        ) / len(results),
        "mean_reciprocal_rank": sum(
            result["reciprocal_rank"] for result in results
        ) / len(results),
        "abstention_accuracy": sum(
            result["abstention_correct"] for result in results
        ) / len(results),
    }

    return {
        "dataset_size": len(results),
        "metrics": metrics,
        "results": results,
    }
