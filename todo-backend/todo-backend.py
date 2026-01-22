import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from datetime import datetime
import requests
from sqlalchemy import create_engine, text

app = FastAPI()

directory = os.path.join('shared','files')

port = int(os.getenv("PORT", 8000))
DB_URL = (os.getenv("DB_URL"))

todo_list = ["Learn JacaScript", "Learn React", "Build a project"]
redirect_url = os.getenv("REDIRECT_URL")

engine = create_engine(DB_URL)

def init_db():
    with engine.connect() as conn:
        exists = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'todos'
            );
        """)).scalar()
        
        if not exists:
            conn.execute(text(
                "CREATE TABLE IF NOT EXISTS todos (id SERIAL PRIMARY KEY, todo TEXT)"))
            conn.commit()
            for todo in todo_list:
                conn.execute(
                    text("INSERT INTO todos (todo) VALUES (:todo) ON CONFLICT DO NOTHING"),
                    {"todo": todo})        
                conn.commit()

init_db()

@app.get("/todos")
async def get_todos():
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT todo FROM todos ORDER BY id ASC"
        ))
    todos_list = [row[0] for row in result]
    return todos_list

@app.post("/todos")
async def post_todos(request: Request):
    data = await request.form()
    todo = data.get("todo")
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO todos (todo) VALUES (:todo)"),
            {"todo": todo}
        )
        conn.commit()

    return RedirectResponse(url=redirect_url, status_code=303)


uvicorn.run(app, host="0.0.0.0", port=port)