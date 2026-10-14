
from pydantic import BaseModel, ConfigDict, Field, model_validator


class SUTRequest(BaseModel):
    """A question submitted to the research assistant."""

    model_config = ConfigDict(extra="forbid")

    question_id: str = Field(min_length=1, max_length=64)
    question: str = Field(min_length=1, max_length=2000)


class Claim(BaseModel):
    """One factual claim made in a generated answer."""

    model_config = ConfigDict(extra="forbid")

    claim_id: str = Field(min_length=1)
    text: str = Field(min_length=1)

class Citation(BaseModel):
    """A reference connecting a claim to a source passage."""

    model_config = ConfigDict(extra="forbid")

    document_id: str = Field(min_length=1)
    passage_id: str = Field(min_length=1)
    claim_ids: list[str] = Field(min_length=1)


class RetrievedPassage(BaseModel):
    """A passage retrieved by the research assistant."""

    model_config = ConfigDict(extra="forbid")

    document_id: str = Field(min_length=1)
    passage_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    rank: int = Field(ge=1)

class SUTResponse(BaseModel):
    """Structured output returned by the research assistant."""

    model_config = ConfigDict(extra="forbid")

    question_id: str = Field(min_length=1, max_length=64)
    answer: str = Field(min_length=1)
    abstained: bool
    abstention_reason: str | None = None
    claims: list[Claim]
    citations: list[Citation]
    retrieved_passages: list[RetrievedPassage]

    @model_validator(mode="after")
    def validate_abstention(self):
        if self.abstained and not self.abstention_reason:
            raise ValueError(
                "An abstaining response must include a reason."
            )

        if not self.abstained and self.abstention_reason is not None:
            raise ValueError(
                "A non-abstaining response cannot have an abstention reason."
            )

        return self