from fastapi import FastAPI
from random import choices
import string
from datetime import datetime

app = FastAPI()

pong_counter = 0

@app.get("/pingpong")
def pingpong():
    global pong_counter
    pong_counter += 1
    return f"pong {pong_counter}"
