print("Importing libraries...")

import os

try:
    import requests
except:
    print("Installing requests module")
    os.system("pip3 install requests")
    import requests
import time
import pickle
try:
    import curses
except:
    print("Installing windows-curses")
    os.system("pip3 install windows-curses")
    import curses
try:
    import colorama
except:
    print("Installing colorama")
    os.system("pip3 install colorama")
    import colorama
import threading
try:
    import urllib.request
except:
    print("Installing urllib")
    os.system("pip3 install urllib")
    import urllib.request
from copy import deepcopy
import random
import atexit
import sys

colorama.init()

version = 0.5

print(f"Hermes version {version}")

print("Retrieving JSON data...")

data = requests.get("https://hebedebe.github.io/chess2.0/hermes_data.json").json()

servers = data["servers"]

print(f"Server list recieved")

patchnotes = data["patchnotes"]

print(f"Downloaded notifications")

latestver = data["latestversion"]
latestverstable = data["stable"]
latestverurgent = data["urgent"]

print(f"Got latest version ({latestver})")

if (latestver > version):
    if latestverurgent:
        doinstall = True
    else:
        print(f"Your installation of Hermes (V{version}) is outdated. Install V{latestver}? [Y/n] (WINDOWS ONLY)")
        if not latestverstable:
            print(f"{colorama.Back.RED}WARNING: Version {latestver} of Hermes is unstable.{colorama.Back.RESET}")
        doinstall = ("y" in input("> "))
    if doinstall:
        print(f"Downloading Hermes V{latestver}... (this may take a while)")
        urllib.request.urlretrieve("https://hebedebe.github.io/chess2.0/Hermes.exe", "Hermes.exe")
        print("Close and reopen the program to complete the installation.")
        while True:
            pass

colour = str(random.randint(2,32))

if len(colour) < len("10"):
    colour = "0"+colour

domain = None

connected = False

for i in servers:
    domain = i
    print(f"Attempting connection to server {domain}... ({servers.index(i)+1} of {len(servers)})")
    try:
        r_ = requests.get(domain)
        if r_.status_code != 200:
            print(f"Recieved error code <{r_.status_code}>")
        elif r_.status_code == 200:
            print(f"Connected successfully!")
            connected = True
            break
    except Exception as e:
        print("Connection failed.")
        print(e)

if not connected:
    print("\nCould not connect to any servers. Please try again later\n")
    while True:
        pass

print(f"\nNotifications\n{patchnotes}\n")

keylen = 32

try:
    if os.path.isfile("key.txt"):
        f = open("key.txt", "r")
        key = f.read()
        f.close()
    else:
        f = open("key.txt", "x")
        f.close()
        f = open("key.txt", "w")
        key = ""
        for i in range(keylen):
            chnum = random.randint(33,126)
            while chnum == 34 or chnum == 96:
                chnum = random.randint(33,126)
            key = key+chr(chnum)
        f.write(key)
        f.close()
except:
    print("Key generation/detection failed.")
    key = None

print("""

Patch Notes
 - Fixed bug that causes the program to crash with invalid colour values
 - Fixed bug that causes colour indexes with more than 2 digits to bug

""")

print(f"Key: {key}\n")

username = input("Username\n> ")

channel = "main"

if len(username) > 16:
    username = username[:16]

messages = []

def get_msg():
    global domain, messages
    response = requests.get(domain+f"/{channel}")
    data = response.json()
    messages = data["messages"]

