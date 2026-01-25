FROM python:3.13-slim

WORKDIR /mydir

COPY requirements.txt .
COPY todo_app.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "todo_app.py"]