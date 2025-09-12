import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys

port = int(os.environ.get("PORT", 8080))

print(f"Server started in port {port}")
sys.stdout.flush()

HTTPServer(("", port), SimpleHTTPRequestHandler).serve_forever()
