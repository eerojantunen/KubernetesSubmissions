from fastapi import FastAPI
from random import choices
import string
from datetime import datetime
import os

app = FastAPI()

pong_counter = 0
directory = os.path.join('shared','files')
filePathPong = os.path.join(directory, 'pingpong.txt')


def handle_pingpong():
    global pong_counter
    pong_counter += 1
    try:
        with open(filePathPong, "w") as f:
            f.write(str(pong_counter))
    except Exception as e:
        return str(e) + "HELLO"
    return pong_counter


@app.get("/pings")
def pings():
    pong_counter = handle_pingpong()
    return f"{pong_counter}"

@app.get("/pingpong")
def pingpong():
    pong_counter = handle_pingpong()
    return f"pong {pong_counter}"