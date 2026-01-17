from fastapi import FastAPI
from random import choices
import string
from datetime import datetime

app = FastAPI()


@app.get("/status")
def status():
    return {
        "timestamp": datetime.now().isoformat(),
        "random string": ''.join(choices(string.ascii_uppercase + string.ascii_lowercase, k=32))
    }