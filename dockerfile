FROM python:3.14-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "-m", "src.main" ]