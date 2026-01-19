from fastapi import FastAPI
import os

app = FastAPI()

directory = os.path.join('files')
filePath = os.path.join(directory, 'log.txt')

@app.get("/status")
def status():
    try:
        with open(filePath, "r") as f:
            content = f.read()
        return content
    except Exception as e:
        return e