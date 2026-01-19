from fastapi import FastAPI
from random import choices
import string
from datetime import datetime
import os

app = FastAPI()

pong_counter = 0
directory = os.path.join('shared','files')
filePathPong = os.path.join(directory, 'pingpong.txt')


@app.get("/pingpong")
def pingpong():
    global pong_counter
    pong_counter += 1
    try:
        with open(filePathPong, "w") as f:
            f.write(str(pong_counter))
    except Exception as e:
        return str(e) + "HELLO"
    return f"pong {pong_counter}"