def send_msg(msg):
    global channel, messages, colour, inpt
    if msg.split()[0] == "|CMD|":
        response = requests.post(domain+f"/{channel}", data=(f"{key}{colour}{msg}".encode(encoding="UTF-8")))
        inpt = ""
        stdscr.addstr(curses.LINES-3, 0, " "*curses.COLS)
        stdscr.addstr(curses.LINES-1, 0, f"Sent admin command                                ")
    elif msg[0] != "!":
        response = requests.post(domain+f"/{channel}", data=(f"{key}{colour}[{username}] {msg}".encode(encoding="UTF-8")))
    else:
        if msg[0:4] == "!key":
            stdscr.addstr(curses.LINES-1, 0, 'Key: "'+key+'"')
        elif msg[0:8] == "!channel":
            requests.post(domain+f"/{channel}", data=(f"{key}00           ({username} left the channel.)".encode(encoding="UTF-8")))
            channel = msg[8:].strip()
            requests.post(domain+f"/{channel}", data=(f"{key}00           ({username} entered the channel.)".encode(encoding="UTF-8")))
            stdscr.addstr(curses.LINES-1, 0, f"Switched to channel {channel}                             ")
            messages = ["00Loading channel...","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00","00"]
        elif msg[0:7] == "!colour":
            colour_ = deepcopy(colour)
            colour = msg.split()[1]
            if len(colour) < len("10"):
                colour = "0"+colour
            if len(colour) < len("1") or len(colour) > len("10"):
                colour = colour_
            stdscr.addstr(curses.LINES-1, 0, f"Changed colour to index <#{colour}>                             ")
        elif msg[0:3] == "!dm":
            pass #send a dm

def msghandler():
    while __name__ == "__main__":
        get_msg()
        time.sleep(1)

inpt = ""

def inputhandler():
    global inpt, stdscr
    while __name__ == "__main__":
        try:
            chcode = stdscr.getch()
            keypressed = chr(chcode)
            if keypressed == "\n":
                send_msg(inpt)
                stdscr.addstr(curses.LINES-3, 0, " "*curses.COLS)
                inpt = ""
            elif keypressed == "\b" or chcode == 127:
                inpt = inpt[:len(inpt)-1]
            else:
                if chcode == 34:
                    inpt = inpt+'"'
                else:
                    inpt = inpt+keypressed
        except:
            pass

requests.post(domain+f"/{channel}", data=(f"{key}00           ({username} joined.)".encode(encoding="UTF-8")))
get_msg()

def exit_handler():
    requests.post(domain+f"/{channel}", data=(f"{key}00           ({username} disconnected.)".encode(encoding="UTF-8")))

atexit.register(exit_handler)

threading.Thread(target=msghandler, daemon=True).start()
threading.Thread(target=inputhandler, daemon=True).start()

stdscr = curses.initscr()

curses.noecho()

curses.cbreak()

curses.curs_set(False)

if curses.has_colors():
    curses.start_color()
    curses.use_default_colors()
    try:
        for i in range(0, curses.COLOR_PAIRS-1):
            curses.init_pair(i + 1, i, -1)
    except:
        for i in range(0, curses.COLORS-1):
            curses.init_pair(i + 1, i, -1)
    if ("debug" in sys.argv):
        try:
            for i in range(0, 255):
                stdscr.addstr(str(i), curses.color_pair(i))
        except curses.ERR:
            pass
        stdscr.refresh()
        time.sleep(5)

y, x = stdscr.getmaxyx()

while __name__ == "__main__":
    if curses.is_term_resized(y, x):
        y, x = stdscr.getmaxyx()
        stdscr = curses.initscr()
        stdscr.clear()
        curses.resize_term(y, x)
        stdscr.refresh()

    stdscr.addstr(0, 0, f"//{channel}          ")
    stdscr.addstr(curses.LINES-4, 0, "-"*curses.COLS)
    stdscr.addstr(curses.LINES-3, 0, "> "+inpt+" "*(curses.COLS-len("> "+inpt)-1))

    for i in range(len(messages))[:curses.LINES-5]:
        if len(messages[i]) > curses.COLS-2:
            messages[i] = messages[i][:curses.COLS-2]
        stdscr.addstr(curses.LINES-5-i, 0, messages[i][2:]+" "*(curses.COLS-len(messages[i])-1), curses.color_pair(int(messages[i][:2])))

    stdscr.refresh()
