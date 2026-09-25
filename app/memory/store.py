
from langgraph.store.memory import InMemoryStore


def create_memory_store():
    """
    Development long-term memory store.

    This store is not persisted to disk.
    """
    return InMemoryStore()
