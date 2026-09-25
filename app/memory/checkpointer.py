
import sqlite3
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

from app.config.settings import get_settings


def create_sqlite_checkpointer():
    settings = get_settings()

    db_path = Path(settings.sqlite_db_path)

    db_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        str(db_path),
        check_same_thread=False,
    )

    checkpointer = SqliteSaver(connection)

    # Initialize the SQLite checkpoint schema.
    checkpointer.setup()

    return connection, checkpointer
