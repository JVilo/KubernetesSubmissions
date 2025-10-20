from flask import Flask
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "pingpongdb")
DB_USER = os.getenv("DB_USER", "pingpong")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secretpassword")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS counter (
                id SERIAL PRIMARY KEY,
                value INT DEFAULT 0
            );
        """)
        cur.execute("SELECT COUNT(*) FROM counter;")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO counter (value) VALUES (0);")
    conn.commit()

@app.route("/pingpong")
def pingpong():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE counter SET value = value + 1 WHERE id = 1 RETURNING value;")
            (count,) = cur.fetchone()
        conn.commit()
    return f"pong {count}\n"

@app.route("/pings")
def pings():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT value FROM counter WHERE id = 1;")
            (count,) = cur.fetchone()
    return str(count)

@app.route("/")
def index():
    return "ping-pong running\n"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Server running on port {port}")
    app.run(host="0.0.0.0", port=port)
