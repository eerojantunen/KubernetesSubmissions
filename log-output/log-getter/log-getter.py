from fastapi import FastAPI
import os
import requests

app = FastAPI()

directory = os.path.join('shared','files')
filePath = os.path.join(directory, 'log.txt')
config = os.path.join('config')
#filePathPong = os.path.join(directory, 'pingpong.txt')

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
        pong = requests.get("http://ping-pong-svc:2346/pingpong/pings").text
        result = (
                 f"file content: {file_content}\n"
                 f"env variable: MESSAGE={env_message}\n"
                 f"{content}\n"
                 f"Ping / Pongs: {pong}"
        )
        return result
    except Exception as e:
        return str(e) 