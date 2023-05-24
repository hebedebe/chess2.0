#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from copy import deepcopy

default_messages = ["00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00"]

messages = {
    "main":deepcopy(default_messages)
}

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        global messages
        self._set_headers()
        if self.path == "/":
            return
        channel = self.path[1:]
        try:
            msg_ = messages[channel]
        except:
            print(f"Created channel {channel}")
            messages[channel] = deepcopy(default_messages)
            msg_ = messages[channel]
        self.wfile.write(json.dumps({"messages":messages[channel][:25]}).encode(encoding="UTF-8"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        global messages
        if self.path == "/":
            return
        channel = self.path[1:]
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode(encoding="UTF-8")
        try:
            msg_ = messages[channel]
        except:
            print(f"Created channel {channel}")
            messages[channel] = deepcopy(default_messages)
            msg_ = messages[channel]
        messages[channel].insert(0,post_data)
        self._set_headers()

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
