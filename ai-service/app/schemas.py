"""HTTP API request and response models, and the shared vocabulary (categories, severities)."""

import re
from typing import Literal, NewType

from pydantic import BaseModel, Field, computed_field, field_validator

# The case categories and severities. ServiceNow choice lists must match these exactly
# (checked by scripts/check_choice_lists.py).
Category = Literal["leave", "benefits", "payroll", "other", "unknown"]
Severity = Literal["low", "medium", "high"]
Priority = Literal[1, 2, 3, 4]

# A policy chunk id, number#vVERSION#cINDEX (for example KB0090002#v4#c5). Distinct from case ids.
ChunkId = NewType("ChunkId", str)

# Countries are ISO 3166 alpha-2 codes. Policies with no country are stored as GLOBAL.
GLOBAL = "GLOBAL"
_ISO_COUNTRY = re.compile(r"^[A-Z]{2}$")


class Employee(BaseModel):
    # None when unknown: the agent then only sees global policies and the suggestion goes to HR.
    country: str | None = None
    employee_type: str | None = None

    @field_validator("country", mode="before")
    @classmethod
    def _iso_or_none(cls, value: object) -> str | None:
        code = str(value or "").strip().upper()
        return code if _ISO_COUNTRY.match(code) else None


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
    employee: Employee = Employee()


class IngestRequest(BaseModel):
    sys_id: str


class Reference(BaseModel):
    ref: int
    article: str
    version: int
    chunk_id: ChunkId
    title: str
    section: str
    country: str
    quote: str
    start_char: int
    end_char: int


class Claim(BaseModel):
    text: str
    citations: list[Reference]


class Answer(BaseModel):
    text: str  # reply with [n] markers
    formatted: str  # text plus the numbered quotes
    claims: list[Claim]
    references: list[Reference]
    all_claims_cited: bool
    # Citations whose quote did not match the stored text, or that pointed at another country.
    dropped_citations: int = 0
    # Sentences removed because they had no citation after one repair attempt.
    removed_uncited: int = 0

    @computed_field
    @property
    def found_policy(self) -> bool:
        return bool(self.references)


class Classification(BaseModel):
    category: Category
    topics: list[str]
    priority: Priority
    severity: Severity
    confidence: float = Field(ge=0, le=1)
    reasoning: str


class TriageResponse(BaseModel):
    trace_id: str
    classification: Classification
    suggestion: Answer
    # True when every claim is cited, a policy was found and the country is known. ServiceNow also
    # applies its own confidence threshold before posting anything to the employee.
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


class ErrorResponse(BaseModel):
    error: str  # stable code, see app.errors.ErrorCode
    detail: str
