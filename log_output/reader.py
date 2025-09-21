from http.server import BaseHTTPRequestHandler, HTTPServer

file_path = "/shared/log.txt"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Log file not found")

if __name__ == "__main__":
    port = 8080
    HTTPServer(("", port), Handler).serve_forever()
