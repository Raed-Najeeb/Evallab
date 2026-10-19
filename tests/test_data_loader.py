
from pathlib import Path

from evallab.data_loader import load_corpus, load_evaluation_dataset
from evallab.schemas import EvaluationCase, Passage


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_load_corpus():
    path = PROJECT_ROOT / "data" / "corpus" / "passages.json"

    passages = load_corpus(path)

    assert len(passages) == 4
    assert all(isinstance(passage, Passage) for passage in passages)
    assert passages[0].passage_id == "doc1/p1"


def test_load_evaluation_dataset():
    path = PROJECT_ROOT / "data" / "evaluation_dataset.json"

    cases = load_evaluation_dataset(path)

    assert len(cases) == 4
    assert all(isinstance(case, EvaluationCase) for case in cases)
    assert cases[0].question_id == "eval001"
    assert cases[3].should_abstain is True
