from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


notes = []


class NoteModel(BaseModel):
    id: str
    title: str
    content: str


@app.get("/")
async def read_notes(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "notes": notes}
    )


@app.get("/note/{note_id}")
async def read_note(request: Request, note_id: str):
    note = next((note for note in notes if note["id"] == note_id), None)
    if not note:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse(
        "detail.html", {"request": request, "note": note}
    )


@app.post("/note/create")
async def create_note(
    title: str = Form(...), content: str = Form(...)
):
    note = NoteModel(id=str(uuid4()), title=title, content=content)
    notes.append(note.dict())
    return RedirectResponse("/", status_code=302)


@app.post("/note/delete/{note_id}")
async def delete_note(note_id: str):
    global notes
    notes = [note for note in notes if note["id"] != note_id]
    return RedirectResponse("/", status_code=302)
