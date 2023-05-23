#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

messages = ["","","","","","","","","","","","","","","","","","","",""]

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        global messages
        self._set_headers()
        if self.path == "/getmsg":
            #print(json.dumps({"messages":messages}))
            self.wfile.write(json.dumps({"messages":messages[:26]}).encode(encoding="UTF-8"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        global messages
        if self.path == "/postmsg":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)[:].decode(encoding="UTF-8")
            messages.insert(0,post_data)
            self._set_headers()
            print(post_data)

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
