from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Ticket:
    conversation_id: str
    intent: str
    address: str
    phone: str
    device: Optional[str] = None
    id: Optional[int] = field(default=None)

    def to_tuple(self) -> tuple:
        return (self.conversation_id, self.intent, self.address, self.phone, self.device)


@dataclass
class ConversationState:
    intent: Optional[str] = None
    device: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

    def update(self, data: dict) -> None:
        """Aktualizuje stan rozmowy danymi wyekstrahowanymi przez AI."""
        if data.get("intent"):
            self.intent = data["intent"]
        if data.get("address"):
            self.address = data["address"]
        if data.get("phone"):
            self.phone = data["phone"]
        if data.get("device"):
            self.device = data["device"]

    def is_complete(self) -> bool:
        """Sprawdza czy zgłoszenie zawiera wszystkie wymagane dane."""
        return all([self.intent, self.address, self.phone])

    def missing_fields(self) -> list[str]:
        """Zwraca listę brakujących pól wymaganych do zapisu zgłoszenia."""
        missing = []
        if not self.intent:
            missing.append("opis problemu")
        if not self.address:
            missing.append("adres")
        if not self.phone:
            missing.append("numer telefonu")
        return missing

    def to_dict(self) -> dict:
        return {
            "intent": self.intent,
            "device": self.device,
            "address": self.address,
            "phone": self.phone,
        }
