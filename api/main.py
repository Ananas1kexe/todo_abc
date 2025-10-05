from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import aiosqlite
from .models import NoteCreate, NoteDel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-vercel-app.vercel.app"],  # домен веба
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DB_PATH = "db/main.db"

@app.post("/create")
async def create(data: NoteCreate):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            chat_id INTEGER,
            note_id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT
            )
        """)
        await db.execute("INSERT INTO notes (chat_id, note) VALUES (?, ?)", data.chat_id, data.note)
        cursor = await db.execute("SELECT last_insert_rowid()")
        note_id = (await cursor.fetchone())[0]
        await db.commit()
    return {"status": "success",  "note_id": note_id}

@app.post("/delete")
async def delete(data: NoteDel):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT note_id FROM notes WHERE chat_id = ?", (data.chat_id,))
        notes = cursor.fetchall()
        if any(data.note_id == note[0] for note in notes):
            await db.execute("DELETE FROM notes WHERE chat_id = ? AND note_id = ?", (data.chat_id, data.note_id))
            await db.commit()
            return {"success": "success"}
        else:
            return HTTPException(status_code=404, detail="not found")
        
@app.get("notes/{chat_id}")
async def notes(chat_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT note_id FROM notes WHERE chat_id = ?", (chat_id,))
        notes = cursor.fetchall()
        return {"notes": [{"note_id": nid, "note": note} for nid, note in notes]}
    