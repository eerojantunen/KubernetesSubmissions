import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from datetime import datetime
import requests

app = FastAPI()

directory = os.path.join('shared','files')

port = int(os.getenv("PORT", 8000))


todo_list = ["Learn JacaScript", "Learn React", "Build a project"]


@app.get("/todos")
async def get_todos():
    global todo_list
    return todo_list

@app.post("/todos")
async def post_todos(request: Request):
    global todo_list
    data = await request.form()
    todo = data.get("todo")
    todo_list.append(todo)
    return RedirectResponse(url="/", status_code=303)


uvicorn.run(app, host="0.0.0.0", port=port)