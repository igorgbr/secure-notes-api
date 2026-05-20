import os
from typing import List, Dict

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Secure Notes API")
APP_ENV = os.getenv("APP_ENV", "development")
API_KEY = os.getenv("API_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

app = FastAPI(title=APP_NAME)


class NoteCreate(BaseModel):
    title: str
    content: str


notes: List[Dict[str, str]] = []


@app.get("/")
def root():
    return {
        "message": f"Welcome to {APP_NAME}",
        "environment": APP_ENV
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/notes")
def list_notes():
    return {
        "items": notes,
        "total": len(notes)
    }


@app.post("/notes")
def create_note(note: NoteCreate):
    if not note.title or not note.content:
        raise HTTPException(status_code=400, detail="Title and content are required")

    new_note = {
        "title": note.title,
        "content": note.content
    }

    notes.append(new_note)

    return {
        "message": "Note created successfully",
        "note": new_note
    }


@app.get("/debug")
def debug_info():
    if not DEBUG:
        raise HTTPException(status_code=403, detail="Debug mode disabled")

    return {
        "app_name": APP_NAME,
        "environment": APP_ENV,
        "api_key": API_KEY,
        "debug": DEBUG
    }