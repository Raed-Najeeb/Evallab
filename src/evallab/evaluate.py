
import json
from pathlib import Path

from evallab.schemas import SUTRequest
from evallab.sut import answer_question


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "data" / "evaluation_dataset.json"
REPORT_PATH = PROJECT_ROOT / "reports" / "evaluation_report.json"
K = 2


def load_dataset(path: Path = DATASET_PATH) -> list[dict]:
    with path.open(encoding="utf-8") as file:
        dataset = json.load(file)

    if not isinstance(dataset, list) or not dataset:
        raise ValueError("The evaluation dataset must be a non-empty list.")

    question_ids = [case["question_id"] for case in dataset]

    if len(question_ids) != len(set(question_ids)):
        raise ValueError("Evaluation question IDs must be unique.")

    return dataset


def precision_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int = K,
) -> float | None:
    if k < 1:
        raise ValueError("k must be at least 1.")

    if not relevant_ids:
        return None

    hits = len(set(retrieved_ids[:k]) & relevant_ids)
    return hits / k


def reciprocal_rank(
    retrieved_ids: list[str],
    relevant_ids: set[str],
) -> float | None:
    if not relevant_ids:
        return None

    for rank, passage_id in enumerate(retrieved_ids, start=1):
        if passage_id in relevant_ids:
            return 1.0 / rank

    return 0.0


def diagnose_retrieval(
    retrieved_ids: list[str],
    relevant_ids: set[str],
) -> list[str]:
    retrieved_set = set(retrieved_ids)
    diagnosis = []

    if not relevant_ids:
        diagnosis.append("no_relevant_passages_expected")
    else:
        if not (retrieved_set & relevant_ids):
            diagnosis.append("relevant_evidence_not_found")
        elif not relevant_ids.issubset(retrieved_set):
            diagnosis.append("some_relevant_evidence_missed")

        if relevant_ids.issubset(retrieved_set):
            if not (retrieved_set - relevant_ids):
                diagnosis.append("retrieval_complete_and_clean")

    if retrieved_set - relevant_ids:
        diagnosis.append("irrelevant_passages_retrieved")

    return diagnosis


def evaluate_dataset(dataset: list[dict]) -> dict:
    results = []

    total_relevant = 0
    total_retrieved_relevant = 0
    correct_abstention_decisions = 0
    precision_scores = []
    reciprocal_rank_scores = []

    for case in dataset:
        request = SUTRequest(
            question_id=case["question_id"],
            question=case["question"],
        )
        response = answer_question(request)

        relevant_ids = set(case["relevant_passage_ids"])

        # Preserve ranking order for ranking-sensitive metrics.
        retrieved_ids = [
            f"{passage.document_id}/{passage.passage_id}"
            for passage in response.retrieved_passages
        ]

        retrieved_relevant = relevant_ids & set(retrieved_ids)

        recall_at_k = (
            len(retrieved_relevant) / len(relevant_ids)
            if relevant_ids
            else None
        )

        precision = precision_at_k(retrieved_ids, relevant_ids)
        rr = reciprocal_rank(retrieved_ids, relevant_ids)

        abstention_correct = (
            response.abstained == case["should_abstain"]
        )

        total_relevant += len(relevant_ids)
        total_retrieved_relevant += len(retrieved_relevant)
        correct_abstention_decisions += int(abstention_correct)

        if precision is not None:
            precision_scores.append(precision)

        if rr is not None:
            reciprocal_rank_scores.append(rr)

        results.append(
            {
                "question_id": case["question_id"],
                "retrieved_passage_ids": retrieved_ids,
                "relevant_passage_ids": sorted(relevant_ids),
                "recall_at_2": recall_at_k,
                "precision_at_2": precision,
                "reciprocal_rank": rr,
                "retrieval_diagnosis": diagnose_retrieval(
                    retrieved_ids, relevant_ids
                ),
                "should_abstain": case["should_abstain"],
                "actually_abstained": response.abstained,
                "abstention_correct": abstention_correct,
            }
        )

    return {
        "dataset_size": len(dataset),
        "metrics": {
            "retrieval_recall_at_2": (
                total_retrieved_relevant / total_relevant
                if total_relevant
                else None
            ),
            "mean_precision_at_2": (
                sum(precision_scores) / len(precision_scores)
                if precision_scores
                else None
            ),
            "mean_reciprocal_rank": (
                sum(reciprocal_rank_scores) / len(reciprocal_rank_scores)
                if reciprocal_rank_scores
                else None
            ),
            "abstention_accuracy": (
                correct_abstention_decisions / len(dataset)
            ),
        },
        "results": results,
    }


def run_evaluation(
    dataset_path: Path = DATASET_PATH,
    report_path: Path = REPORT_PATH,
) -> dict:
    dataset = load_dataset(dataset_path)
    report = evaluate_dataset(dataset)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    return report


if __name__ == "__main__":
    report = run_evaluation()
    print(json.dumps(report, indent=2))
