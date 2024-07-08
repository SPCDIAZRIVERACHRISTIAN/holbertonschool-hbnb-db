FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && \
    apt-get install -y \
    mariadb-server \
    mariadb-client \
    gcc \
    python3-dev \
    musl-dev \
    libmariadb-dev \
    libssl-dev \
    pkg-config && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT 5000

EXPOSE $PORT

CMD gunicorn hbnb:app -w 2 -b 0.0.0.0:$PORT
