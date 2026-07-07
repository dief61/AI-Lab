# AI-Lab 🚀

Dieses Projekt ist eine KI-gestützte Entwicklungsumgebung (Vibe Coding Lab) innerhalb der WSL2, betrieben mit **Aider** und **Google Gemini 2.5**, verwaltet über das moderne Python-Tool **`uv`**.

---

## 1. Voraussetzungen & API-Key einrichten

Der Google Gemini API-Key muss in der Linux-Umgebung hinterlegt sein. Falls noch nicht geschehen, wird der Key dauerhaft in der `~/.bashrc` gespeichert:

```bash
# Key dauerhaft hinzufügen
echo 'export GEMINI_API_KEY="DEIN_GEMINI_API_KEY"' >> ~/.bashrc

# Konfiguration neu laden
source ~/.bashrc
```

---

## 2. Projekt-Infrastruktur starten (uv & venv)

Da wir die Abhängigkeiten isoliert und performant halten wollen, nutzen wir `uv` für das virtuelle Environment und das Paketmanagement.

```bash
# 1. In das Projektverzeichnis wechseln
cd ~/workspace/projects/AI-Demo

# 2. Virtuelle Umgebung erstellen (falls nicht vorhanden)
uv venv

# 3. Virtuelle Umgebung aktivieren
source .venv/bin/activate

# 4. Abhängigkeiten blitzschnell installieren
uv pip install fastapi uvicorn jinja2
```

---

## 3. Aider (KI-Assistent) starten

Um mit Gemini Code zu generieren und automatische Git-Commits zu nutzen, wird Aider mit dem stabilen Gemini-Modell-Pfad aufgerufen:

```bash
aider --model gemini/gemini-2.5-flash
```

*Hinweis: Bestätige beim ersten Start die Abfrage, `.aider*` zur `.gitignore` hinzuzufügen mit **`Y`** (Yes), um den Git-Verlauf sauber zu halten.*

---

## 4. FastAPI-Service (Server) starten

Da die WSL2 in einem eigenen Netzwerksegment läuft, muss der Uvicorn-Server an `0.0.0.0` gebunden werden, damit er vom Windows-Browser aus erreichbar ist.

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Server im Windows-Browser aufrufen:
1. Ermittle die IP-Adresse deiner WSL2-Instanz in einem separaten Terminal:
   ```bash
   hostname -I
   ```
2. Öffne deinen Windows-Browser und rufe die Adresse auf (Beispiel):
   `http://<DEINE-WSL-IP>:8000`
