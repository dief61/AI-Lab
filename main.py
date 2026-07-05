# main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/greeting")
def greeting(mood: str | None = None):
    response = "Hallo Welt! Wie geht es dir?"
    if mood:
        mood_lower = mood.lower()
        if mood_lower == "gut":
            response = "Das freut mich!"
        elif mood_lower == "schlecht":
            response = "Das tut mir leid."
        else:
            response = f"Hallo Welt! Du sagtest: '{mood}'. Wie geht es dir?" # Fallback for unknown input

    return {"message": response}
