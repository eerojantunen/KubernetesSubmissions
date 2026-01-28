import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response
from datetime import datetime
import requests
from sqlalchemy import create_engine, text
import nats

app = FastAPI()

directory = os.path.join('shared','files')

port = int(os.getenv("PORT", 8000))
DB_URL = (os.getenv("DB_URL"))

todo_list = ["Learn JacaScript", "Learn React", "Build a project"]
redirect_url = os.getenv("REDIRECT_URL")

engine = create_engine(DB_URL)


def init_db():
    try:
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
                    "CREATE TABLE IF NOT EXISTS todos (id SERIAL PRIMARY KEY, todo TEXT, status INTEGER DEFAULT 0)"))
                conn.commit()
                for todo in todo_list:
                    conn.execute(
                        text("INSERT INTO todos (todo) VALUES (:todo) ON CONFLICT DO NOTHING"),
                        {"todo": todo})        
                    conn.commit()
            conn.execute(text("""
                ALTER TABLE todos ADD COLUMN IF NOT EXISTS status INTEGER DEFAULT 0
            """))
            conn.commit()
    except Exception:
        pass

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/healthz")
def healthz():
    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        return Response(status_code=200)
    except Exception:
        return Response(status_code=500)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/todos")
def get_todos():
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT id, todo FROM todos WHERE status=0 ORDER BY id ASC"
        ))
    todos_list = [{"id": row.id, "content": row.todo} for row in result]
    return todos_list

@app.get("/done")
def get_done():
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT todo FROM todos WHERE status=1 ORDER BY id ASC"
        ))
    todos_list = [row[0] for row in result]
    return todos_list

@app.put("/todos/{target_id}/done")
async def update_done_status(target_id):
    with engine.connect() as conn:
        result = conn.execute(text(
            "UPDATE todos SET status=1 WHERE id=:target_id"
        ), {"target_id":target_id})
        conn.commit()
        if result.rowcount == 0:
            return Response(status_code=404)
    try:
        nc = await nats.connect("nats://my-nats:4222")
        await nc.publish("todos", f"Todo {target_id} marked as done".encode())
        await nc.close()
    except Exception as e:
        pass
    return Response(status_code=200)

@app.post("/todos")
async def post_todos(request: Request):
    data = await request.form()
    todo = data.get("todo")
    if len(todo) > 140:
        print("Todo is over 140 characters, rejected")
        print(f"Rejected todo: {todo}")
        return RedirectResponse(url=redirect_url, status_code=303)
    print(f"Recieved valid todo {todo}")
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO todos (todo) VALUES (:todo)"),
            {"todo": todo}
        )
        conn.commit()
    print(f"todo: {todo} added to database")
    try:
        nc = await nats.connect("nats://my-nats:4222")
        await nc.publish("todos", f"Todo: {todo}".encode())
        await nc.close()
    except Exception as e:
        pass
    return RedirectResponse(url=redirect_url, status_code=303)


uvicorn.run(app, host="0.0.0.0", port=port)