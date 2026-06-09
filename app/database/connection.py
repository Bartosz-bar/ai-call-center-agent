import sqlite3
from contextlib import contextmanager
from typing import Generator

DATABASE_PATH = "database.db"


def init_db() -> None:
    """Inicjalizuje bazę danych i tworzy tabele jeśli nie istnieją."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT    NOT NULL,
                intent      TEXT    NOT NULL,
                address     TEXT    NOT NULL,
                phone       TEXT    NOT NULL,
                device      TEXT
            )
        """)


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager zapewniający bezpieczne połączenie z bazą danych."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
