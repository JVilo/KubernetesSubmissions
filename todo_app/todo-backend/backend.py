from flask import Flask, request, jsonify
import psycopg2
import logging
import os

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

# Initialize DB
with get_conn() as conn:
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            text VARCHAR(140) NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        );
        """)
    conn.commit()

# Get all todos
@app.route("/api/todos", methods=["GET"])
def get_todos():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, text, done FROM todos ORDER BY id;")
            rows = cur.fetchall()

    todos = [{"id": r[0], "text": r[1], "done": r[2]} for r in rows]
    return jsonify(todos)

# Add new todo
@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    todo = data.get("todo", "").strip()

    if not todo:
        return jsonify({"error": "Todo cannot be empty"}), 400
    if len(todo) > 140:
        return jsonify({"error": "Todo too long"}), 400

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO todos (text) VALUES (%s) RETURNING id;",
                (todo,)
            )
            todo_id = cur.fetchone()[0]
        conn.commit()

    return jsonify({
        "id": todo_id,
        "text": todo,
        "done": False
    }), 201

# Mark todo as done
@app.route("/api/todos/<int:todo_id>/done", methods=["POST"])
def mark_done(todo_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE todos SET done = TRUE WHERE id = %s;",
                (todo_id,)
            )
        conn.commit()

    return jsonify({"success": True}), 200

@app.route("/ready", methods=["GET"])
def ready():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        return jsonify({"status": "ready"}), 200
    except Exception as e:
        return jsonify({"status": "not ready", "error": str(e)}), 503

@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"status": "alive"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
