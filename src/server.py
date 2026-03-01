#!/usr/bin/env python3
"""Simple HTTP server for XRP Alert Bot"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        if self.path == "/":
            response = {"message": "Hello World from XRP Alert Bot"}
        elif self.path == "/health":
            response = {"status": "healthy"}
        else:
            response = {"error": "Not found", "path": self.path}
        
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    print("Starting XRP Alert Bot server on port 8000...")
    server = HTTPServer(("0.0.0.0", 8000), SimpleHandler)
    server.serve_forever()