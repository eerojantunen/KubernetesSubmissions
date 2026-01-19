FROM python:3.11-slim

WORKDIR /mydir

COPY requirements.txt .
COPY log-getter.py .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "uvicorn log-getter:app --host 0.0.0.0 --port $PORT"]
