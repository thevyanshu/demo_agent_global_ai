"""
Custom DeepEval LLM adapter that routes evaluation calls through Groq.

DeepEval does not ship a native Groq integration. When a plain string
is passed as the ``model`` argument to a metric, the framework falls
back to OpenAI. This adapter implements ``DeepEvalBaseLLM`` so that all
evaluation LLM calls go through the Groq API instead.
"""

from __future__ import annotations

import os
from typing import Any

from deepeval.models import DeepEvalBaseLLM
from groq import Groq


class GroqEvalModel(DeepEvalBaseLLM):
    """Groq-backed evaluation model for DeepEval metrics."""

    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self._model_name = model or os.getenv(
            "DEEPEVAL_MODEL", "qwen/qwen3.8-27b"
        )
        self._api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self._api_key:
            raise ValueError(
                "GROQ_API_KEY must be set as an environment variable "
                "or passed explicitly."
            )
        super().__init__(model=self._model_name)

    def load_model(self) -> Any:
        """Return a configured Groq client."""
        return Groq(api_key=self._api_key)

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """Synchronous text generation via Groq chat completions with rate limit retry."""
        import re
        import time
        from groq import RateLimitError

        max_retries = 3
        for attempt in range(max_retries + 1):
            try:
                response = self.model.chat.completions.create(
                    model=self._model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                )
                return response.choices[0].message.content
            except RateLimitError as exc:
                if attempt == max_retries:
                    raise
                match = re.search(r"try again in ([\d\.]+)s", str(exc))
                wait_time = float(match.group(1)) + 1.5 if match else 30.0
                time.sleep(wait_time)

    async def a_generate(self, prompt: str, **kwargs: Any) -> str:
        """Async generation — delegates to sync for simplicity."""
        return self.generate(prompt, **kwargs)

    def get_model_name(self) -> str:
        """Return the Groq model identifier."""
        return self._model_name
