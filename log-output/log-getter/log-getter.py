from fastapi import FastAPI
import os
import requests

app = FastAPI()

directory = os.path.join('shared','files')
filePath = os.path.join(directory, 'log.txt')
#filePathPong = os.path.join(directory, 'pingpong.txt')


@app.get("/status")
def status():
    try:
        with open(filePath, "r") as f:
            content = f.read()
        pong = requests.get("http://ping-pong-svc:2346/pings").text
        result = f"{content} Ping / Pongs: {pong}"
        return result
    except Exception as e:
        return str(e) 