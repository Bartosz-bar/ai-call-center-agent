from fastapi import FastAPI

from app.database.connection import init_db
from app.routers import tickets

app = FastAPI(
    title="AI Call Center Agent",
    description="Backend do obsługi zgłoszeń serwisowych przez AI.",
    version="1.0.0",
)

# Inicjalizacja bazy przy starcie aplikacji
init_db()

# Rejestracja routerów
app.include_router(tickets.router)


@app.get("/", tags=["health"])
def health_check() -> dict:
    """Endpoint sprawdzający stan aplikacji."""
    return {"status": "ok", "message": "AI Call Center Agent działa poprawnie."}
