FROM python:3.11-slim

WORKDIR /app

COPY server.py index.html ./

RUN pip install --no-cache-dir requests

RUN mkdir -p /shared

EXPOSE 8080

CMD ["python", "server.py"]
