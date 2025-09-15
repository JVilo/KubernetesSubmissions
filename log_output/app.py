import sys
import time
import uuid
import threading
from datetime import datetime, UTC
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

random_string = str(uuid.uuid4())
startup_timestamp = datetime.now(UTC).isoformat(timespec='milliseconds')

def log_status():
    while True:
        now = datetime.now(UTC).isoformat(timespec='milliseconds')
        print(f"{now}: {random_string}")
        sys.stdout.flush()
        time.sleep(5)

threading.Thread(target=log_status, daemon=True).start()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open("index.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"index.html not found")
        elif self.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "timestamp": startup_timestamp,
                "random_string": random_string
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Server running on port {port}")
    sys.stdout.flush()
    HTTPServer(("", port), Handler).serve_forever()

