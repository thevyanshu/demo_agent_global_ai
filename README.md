
# LangGraph Agent

A modular LangGraph agent with SQLite checkpointing,
custom tools, and DeepEval evaluations.

## Features

- LangGraph agent orchestration
- SQLite conversation persistence
- Tool calling
- Calculator tool
- UTC time tool
- Deterministic evaluation
- LLM-based DeepEval evaluation

## Setup

Create a virtual environment:

python -m venv .venv

Activate it and install dependencies:

pip install -r requirements.txt

Copy environment variables:

cp .env.example .env

Configure GROQ_API_KEY.

## Run the Agent

python -m app.main

## Run Tests

pytest tests -v

## Run Deterministic Evaluation

pytest evals/deterministic -v

## Run LLM Evaluation

pytest evals/llm_based -v -s

## Run All Evaluations

pytest evals -v -s
