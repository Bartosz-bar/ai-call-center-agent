# AI Call Center Agent

Backend do obsługi zgłoszeń serwisowych przez AI — Proof of Concept.

## Architektura

```
app/
├── main.py                  # Punkt wejścia aplikacji FastAPI
├── database/
│   ├── connection.py        # Połączenie z SQLite, context manager
│   └── repository.py        # Operacje na bazie danych (TicketRepository)
├── routers/
│   └── tickets.py           # Endpointy HTTP, logika obsługi rozmowy
├── services/
│   └── ai_extractor.py      # Integracja z OpenAI — ekstrakcja danych
├── schemas/
│   └── message.py           # Modele Pydantic (request / response)
└── models/
    └── ticket.py            # Modele domenowe (Ticket, ConversationState)

tests/
├── test_models.py           # Testy jednostkowe modeli
└── test_tickets_router.py   # Testy integracyjne endpointów
```

## Wymagania

- Python 3.11+
- Klucz API OpenAI

## Uruchomienie

```bash
# 1. Utwórz i aktywuj środowisko wirtualne
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# 2. Zainstaluj zależności
pip install -r requirements.txt

# 3. Ustaw klucz API
set OPENAI_API_KEY=sk-...      # Windows
export OPENAI_API_KEY=sk-...   # macOS / Linux

# 4. Uruchom serwer
uvicorn app.main:app --reload
```

API dostępne pod: http://127.0.0.1:8000/docs

## Testy

```bash
pytest tests/ -v
```

## Endpointy

| Metoda | Ścieżka            | Opis                                      |
|--------|--------------------|-------------------------------------------|
| GET    | `/`                | Health check                              |
| POST   | `/tickets/message` | Przetworzenie wiadomości od klienta       |
| GET    | `/tickets/`        | Lista wszystkich zgłoszeń                 |
| GET    | `/tickets/{id}`    | Szczegóły zgłoszenia                      |

### POST `/tickets/message`

```json
{
  "conversation_id": "abc-123",
  "text": "Mam awarię pralki, mieszkam na ul. Kwiatowej 5 w Krakowie, tel. 500600700"
}
```

Odpowiedź gdy dane kompletne:
```json
{
  "response": "Dziękujemy. Zgłoszenie zostało przyjęte.",
  "ticket_data": {
    "intent": "awaria",
    "device": "pralka",
    "address": "ul. Kwiatowej 5, Kraków",
    "phone": "500600700"
  }
}
```

Odpowiedź gdy dane niekompletne:
```json
{
  "response": "Proszę podać: adres, numer telefonu.",
  "current_state": { "intent": "awaria", "device": "pralka", "address": null, "phone": null }
}
```

## Ograniczenia PoC

- Stan rozmów przechowywany w pamięci aplikacji (nie w Redis).
- Brak obsługi audio (STT/TTS).
- Brak integracji z telefonią (Twilio).
- SQLite zamiast PostgreSQL.

Pełna architektura produkcyjna opisana jest w dokumentacji projektu.
