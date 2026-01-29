from fastapi import FastAPI
from fastapi.responses import Response
import os
import requests

app = FastAPI()

directory = os.path.join('shared','files')
filePath = os.path.join(directory, 'log.txt')
config = os.path.join('config')
#filePathPong = os.path.join(directory, 'pingpong.txt')

@app.get("/healthz")
def healthz():
    try:
        pingpong_status = requests.get("http://ping-pong-svc:2346/healthz", timeout=2).status_code
    except Exception:
        return Response(status_code=500)
    if pingpong_status == 200:
        return Response(status_code=200)
    return Response(status_code=500)

@app.get("/")
def root():
    return "OK"

@app.get("/status")
def status():

    env_message = os.getenv("MESSAGE", "not found")        
    try:
        with open(filePath, "r") as f:
            content = f.read()
        with open("/config/information.txt", "r") as f:
            file_content = f.read().strip()
        pong = requests.get("http://ping-pong-svc:2346/pings").text
        result = (
                 f"file content: {file_content}\n"
                 f"env variable: MESSAGE={env_message}\n"
                 f"{content}\n"
                 f"Ping / Pongs: {pong}"
                 f"gitops test"
        )
        return result
    except Exception as e:
        return str(e) 