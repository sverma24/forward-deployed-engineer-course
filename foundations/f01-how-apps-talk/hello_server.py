"""F1: the smallest possible web server, so you can watch a request arrive.

Run it:      python3 hello_server.py
Then visit:  http://localhost:8080/hello   (or: curl -i localhost:8080/hello)
Every request is printed here, so you can see what the browser actually sent.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8080


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"\n--> request arrived: {self.command} {self.path}")
        print(f"    from: {self.client_address[0]}   asking for host: {self.headers['Host']}")
        print(f"    sent by: {self.headers.get('User-Agent', '?')[:60]}")
        if self.path == "/hello":
            body, status = "Hello! The server got your request.\n", 200
        else:
            body, status = "Nothing lives at that address.\n", 404
        self.send_response(status)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body.encode())
        print(f"<-- replied with status {status}")

    def log_message(self, *args):   # keep the output to our own prints
        pass


print(f"Server listening on port {PORT}. Press Ctrl+C to stop.")
HTTPServer(("localhost", PORT), Handler).serve_forever()
