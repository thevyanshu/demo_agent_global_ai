"""
Evaluation configuration.

Returns a ``GroqEvalModel`` instance so that DeepEval metrics use Groq
instead of silently falling back to OpenAI.
"""

from app.config.settings import get_settings
from evals.models.groq_eval_model import GroqEvalModel


def get_eval_settings():
    """Build the evaluation configuration dictionary.

    The ``model`` value is a ``DeepEvalBaseLLM`` subclass backed by
    Groq, not a plain string. This prevents DeepEval from resolving
    the model string through its default OpenAI path.
    """
    settings = get_settings()

    return {
        "model": GroqEvalModel(
            model=settings.deepeval_model,
            api_key=settings.groq_api_key,
        ),
        "threshold": settings.deepeval_threshold,
    }
