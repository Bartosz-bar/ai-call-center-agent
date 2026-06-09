import json
import os

from openai import OpenAI

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    """Zwraca klienta OpenAI, inicjalizując go przy pierwszym wywołaniu (lazy init)."""
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client

_SYSTEM_PROMPT = """
Jesteś systemem ekstrakcji danych zgłoszenia serwisowego.

Wyciągnij z tekstu:
- intent  (np. awaria, reklamacja, instalacja)
- device  (np. pralka, lodówka, piec)
- address (ulica, miasto)
- phone   (numer telefonu)

Zwróć WYŁĄCZNIE poprawny JSON bez żadnych dodatkowych treści:
{
  "intent":  string | null,
  "device":  string | null,
  "address": string | null,
  "phone":   string | null
}
"""


def extract_ticket_data(text: str) -> dict:
    """
    Wysyła tekst do modelu AI i zwraca wyekstrahowane dane zgłoszenia.

    Raises:
        ValueError: gdy odpowiedź modelu nie jest poprawnym JSON-em.
    """
    response = _get_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model zwrócił niepoprawny JSON: {raw}") from exc
