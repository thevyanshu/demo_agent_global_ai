
from typing import Annotated, Any, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    """
    Shared state across LangGraph nodes.
    """

    messages: Annotated[
        list[AnyMessage],
        add_messages,
    ]

    user_id: str
    session_id: str

    metadata: dict[str, Any]
