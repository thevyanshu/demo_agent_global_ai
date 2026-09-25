
from langchain_core.messages import HumanMessage

from app.graph.builder import build_graph
from app.memory.checkpointer import create_sqlite_checkpointer
from app.memory.store import create_memory_store


def main():
    connection, checkpointer = (
        create_sqlite_checkpointer()
    )

    store = create_memory_store()

    try:
        graph = build_graph(
            checkpointer=checkpointer,
            store=store,
        )

        config = {
            "configurable": {
                "thread_id": "demo-user-session-1",
            }
        }

        print("LangGraph SQLite Agent")
        print("Type 'exit' to quit.\n")

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in {
                "exit",
                "quit",
            }:
                break

            if not user_input:
                continue

            result = graph.invoke(
                {
                    "messages": [
                        HumanMessage(
                            content=user_input
                        )
                    ],
                    "user_id": "demo-user",
                    "session_id": "demo-session",
                },
                config=config,
            )

            last_message = result["messages"][-1]

            print(f"\nAgent: {last_message.content}\n")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
