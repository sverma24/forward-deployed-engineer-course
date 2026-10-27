"""F1 your turn, solved: a /time path that answers with the current time, and 404 for anything else.

Run:  python3 exercises/solutions/part2/f01/hello_server.py   then   curl -i localhost:8081/time
"""

from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8081


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/hello":
            body, status = "Hello! The server got your request.\n", 200
        elif self.path == "/time":
            body, status = f"The time here is {datetime.now():%H:%M}.\n", 200
        else:
            body, status = "Nothing lives at that address.\n", 404
        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body.encode())
        print(f"{self.command} {self.path} -> {status}")

    def log_message(self, *args):
        pass


HTTPServer(("localhost", PORT), Handler).serve_forever()
