
import json
from pathlib import Path

from evallab.schemas import EvaluationCase, Passage


def load_corpus(path: Path) -> list[Passage]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [Passage.model_validate(item) for item in data]


def load_evaluation_dataset(path: Path) -> list[EvaluationCase]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [EvaluationCase.model_validate(item) for item in data]
