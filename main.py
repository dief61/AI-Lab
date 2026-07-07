# main.py

from fastapi import FastAPI, Query

app = FastAPI(
    title="Hallo Welt API",
    description="A simple German greeting service",
    version="1.0.0"
)


@app.get("/")
def read_root():
    """Root endpoint returning a welcome message."""
    return {"message": "Hello World"}


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
