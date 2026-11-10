"""The one failure type the service raises, with stable codes that ServiceNow can log and match on.

app.main maps each code to an HTTP status in one place. Messages are safe to show to callers;
raw provider or database errors are logged, never returned.
"""

from typing import Literal

ErrorCode = Literal[
    "llm_refused",  # the model declined the request
    "llm_truncated",  # the answer was cut off
    "llm_invalid_output",  # structured output did not parse
    "llm_unavailable",  # the provider could not be reached or returned an error
    "index_unavailable",  # the policy search index could not be read
    "busy",  # too many requests in progress; try again
]

HTTP_STATUS: dict[str, int] = {
    "llm_refused": 502,
    "llm_truncated": 502,
    "llm_invalid_output": 502,
    "llm_unavailable": 502,
    "index_unavailable": 503,
    "busy": 503,
}


class AgentError(Exception):
    def __init__(self, code: ErrorCode, message: str):
        super().__init__(message)
        self.code = code
        self.message = message
