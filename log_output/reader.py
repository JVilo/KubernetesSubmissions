from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone
import uuid
import os
import requests

random_string = str(uuid.uuid4())
startup_timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds")

PING_PONG_URL = os.environ.get("PING_PONG_URL", "http://ping-pong-service/pings")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            pong_count = "N/A"
            try:
                r = requests.get(PING_PONG_URL, timeout=2)
                pong_count = r.text.strip()
            except Exception as e:
                pong_count = f"Error: {e}"

            response = f"{startup_timestamp}: {random_string}\nPing / Pongs: {pong_count}"
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Server running on port {port}")
    HTTPServer(("", port), Handler).serve_forever()



