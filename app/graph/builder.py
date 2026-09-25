
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from app.graph.nodes import create_agent_node
from app.graph.state import AgentState
from app.tools.registry import get_tools


def should_continue(state: AgentState):
    messages = state.get("messages", [])

    if not messages:
        return END

    last_message = messages[-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return END


def build_graph(checkpointer=None, store=None):
    tools = get_tools()

    agent_node = create_agent_node(tools)

    builder = StateGraph(AgentState)

    builder.add_node("agent", agent_node)

    builder.add_node(
        "tools",
        ToolNode(tools),
    )

    builder.add_edge(START, "agent")

    builder.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END,
        },
    )

    builder.add_edge("tools", "agent")

    return builder.compile(
        checkpointer=checkpointer,
        store=store,
    )
