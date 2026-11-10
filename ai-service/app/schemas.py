from typing import Literal

from pydantic import BaseModel, Field


class Employee(BaseModel):
    country: str | None = None
    employee_type: str | None = None


class TriageRequest(BaseModel):
    case_id: str
    number: str
    title: str = Field(max_length=500)
    description: str = Field(default="", max_length=20000)
    employee: Employee = Employee()


class ChatRequest(BaseModel):
    case_id: str
    number: str
    message: str = Field(max_length=5000)
    author: str = "hr_agent"


class IngestRequest(BaseModel):
    sys_id: str
    number: str | None = None
    version: int | None = None
    event: Literal["published", "updated", "retired"] = "published"


class Reference(BaseModel):
    ref: int
    article: str
    version: int
    chunk_id: str
    title: str
    section: str
    quote: str
    start_char: int
    end_char: int


class Claim(BaseModel):
    text: str
    citations: list[Reference]


class Answer(BaseModel):
    text: str
    formatted: str
    claims: list[Claim]
    all_claims_cited: bool
    found_policy: bool
    # Sentences removed because they had no citation after one repair attempt.
    removed_uncited: int = 0


class Classification(BaseModel):
    category: str
    topics: list[str]
    priority: int
    severity: str
    confidence: float
    reasoning: str


class TriageResponse(BaseModel):
    trace_id: str
    classification: Classification
    suggestion: Answer
    # True when every claim is cited and at least one policy was found. ServiceNow also applies
    # its own confidence threshold before posting anything to the employee.
    suggestion_allowed: bool
    # Why the suggestion should not be posted to the employee, when suggestion_allowed is false.
    suggestion_blocked_reason: str | None = None
    tools_used: list[str]
    model: str


class Proposal(BaseModel):
    action: Literal["close"]
    resolution: str


class ChatResponse(BaseModel):
    trace_id: str
    reply: Answer
    proposed_action: Proposal | None
    tools_used: list[str]
    model: str
