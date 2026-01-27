from fastapi import FastAPI
from fastapi.responses import Response
from random import choices
import string
from datetime import datetime
import os
from sqlalchemy import create_engine, text

app = FastAPI()

directory = os.path.join('shared','files')
filePathPong = os.path.join(directory, 'pingpong.txt')
db_url = "postgresql://postgres:pass123@postgres-svc:5432/postgres"

engine = create_engine(db_url)
with engine.connect() as conn:
    conn.execute(text(
        "CREATE TABLE IF NOT EXISTS counter (id INT PRIMARY KEY, value INT)"))
    conn.execute(text(
        "INSERT INTO counter (id, value) VALUES (1, 0) ON CONFLICT DO NOTHING"))
    conn.commit()

def handle_pingpong():
    with engine.connect() as conn:
        result = conn.execute(text(
            "UPDATE counter SET value = value + 1 WHERE id = 1 RETURNING value"
        ))
        count = result.fetchone()[0]
        conn.commit()
        return count

@app.get("/healthz")
def healthz():

    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        return Response(status_code=200)
    except Exception:
        return Response(status_code=500)

@app.get("/pings")
def pings():
    pong_counter = handle_pingpong()
    return f"{pong_counter}"

@app.get("/")
def pingpong():
    pong_counter = handle_pingpong()
    return f"pong {pong_counter}"