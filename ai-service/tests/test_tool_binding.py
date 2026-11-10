"""The model never chooses whose policies or which case it reads: the request decides."""

from types import SimpleNamespace

from app.agent.mcp_client import ToolClient, _without


class RecordingSession:
    def __init__(self):
        self.calls = []

    async def call_tool(self, name, arguments):
        self.calls.append((name, arguments))
        return SimpleNamespace(content=[SimpleNamespace(type="text", text="[]")], isError=False)


def _client() -> tuple[ToolClient, RecordingSession]:
    client, session = ToolClient(), RecordingSession()
    client._session = session
    return client, session


def test_bound_parameters_are_hidden_from_the_model():
    schema = {
        "type": "object",
        "properties": {"query": {}, "country": {}},
        "required": ["query", "country"],
    }
    assert _without(schema, {"country"}) == {
        "type": "object",
        "properties": {"query": {}},
        "required": ["query"],
    }


async def test_country_from_the_request_replaces_the_models_choice():
    client, session = _client()
    await client.call(
        "search_policies", {"query": "parental leave", "country": "US"}, {"country": "DE"}
    )
    assert session.calls == [("search_policies", {"query": "parental leave", "country": "DE"})]


async def test_unknown_country_is_sent_as_empty_so_only_global_policies_match():
    client, session = _client()
    await client.call(
        "get_policy_section", {"article": "KB0090001", "country": "US"}, {"country": ""}
    )
    assert session.calls[0][1]["country"] == ""


async def test_get_case_always_reads_the_case_being_worked_on():
    client, session = _client()
    await client.call(
        "get_case", {"case_number": "HRC0009999"}, {"case_number": "HRC0001001", "country": "DE"}
    )
    assert session.calls == [("get_case", {"case_number": "HRC0001001"})]
