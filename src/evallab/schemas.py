
from pydantic import BaseModel, Field


class Passage(BaseModel):
    passage_id: str
    text: str


class EvaluationCase(BaseModel):
    question_id: str
    question: str
    relevant_passage_ids: list[str] = Field(default_factory=list)
    should_abstain: bool


class SUTResponse(BaseModel):
    answer: str
    retrieved_passage_ids: list[str] = Field(default_factory=list)
    citations: list[str] = Field(default_factory=list)
    abstained: bool
