FROM python:3.11-slim

WORKDIR /mydir

COPY requirements.txt .
COPY log-output.py .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "uvicorn log-output:app --host 0.0.0.0 --port $PORT"]
