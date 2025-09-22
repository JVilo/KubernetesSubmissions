from http.server import BaseHTTPRequestHandler, HTTPServer
import os

log_file = "/shared/log.txt"
counter_file = "/shared/counter.txt"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            # Read the last line from the log file
            random_string_line = ""
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    lines = f.readlines()
                    if lines:
                        random_string_line = lines[-1].strip()

            # Read the ping-pong counter
            counter_value = "0"
            if os.path.exists(counter_file):
                with open(counter_file, "r") as f:
                    counter_value = f.read().strip()

            response = f"{random_string_line}\nPing / Pongs: {counter_value}"

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"[DEBUG] Starting server on port {port}")
    HTTPServer(("", port), Handler).serve_forever()

