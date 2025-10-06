import os
import sys
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta
import json
import requests

port = int(os.environ.get("PORT", 8080))

IMAGE_DIR = "/shared"
IMAGE_PATH = os.path.join(IMAGE_DIR, "image.jpg")
TIMESTAMP_PATH = os.path.join(IMAGE_DIR, "timestamp.txt")

TODO_BACKEND = os.environ.get("BACKEND_URL", "http://todo-backend-service/api/todos")

os.makedirs(IMAGE_DIR, exist_ok=True)

def fetch_new_image():
    urllib.request.urlretrieve("https://picsum.photos/600", IMAGE_PATH)
    with open(TIMESTAMP_PATH, "w") as f:
        f.write(datetime.utcnow().isoformat())
    sys.stdout.flush()

def get_cached_image():
    if not os.path.exists(IMAGE_PATH) or not os.path.exists(TIMESTAMP_PATH):
        fetch_new_image()
    else:
        with open(TIMESTAMP_PATH, "r") as f:
            last_fetch = datetime.fromisoformat(f.read().strip())
        if datetime.utcnow() - last_fetch > timedelta(minutes=10):
            fetch_new_image()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            with open("index.html", "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(content)

        elif self.path == "/image":
            get_cached_image()
            with open(IMAGE_PATH, "rb") as f:
                img = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg")
            self.end_headers()
            self.wfile.write(img)

        elif self.path == "/api/todos":  # Proxy GET to backend
            resp = requests.get(TODO_BACKEND)
            self.send_response(resp.status_code)
            self.end_headers()
            self.wfile.write(resp.content)

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/todos":  # Proxy POST to backend
            length = int(self.headers.get("Content-Length"))
            data = self.rfile.read(length)
            resp = requests.post(TODO_BACKEND, data=data, headers={"Content-Type": "application/json"})
            self.send_response(resp.status_code)
            self.end_headers()
            self.wfile.write(resp.content)
        else:
            self.send_response(404)
            self.end_headers()

print(f"Server started in port {port}")
sys.stdout.flush()
HTTPServer(("", port), Handler).serve_forever()


