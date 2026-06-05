"""A tiny threaded HTTP server for tests. handler(method, path, headers, body) -> (status, dict)."""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


def start(handler):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _do(self):
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length) if length else b""
            status, payload = handler(self.command, self.path, dict(self.headers), body)
            data = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        do_GET = _do
        do_POST = _do
        do_DELETE = _do

    srv = HTTPServer(("127.0.0.1", 0), H)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"
