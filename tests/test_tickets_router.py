from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _mock_extract(data: dict):
    """Helper zwracający funkcję mocka dla extract_ticket_data."""
    return lambda text: data


class TestHealthCheck:
    def test_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestHandleMessage:
    def test_asks_for_missing_fields_when_incomplete(self):
        with patch(
            "app.routers.tickets.extract_ticket_data",
            _mock_extract({"intent": "awaria", "device": None, "address": None, "phone": None}),
        ):
            response = client.post(
                "/tickets/message",
                json={"conversation_id": "test-001", "text": "mam awarię"},
            )

        assert response.status_code == 200
        body = response.json()
        assert "adres" in body["response"]
        assert "numer telefonu" in body["response"]

    def test_saves_ticket_when_data_complete(self):
        with patch(
            "app.routers.tickets.extract_ticket_data",
            _mock_extract({
                "intent": "awaria",
                "device": "pralka",
                "address": "ul. Testowa 1, Kraków",
                "phone": "500600700",
            }),
        ):
            response = client.post(
                "/tickets/message",
                json={"conversation_id": "test-complete-001", "text": "pełne dane"},
            )

        assert response.status_code == 200
        body = response.json()
        assert "przyjęte" in body["response"]
        assert body["ticket_data"]["intent"] == "awaria"

    def test_rejects_empty_text(self):
        response = client.post(
            "/tickets/message",
            json={"conversation_id": "test-002", "text": ""},
        )
        assert response.status_code == 422


class TestListTickets:
    def test_returns_list(self):
        response = client.get("/tickets/")
        assert response.status_code == 200
        body = response.json()
        assert "tickets" in body
        assert "total" in body

    def test_total_matches_tickets_length(self):
        response = client.get("/tickets/")
        body = response.json()
        assert body["total"] == len(body["tickets"])


class TestGetTicket:
    def test_returns_404_for_nonexistent_ticket(self):
        response = client.get("/tickets/999999")
        assert response.status_code == 404
