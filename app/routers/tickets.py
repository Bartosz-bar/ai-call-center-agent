from fastapi import APIRouter, HTTPException

from app.database.repository import TicketRepository
from app.models.ticket import ConversationState, Ticket
from app.schemas.message import MessageRequest, TicketListResponse, TicketRecord, TicketResponse
from app.services.ai_extractor import extract_ticket_data

router = APIRouter(prefix="/tickets", tags=["tickets"])

_repository = TicketRepository()

# Stan rozmów przechowywany w pamięci (PoC).
# W środowisku produkcyjnym należy zastąpić Redis.
_conversation_states: dict[str, ConversationState] = {}


@router.post("/message", response_model=TicketResponse)
def handle_message(message: MessageRequest) -> TicketResponse:
    """
    Przetwarza wiadomość od klienta.

    - Ekstrauje dane zgłoszenia przy pomocy AI.
    - Aktualizuje stan rozmowy.
    - Zapisuje zgłoszenie gdy dane są kompletne.
    - Pyta o brakujące dane gdy zgłoszenie jest niekompletne.
    """
    state = _get_or_create_state(message.conversation_id)

    ai_data = extract_ticket_data(message.text)
    state.update(ai_data)

    if state.is_complete():
        return _save_and_confirm(message.conversation_id, state)

    return TicketResponse(
        response=f"Proszę podać: {', '.join(state.missing_fields())}.",
        current_state=state.to_dict(),
    )


@router.get("/", response_model=TicketListResponse)
def list_tickets() -> TicketListResponse:
    """Zwraca listę wszystkich zapisanych zgłoszeń."""
    tickets = _repository.get_all()
    records = [
        TicketRecord(
            id=t.id,
            conversation_id=t.conversation_id,
            intent=t.intent,
            address=t.address,
            phone=t.phone,
            device=t.device,
        )
        for t in tickets
    ]
    return TicketListResponse(tickets=records, total=len(records))


@router.get("/{ticket_id}", response_model=TicketRecord)
def get_ticket(ticket_id: int) -> TicketRecord:
    """Zwraca szczegóły zgłoszenia o podanym id."""
    ticket = _repository.get_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Zgłoszenie nie istnieje.")
    return TicketRecord(
        id=ticket.id,
        conversation_id=ticket.conversation_id,
        intent=ticket.intent,
        address=ticket.address,
        phone=ticket.phone,
        device=ticket.device,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_or_create_state(conversation_id: str) -> ConversationState:
    if conversation_id not in _conversation_states:
        _conversation_states[conversation_id] = ConversationState()
    return _conversation_states[conversation_id]


def _save_and_confirm(conversation_id: str, state: ConversationState) -> TicketResponse:
    ticket = Ticket(
        conversation_id=conversation_id,
        intent=state.intent,
        address=state.address,
        phone=state.phone,
        device=state.device,
    )
    _repository.save(ticket)
    _conversation_states.pop(conversation_id, None)

    return TicketResponse(
        response="Dziękujemy. Zgłoszenie zostało przyjęte.",
        ticket_data=state.to_dict(),
    )
