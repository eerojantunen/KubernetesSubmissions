from fastapi import FastAPI
import os

app = FastAPI()

directory = os.path.join('shared','files')
filePath = os.path.join(directory, 'log.txt')
filePathPong = os.path.join(directory, 'pingpong.txt')

@app.get("/status")
def status():
    try:
        with open(filePath, "r") as f:
            content = f.read()
        with open(filePathPong, "r") as f:
            pong = f.read()
        result = f"{content} \n Ping / Pongs: {pong}"
        return result
    except Exception as e:
        return str(e) 