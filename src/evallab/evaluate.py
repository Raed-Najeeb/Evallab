import json
from pathlib import Path

from evallab.schemas import SUTRequest
from evallab.sut import answer_question


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "data" / "evaluation_dataset.json"
REPORT_PATH = PROJECT_ROOT / "reports" / "evaluation_report.json"


def load_dataset(path: Path = DATASET_PATH) -> list[dict]:
    with path.open(encoding="utf-8") as file:
        dataset = json.load(file)

    if not isinstance(dataset, list) or not dataset:
        raise ValueError("The evaluation dataset must be a non-empty list.")

    question_ids = [case["question_id"] for case in dataset]

    if len(question_ids) != len(set(question_ids)):
        raise ValueError("Evaluation question IDs must be unique.")

    return dataset


def evaluate_dataset(dataset: list[dict]) -> dict:
    results = []

    total_relevant = 0
    total_retrieved_relevant = 0
    correct_abstention_decisions = 0

    for case in dataset:
        request = SUTRequest(
            question_id=case["question_id"],
            question=case["question"],
        )

        response = answer_question(request)

        relevant_ids = set(case["relevant_passage_ids"])

        retrieved_ids = {
            f"{passage.document_id}/{passage.passage_id}"
            for passage in response.retrieved_passages
        }

        retrieved_relevant = relevant_ids & retrieved_ids

        # Recall is undefined when no relevant passages are annotated.
        recall_at_2 = (
            len(retrieved_relevant) / len(relevant_ids)
            if relevant_ids
            else None
        )

        abstention_correct = (
            response.abstained == case["should_abstain"]
        )

        total_relevant += len(relevant_ids)
        total_retrieved_relevant += len(retrieved_relevant)
        correct_abstention_decisions += int(abstention_correct)

        results.append(
            {
                "question_id": case["question_id"],
                "retrieved_passage_ids": sorted(retrieved_ids),
                "relevant_passage_ids": sorted(relevant_ids),
                "recall_at_2": recall_at_2,
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