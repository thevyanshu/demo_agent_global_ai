
# LangGraph Agent

A modular LangGraph agent powered by **Groq** with SQLite checkpointing,
custom tools, and DeepEval evaluations.

## Features

- LangGraph agent orchestration with Groq LLM
- SQLite conversation checkpoint persistence
- Tool calling (calculator, UTC time)
- Deterministic evaluation (direct tool tests)
- LLM-based DeepEval evaluation via custom Groq adapter

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it and install dependencies:

```bash
pip install -r requirements.txt
```

Copy environment variables:

```bash
cp .env.example .env
```

Configure `GROQ_API_KEY` with your Groq API key.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | Groq API key |
| `GROQ_MODEL` | No | Agent model (default: `openai/gpt-oss-120b`) |
| `DEEPEVAL_MODEL` | No | Evaluation judge model (default: `qwen/qwen3.8-27b`) |
| `DEEPEVAL_THRESHOLD` | No | Minimum relevancy score (default: `0.7`) |
| `SQLITE_DB_PATH` | No | Checkpoint DB path (default: `data/checkpoints.sqlite`) |

## Run the Agent

```bash
python -m app.main
```

## Run Tests

```bash
pytest tests -v
```

## Run Deterministic Evaluation

```bash
pytest evals/deterministic -v
```

## Run LLM Evaluation

```bash
pytest evals/llm_based -v -s
```

## Run All Evaluations

```bash
pytest evals -v -s
```

## Architecture

- `app/config/` — Centralized Pydantic settings
- `app/llm/` — Groq LLM factory
- `app/graph/` — LangGraph state, nodes, and builder
- `app/tools/` — Safe AST-based calculator, UTC time tool
- `app/memory/` — SQLite checkpointer, in-memory store
- `app/prompts/` — System prompt
- `evals/` — Deterministic and LLM-based evaluations
- `evals/models/` — Custom Groq adapter for DeepEval

## Notes

- **InMemoryStore** is used for development only; it is **not** persisted
  across restarts. Only SQLite checkpoint state is persisted.
- SQLite has single-writer concurrency limitations.
  For multi-worker production use, consider PostgreSQL checkpointing.
