import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
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
todos_health_url = os.getenv("TODOS_HEALTH_URL")
todos_done_url = os.getenv("TODOS_DONE_URL")

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
        todo_list_html += (
            f"<li>{todo['content']} "
            f"<button onclick=\"markDone({todo['id']})\">Mark as done</button>"
            f"</li>"
        )
    return todo_list_html

def get_done():
    done_list = requests.get(todos_done_url).json()
    done_list_html = ""

    for done in done_list:
        done_list_html += f"<li>{done}</li>"
    return done_list_html

@app.get("/healthz")
def healthz():
    try:
        todo_status = requests.get(todos_health_url, timeout=2).status_code
    except Exception:
        return Response(status_code=500)
    if todo_status == 200:
        return Response(status_code=200)
    return Response(status_code=500)

@app.post("/markdone/{id}")
def markdone(id):
    try:
        url = f"{todos_url}/{id}/done"
        markdone_status = requests.put(url)
        return Response(status_code=markdone_status.status_code)
    except Exception:
        return Response(status_code=500)






@app.get("/", response_class=HTMLResponse)
def root():
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
                <script>
                    async function markDone(todoId) {{
                        const response = await fetch('/markdone/' + todoId, {{
                            method: 'POST',
                        }});
                        if (response.ok) {{
                            location.reload();
                        }} else {{
                            alert('Failed to update todo');
                        }}
                    }}
                </script>
                
                <h1>The project App</h1>
                <img src="/static/image.jpg" style="max-width: 500px;">
                
                <form action="/todos" method="POST">
                    <input type="text" name="todo" maxlength="140" required>
                    <button type="submit">Create todo</button>
                </form>
                
                <h2>Todo</h2>
                {get_todos()}
                <h2>Done</h2>
                {get_done()}
                
                <p>DevOps with Kubernetes 2025 University of Helsinki - gitops test =)</p>
            </body>
        </html>
        """


print(f"Server started in port {port}")
uvicorn.run(app, host="0.0.0.0", port=port)