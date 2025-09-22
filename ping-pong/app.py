from http.server import BaseHTTPRequestHandler, HTTPServer
import os

counter_file = "/shared/counter.txt"

# make sure file exists
if not os.path.exists(counter_file):
    with open(counter_file, "w") as f:
        f.write("0")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/pingpong":
            # read counter
            with open(counter_file, "r") as f:
                count = int(f.read().strip())
            count += 1
            with open(counter_file, "w") as f:
                f.write(str(count))

            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"pong {count}".encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(("", port), Handler).serve_forever()
