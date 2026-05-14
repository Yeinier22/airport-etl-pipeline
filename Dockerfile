FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

RUN mkdir -p data/raw data/processed logs metadata

VOLUME ["/app/data", "/app/logs", "/app/metadata"]

CMD ["python", "src/main.py"]