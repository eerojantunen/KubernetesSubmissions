import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
import requests
from fastapi.staticfiles import StaticFiles


app = FastAPI()

directory = os.path.join('shared','files')
img_filePath = os.path.join(directory, 'image.jpg')
time_filePath = os.path.join(directory, 'time.txt')

app.mount("/static", StaticFiles(directory=directory), name="static")

port = int(os.getenv("PORT", 8000))

env_url = os.getenv("PICSUM_URL")
todos_url = os.getenv("TODOS_URL")

def download_image():
    response = requests.get(env_url)    
    with open(img_filePath, "wb") as f:
        f.write(response.content)
    with open(time_filePath, "w") as f:
        f.write(datetime.now().isoformat())

def get_todos():
    todos_list = requests.get(todos_url).json()

    todo_list_html = ""

    for todo in todos_list:
        todo_list_html += f"<li>{todo}</li>"
    return todo_list_html

@app.get("/", response_class=HTMLResponse)
async def root():

    if not os.path.exists(time_filePath):
        download_image()

    else:
        with open(time_filePath, "r") as f:
            time_last = datetime.fromisoformat(f.read())
        if (datetime.now() - time_last).total_seconds() > 600:
            download_image()


    return f"""
    <html>
        <body>
            <h1>The project App</h1>
            <img src="/static/image.jpg" style="max-width: 500px;">
            <form action="/todos" method="POST">
                <input type="text" name="todo" maxlength="140" required>
                <button type="submit">Create todo</button>
            </form>
            {get_todos()}
            <p>DevOps with Kubernetes 2025<p>
        </body>
    </html>
    """

print(f"Server started in port {port}")
uvicorn.run(app, host="0.0.0.0", port=port)