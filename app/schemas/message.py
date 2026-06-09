from pydantic import BaseModel, Field
from typing import Optional


class MessageRequest(BaseModel):
    conversation_id: str = Field(..., description="Unikalny identyfikator rozmowy")
    text: str = Field(..., min_length=1, description="Treść wiadomości od klienta")


class TicketResponse(BaseModel):
    response: str
    ticket_data: Optional[dict] = None
    current_state: Optional[dict] = None


class TicketRecord(BaseModel):
    id: int
    conversation_id: str
    intent: str
    address: str
    phone: str
    device: Optional[str] = None


class TicketListResponse(BaseModel):
    tickets: list[TicketRecord]
    total: int
