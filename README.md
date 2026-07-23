# AI-Demo

CRM-Webanwendung zur Verwaltung von Verkäufern (Seller) und Käufern (Buyer) mit PostgreSQL-Datenbank.

## Technologie-Stack

- **Python 3.12** + **FastAPI** (REST-API)
- **PostgreSQL 16** (Docker)
- **psycopg2** (Datenbankverbindung)
- **HTML/CSS/JS** (Web-Frontend)
- **uv** (Paketmanagement)

## Projektstruktur

```
AI-Demo/
├── service/                # Service-Code
│   ├── main.py             # FastAPI-App mit allen Endpunkten
│   ├── db.py               # Datenbankverbindung (psycopg2)
│   └── service.sh          # Service-Manager (start/stop/restart)
├── Datenbank/
│   └── create_tables.sql   # SQL-Skript zum Anlegen der Tabellen
├── static/
│   └── index.html          # Web-Frontend (Single-Page-App)
├── .venv/                  # Python-Virtual-Environment
├── pyproject.toml          # Projektkonfiguration & Dependencies
├── .python-version         # Python-Version
└── AGENTS.md               # KI-Assistenten-Konfiguration
```

## Setup

### 1. PostgreSQL (Docker)

```bash
docker run -d --name R-DB \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=postgres \
  -p 5433:5432 \
  postgres:16
```

### 2. Datenbanktabellen anlegen

```bash
docker exec -i R-DB psql -U postgres -d postgres < Datenbank/create_tables.sql
```

### 3. Abhängigkeiten installieren

```bash
uv sync
```

### 4. Service starten

```bash
# Via Service-Manager (interaktives Menü)
./service/service.sh

# Oder direkt
uvicorn service.main:app --reload --host 0.0.0.0 --port 8000
```

## API-Endpunkte

### Basis

| Methode | Pfad | Beschreibung |
|---------|------|-------------|
| GET | `/` | `{"message": "Hallo Welt"}` |
| GET | `/health` | `{"status": "healthy"}` |
| GET | `/greeting?mood=gut` | Deutsche Begrüßung mit Mood-Handling |

### Verkäufer (Seller)

| Methode | Pfad | Beschreibung |
|---------|------|-------------|
| GET | `/api/sellers` | Alle Verkäufer auflisten |
| GET | `/api/sellers/{id}` | Einzelnen Verkäufer abrufen |
| POST | `/api/sellers` | Neuen Verkäufer anlegen |
| PUT | `/api/sellers/{id}` | Verkäufer aktualisieren |
| DELETE | `/api/sellers/{id}` | Verkäufer löschen |

**Felder:** `name`, `strasse`, `plz`, `ort`, `steuernummer`, `email`

### Käufer (Buyer)

| Methode | Pfad | Beschreibung |
|---------|------|-------------|
| GET | `/api/buyers` | Alle Käufer auflisten |
| GET | `/api/buyers/{id}` | Einzelnen Käufer abrufen |
| POST | `/api/buyers` | Neuen Käufer anlegen |
| PUT | `/api/buyers/{id}` | Käufer aktualisieren |
| DELETE | `/api/buyers/{id}` | Käufer löschen |

**Felder:** `name`, `strasse`, `plz`, `ort`, `email`

### JSON-Beispiel (POST/PUT)

```json
{
  "name": "Dr. Michael Diefenbach",
  "strasse": "Bad Sodener Straße 20",
  "plz": "65843",
  "ort": "Sulzbach",
  "steuernummer": "046/812/01925",
  "email": "mc.diefenbach@t-online.de"
}
```

## Web-Frontend

Die grafische Oberfläche ist erreichbar unter:

```
http://localhost:8000/ui/
```

Funktionen:
- Tab-Wechsel zwischen Verkäufern und Käufern
- Tabellarische Auflistung aller Einträge
- Neuanlage über Formular-Modal
- Bearbeiten bestehender Einträge
- Löschen mit Bestätigung
- Toast-Benachrichtigungen bei Erfolg/Fehler

## Datenbank

### Tabelle `Seller`

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| id | SERIAL | Primärschlüssel |
| name | TEXT | Name |
| strasse | TEXT | Straße |
| plz | TEXT | Postleitzahl |
| ort | TEXT | Ort |
| steuernummer | TEXT | Steuernummer |
| email | TEXT | E-Mail |

### Tabelle `Buyer`

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| id | SERIAL | Primärschlüssel |
| name | TEXT | Name |
| strasse | TEXT | Straße |
| plz | TEXT | Postleitzahl |
| ort | TEXT | Ort |
| email | TEXT | E-Mail |

## Umgebungsvariablen

Die Datenbankverbindung kann über `.env` oder Umgebungsvariablen konfiguriert werden:

| Variable | Standard | Beschreibung |
|----------|----------|-------------|
| `DB_HOST` | `localhost` | Datenbank-Host |
| `DB_PORT` | `5433` | Datenbank-Port |
| `DB_USER` | `postgres` | Datenbank-Benutzer |
| `DB_PASS` | `postgres` | Datenbank-Passwort |
| `DB_NAME` | `postgres` | Datenbank-Name |

## Service-Manager

Das Skript `service/service.sh` bietet ein interaktives Menü:

- **Läuft der Service:** Neu starten / Beenden
- **Gestoppt:** Starten

Ausführung:
```bash
./service/service.sh
```

## Entwicklung

Neue Pakete hinzufügen:
```bash
uv add <paketname>
```

Venv synchronisieren:
```bash
uv sync
```

Swagger-Doku: `http://localhost:8000/docs`
