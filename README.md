# AI Call Center Agent

Proof of Concept aplikacji wykorzystującej FastAPI oraz OpenAI API do automatycznej obsługi zgłoszeń serwisowych.

System analizuje wiadomości użytkownika, identyfikuje kluczowe informacje (typ zgłoszenia, urządzenie, adres oraz numer telefonu), zarządza stanem rozmowy i zapisuje kompletne zgłoszenia w bazie danych.


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

Projekt ma charakter demonstracyjny i został przygotowany jako Proof of Concept.

Obecna wersja nie obejmuje:

* przechowywania stanu rozmowy w Redis,
* obsługi audio (STT/TTS),
* integracji z telefonią (np. Twilio),
* uwierzytelniania użytkowników,
* wdrożenia produkcyjnego i monitoringu aplikacji.

