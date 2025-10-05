from pydantic import BaseModel

class NoteCreate(BaseModel):
    chat_id: int
    note: str

class NoteDel(BaseModel):
    chat_id: int
    note_id: int