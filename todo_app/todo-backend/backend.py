from flask import Flask, request, jsonify
import psycopg2
import logging
import os

# Configure logging to stdout (required for Promtail/Loki)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "todo-postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "tododb")
DB_USER = os.getenv("DB_USER", "todo")
DB_PASSWORD = os.getenv("DB_PASSWORD", "supersecret")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Initialize DB (create table if not exists)
with get_conn() as conn:
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            text VARCHAR(140) NOT NULL
        );
        """)
    conn.commit()

@app.route("/api/todos", methods=["GET"])
def get_todos():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT text FROM todos ORDER BY id;")
            rows = cur.fetchall()
    return jsonify([r[0] for r in rows])

@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    todo = data.get("todo", "").strip()

    # Log incoming request
    logging.info(f"Received new todo: {todo}")

    if not todo:
        logging.warning("Rejected empty todo.")
        return jsonify({"error": "Todo cannot be empty"}), 400

    if len(todo) > 140:
        logging.warning(f"Rejected todo exceeding 140 characters: {todo}")
        return jsonify({"error": "Todo too long"}), 400

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO todos (text) VALUES (%s);", (todo,))
        conn.commit()

    logging.info(f"Todo added: {todo}")
    return jsonify({"success": True, "todo": todo}), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


