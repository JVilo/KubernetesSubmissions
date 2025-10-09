FROM python:3.11-slim

WORKDIR /app
COPY backend.py .
RUN pip install flask psycopg2-binary

EXPOSE 8080
CMD ["python", "backend.py"]

