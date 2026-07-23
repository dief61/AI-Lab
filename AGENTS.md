# AGENTS.md

## Tech Stack
- Python + FastAPI — app in `service/main.py`, instance named `app`
- **`uv`** for package management, `.venv` im Projektverzeichnis
- PostgreSQL in Docker als `R-DB` (Port 5433)

## Commands
- **Service starten:** `./service/service.sh` (interaktives Menü)
- **Dev server direkt:** `uvicorn service.main:app --reload --host 0.0.0.0 --port 8000`
- **Package hinzufügen:** `uv add <pkg>`
- **venv synchronisieren:** `uv sync`
- **SQL ausführen:** `docker exec -i R-DB psql -U postgres -d postgres < Datenbank/create_tables.sql`
- **Keine Tests, kein CI, kein pre-commit**

## Projektstruktur
```
AI-Demo/
├── service/          # Service-Code (main.py, db.py, service.sh)
├── Datenbank/        # SQL-Skripte
├── static/           # Web-Frontend (HTML/CSS/JS)
├── .venv/            # Python-Venv (automatisch via uv)
├── pyproject.toml    # Projekt-Konfiguration & Dependencies
└── .python-version   # Python-Version
```

## API Routes
- `GET /` — `{"message": "Hallo Welt"}`
- `GET /greeting?mood=...` — Deutsche Begrüßung mit Mood-Handling
- `GET /health` — `{"status": "healthy"}`
- `GET/POST /api/sellers` — CRUD Verkäufer
- `GET/PUT/DELETE /api/sellers/{id}` — CRUD Verkäufer
- `GET/POST /api/buyers` — CRUD Käufer
- `GET/PUT/DELETE /api/buyers/{id}` — CRUD Käufer
- `GET /ui/` — Grafische Oberfläche

## Conventions
- DB-Queries: `psycopg2` (connection via `service/db.py`)
- `.env` ist gitignored — DB-Zugangsdaten dort hinterlegen
- Dies ist ein leichtes Demo-Projekt; einfach halten
