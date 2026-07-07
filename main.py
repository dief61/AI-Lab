# main.py

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(
    title="Hallo Welt API",
    description="A simple German greeting service",
    version="1.0.0"
)

# Mount static files directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Setup templates directory
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
if not os.path.exists(templates_dir):
    os.makedirs(static_dir)

templates = Jinja2Templates(directory=templates_dir)


@app.get("/")
def index_page():
    """Serve the main HTML page with greeting form."""
    return templates.TemplateResponse("index.html", {
        "request": None,
        "title": "Hallo Welt API"
    })


@app.get("/greeting")
def greeting(mood: str | None = Query(None, description="Optional mood parameter (gut/schlecht/other)")):
    """
    Greeting endpoint that responds based on the provided mood.
    
    - If no mood is provided: returns default German greeting
    - If mood is "gut": returns positive response
    - If mood is "schlecht": returns empathetic response
    - For other moods: echoes back the input and asks how they are
    
    Args:
        mood (str | None): Optional mood parameter. Case-insensitive matching.
    
    Returns:
        dict: JSON response with message key containing German greeting text.
    """
    # Default greeting when no mood is provided or unknown
    default_response = "Hallo Welt! Wie geht es dir?"
    
    if not mood:
        return {"message": default_response}
    
    mood_lower = mood.lower()
    
    if mood_lower == "gut":
        response = "Das freut mich!"
    elif mood_lower == "schlecht":
        response = "Das tut mir leid."
    else:
        # Fallback for unknown input - echo back and ask how they are
        response = f"Hallo Welt! Du sagtest: '{mood}'. Wie geht es dir?"
    
    return {"message": response}


@app.get("/health")
def health_check():
    """Health check endpoint for service monitoring."""
    return {"status": "healthy"}


@app.get("/api/greeting")
def api_greeting(mood: str | None = Query(None)):
    """API endpoint for the greeting service."""
    return greeting(mood=mood)
