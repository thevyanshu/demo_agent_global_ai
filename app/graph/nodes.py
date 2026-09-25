
from langchain_core.messages import SystemMessage

from app.llm.factory import get_llm
from app.prompts.agent import SYSTEM_PROMPT


def create_agent_node(tools):
    llm = get_llm().bind_tools(tools)

    def agent_node(state):
        messages = state.get("messages", [])

        prompt_messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            *messages,
        ]

        response = llm.invoke(prompt_messages)

        return {
            "messages": [response],
        }

    return agent_node
