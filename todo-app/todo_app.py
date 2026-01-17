import os
import uvicorn
from fastapi import FastAPI


app = FastAPI()

port = int(os.getenv("PORT", 8000))

@app.get("/")
async def root():
    return {"message": "hello"}

print(f"Server started in port {port}")
uvicorn.run(app, host="0.0.0.0", port=port)