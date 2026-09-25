"""Unit tests for LangGraph graph compilation.

These tests verify the graph structure and compilation without making
any Groq API calls, by mocking the LLM factory.
"""

from unittest.mock import patch, MagicMock

from langchain_core.messages import AIMessage, HumanMessage

from langgraph.graph import END

from app.graph.builder import build_graph, should_continue


# ── should_continue routing ──────────────────────────────────────────

def test_should_continue_returns_end_on_no_messages():
    state = {"messages": []}
    assert should_continue(state) == END


def test_should_continue_returns_end_on_normal_message():
    msg = AIMessage(content="Hello")
    state = {"messages": [msg]}
    assert should_continue(state) == END


def test_should_continue_returns_tools_on_tool_call():
    msg = AIMessage(
        content="",
        tool_calls=[
            {
                "id": "call_1",
                "name": "calculate",
                "args": {"expression": "2+2"},
            }
        ],
    )
    state = {"messages": [msg]}
    assert should_continue(state) == "tools"


# ── Graph compilation ────────────────────────────────────────────────

@patch("app.graph.nodes.get_llm")
def test_graph_compiles_with_expected_nodes(mock_get_llm):
    """Graph must compile and contain the agent and tools nodes."""
    mock_llm = MagicMock()
    mock_llm.bind_tools.return_value = mock_llm
    mock_get_llm.return_value = mock_llm

    graph = build_graph()

    # Compiled graph should have the expected node names.
    node_names = set(graph.nodes.keys())
    assert "agent" in node_names
    assert "tools" in node_names
