FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /data

ENV PYTHONUNBUFFERED=1
ENV PORT=8787
ENV DATA_DIR=/data
ENV SOCKS5_PORT=1081

EXPOSE 8787 1081

VOLUME ["/data"]

CMD ["python", "main.py"]
