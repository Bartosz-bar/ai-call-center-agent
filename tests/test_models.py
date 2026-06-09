import pytest
from app.models.ticket import ConversationState, Ticket


class TestConversationState:
    def test_is_complete_returns_false_when_empty(self):
        state = ConversationState()
        assert state.is_complete() is False

    def test_is_complete_returns_true_when_all_required_fields_set(self):
        state = ConversationState(intent="awaria", address="Kraków", phone="123456789")
        assert state.is_complete() is True

    def test_is_complete_requires_phone(self):
        state = ConversationState(intent="awaria", address="Kraków")
        assert state.is_complete() is False

    def test_missing_fields_returns_all_when_empty(self):
        state = ConversationState()
        missing = state.missing_fields()
        assert "opis problemu" in missing
        assert "adres" in missing
        assert "numer telefonu" in missing

    def test_missing_fields_returns_only_missing(self):
        state = ConversationState(intent="awaria", address="Kraków")
        missing = state.missing_fields()
        assert missing == ["numer telefonu"]

    def test_update_sets_fields_from_dict(self):
        state = ConversationState()
        state.update({"intent": "reklamacja", "phone": "500600700"})
        assert state.intent == "reklamacja"
        assert state.phone == "500600700"
        assert state.address is None

    def test_update_ignores_none_values(self):
        state = ConversationState(intent="awaria")
        state.update({"intent": None, "address": "Warszawa"})
        assert state.intent == "awaria"
        assert state.address == "Warszawa"

    def test_to_dict_returns_all_fields(self):
        state = ConversationState(intent="awaria", device="pralka", address="Kraków", phone="123")
        result = state.to_dict()
        assert result == {
            "intent": "awaria",
            "device": "pralka",
            "address": "Kraków",
            "phone": "123",
        }


class TestTicket:
    def test_to_tuple_returns_correct_order(self):
        ticket = Ticket(
            conversation_id="abc",
            intent="awaria",
            address="Kraków",
            phone="123",
            device="pralka",
        )
        assert ticket.to_tuple() == ("abc", "awaria", "Kraków", "123", "pralka")

    def test_to_tuple_handles_none_device(self):
        ticket = Ticket(conversation_id="abc", intent="awaria", address="Kraków", phone="123")
        assert ticket.to_tuple() == ("abc", "awaria", "Kraków", "123", None)
