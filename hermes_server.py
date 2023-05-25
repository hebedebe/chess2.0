#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from copy import deepcopy

version = 0.3

print(f"Hermes server version {version}")

default_messages = ["00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00"]

print("retrieving admin keys")
admin_keys = requests.get("https://hebedebe.github.io/chess2.0/admin_keys.json").json()["keys"]
print(admin_keys)

print("retrieving banned keys")
banned_keys = requests.get("https://hebedebe.github.io/chess2.0/banned_keys.json").json()["keys"]
print(banned_keys)

messages = {
    "main":deepcopy(default_messages)
}

keylen = 32

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def log_message(self, format, *args):
        return

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
        global messages, banned_keys, admin_keys
        if self.path == "/":
            return
        channel = self.path[1:]
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode(encoding="UTF-8")
        print(post_data)
        key = post_data[:keylen]
        #print(key)
        if key in banned_keys:
            return
        if key in admin_keys:
            msg_ = post_data[keylen+2:].split()
            #print(msg_)
            if msg_[0] == "|CMD|":
                cmd = msg_[1]
                try:
                    args = msg_[2:]
                except:
                    args = False
                if cmd == "ban":
                    for i in args:
                        banned_keys.append(i)
                        print(f"Banned ({i})")
                if cmd == "unban":
                    for i in args:
                        banned_keys.remove(i)
                        print(f"Unbanned ({i})")
                elif cmd == "listadmins":
                    for i in admin_keys:
                        messages[channel].insert(0,"00"+i)
                elif cmd == "clear":
                    if args:
                        for i in args:
                            messages[i] = deepcopy(default_messages)
                    else:
                        messages[channel] = deepcopy(default_messages)
                return

        try:
            msg_ = messages[channel]
        except:
            print(f"Created channel {channel}")
            messages[channel] = deepcopy(default_messages)
            msg_ = messages[channel]
        if key in admin_keys:
            messages[channel].insert(0,post_data[keylen:keylen+2]+"☣ "+post_data[keylen+2:])
        else:
            messages[channel].insert(0,post_data[keylen:])
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
