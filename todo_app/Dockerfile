FROM python:3.11-slim

WORKDIR /app

COPY server.py index.html ./

RUN mkdir -p /shared

CMD ["python", "server.py"]
