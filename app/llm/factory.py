
from langchain_groq import ChatGroq

from app.config.settings import get_settings


def get_llm():
    settings = get_settings()

    provider = settings.llm_provider.lower()

    if provider == "groq":
        return ChatGroq(
            model=settings.groq_model,
            api_key=settings.groq_api_key,
            temperature=0,
        )

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )
