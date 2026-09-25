
from uuid import uuid4

from langchain_core.messages import HumanMessage

from app.graph.builder import build_graph
from app.memory.checkpointer import create_sqlite_checkpointer
from app.memory.store import create_memory_store


def run_agent(user_input: str) -> str:
    connection, checkpointer = (
        create_sqlite_checkpointer()
    )

    store = create_memory_store()

    try:
        graph = build_graph(
            checkpointer=checkpointer,
            store=store,
        )

        thread_id = f"eval-{uuid4()}"

        config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=user_input
                    )
                ],
                "user_id": "eval-user",
                "session_id": thread_id,
            },
            config=config,
        )

        last_message = result["messages"][-1]

        content = last_message.content

        if isinstance(content, str):
            return content

        return str(content)

    finally:
        connection.close()
