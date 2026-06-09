from app.database.connection import get_connection
from app.models.ticket import Ticket


class TicketRepository:
    def save(self, ticket: Ticket) -> int:
        """Zapisuje nowe zgłoszenie do bazy. Zwraca id nowego rekordu."""
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO tickets (conversation_id, intent, address, phone, device)
                VALUES (?, ?, ?, ?, ?)
                """,
                ticket.to_tuple(),
            )
            return cursor.lastrowid

    def get_all(self) -> list[Ticket]:
        """Zwraca listę wszystkich zapisanych zgłoszeń."""
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM tickets").fetchall()
        return [self._row_to_ticket(row) for row in rows]

    def get_by_id(self, ticket_id: int) -> Ticket | None:
        """Zwraca zgłoszenie o podanym id lub None jeśli nie istnieje."""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
            ).fetchone()
        return self._row_to_ticket(row) if row else None

    @staticmethod
    def _row_to_ticket(row: object) -> Ticket:
        return Ticket(
            id=row["id"],
            conversation_id=row["conversation_id"],
            intent=row["intent"],
            address=row["address"],
            phone=row["phone"],
            device=row["device"],
        )
