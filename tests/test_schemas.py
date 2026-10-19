
from evallab.schemas import EvaluationCase, Passage, SUTResponse


def test_passage_schema():
    passage = Passage(passage_id="doc1/p1", text="Evidence text")

    assert passage.passage_id == "doc1/p1"
    assert passage.text == "Evidence text"


def test_evaluation_case_schema():
    case = EvaluationCase(
        question_id="eval001",
        question="What is retrieval?",
        relevant_passage_ids=["doc1/p1"],
        should_abstain=False,
    )

    assert case.question_id == "eval001"
    assert case.relevant_passage_ids == ["doc1/p1"]
    assert case.should_abstain is False


def test_sut_response_schema():
    response = SUTResponse(
        answer="Retrieval finds relevant passages.",
        retrieved_passage_ids=["doc1/p1"],
        citations=["doc1/p1"],
        abstained=False,
    )

    assert response.citations == ["doc1/p1"]
    assert response.abstained is False
