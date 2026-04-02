from fastapi import FastAPI, HTTPException, status
import json
import os
from pydantic import BaseModel
from typing import List

app = FastAPI()


# --- Models ---
class NoteCreate(BaseModel):
    title: str
    content: str


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str


# --- Helper Functions ---
FILE_NAME = 'notes.json'


def getData():
    # Create file if it doesn't exist to prevent errors
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w') as f:
            json.dump([], f)
        return []

    with open(FILE_NAME, 'r') as f:
        return json.load(f)


def saveData(notes):
    with open(FILE_NAME, 'w') as f:
        json.dump(notes, f, indent=4)


# --- Routes ---

@app.get("/")
def greet():
    return {"message": "Mini Notes API is Running !!"}


@app.get("/notes", response_model=List[NoteResponse])
def get_all_notes():
    return getData()


@app.get("/notes/{id}", response_model=NoteResponse)
def get_note_by_id(id: int):
    notes = getData()
    for note in notes:
        if note["id"] == id:  # JSON data is a list of dicts, use ["id"]
            return note
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Note with id {id} not found"
    )


@app.post("/create", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate):
    notes = getData()

    # Calculate new ID safely
    new_id = 1 if not notes else notes[-1]["id"] + 1

    new_note = {
        "id": new_id,
        "title": note.title,
        "content": note.content
    }

    notes.append(new_note)
    saveData(notes)
    return new_note


@app.delete("/delete/{id}")
def delete_note(id: int):
    notes = getData()

    # Check if exists and filter out the one to delete
    original_length = len(notes)
    notes = [n for n in notes if n["id"] != id]

    if len(notes) == original_length:
        raise HTTPException(status_code=404, detail="Note not found")

    saveData(notes)
    return {"message": f"Note {id} deleted successfully"}