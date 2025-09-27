from http.server import BaseHTTPRequestHandler, HTTPServer
import os

counter = 0

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global counter
        if self.path == "/pingpong":
            counter += 1
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"pong {counter}".encode())
        elif self.path == "/pings":  # new endpoint for Log-output
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(counter).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Server running on port {port}")
    HTTPServer(("", port), Handler).serve_forever()
