import requests
import time
import pickle
import curses
import threading
import random
import atexit
import sys

servers = requests.get("https://hebedebe.github.io/chess2.0/hermes_data.json").json()["servers"]

print(f"Server list recieved")

patchnotes = requests.get("https://hebedebe.github.io/chess2.0/hermes_data.json").json()["patchnotes"]

print(f"Downloaded patch notes")

#servers = ["http://10.185.154.17:80","http://188.191.106.61:80"]

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
    print("\nThe main server is probably offline. Try again later\n")
    while True:
        pass

print(f"\nPatch Notes\n{patchnotes}\n")

username = input("Username\n> ")

messages = []

def get_msg():
    global domain, messages
    response = requests.get(domain+"/getmsg")
    data = response.json()
    messages = data["messages"]

def send_msg(msg):
    response = requests.post(domain+"/postmsg", data=(f"{colour}[{username}] {msg}".encode(encoding="UTF-8")))

def msghandler():
    while __name__ == "__main__":
        get_msg()
        time.sleep(1)

inpt = ""

def inputhandler():
    global inpt, stdscr
    while __name__ == "__main__":
        try:
            keypressed = chr(stdscr.getch())
            if keypressed == "\n":
                send_msg(inpt)
                stdscr.addstr(curses.LINES-3, 0, " "*curses.COLS)
                inpt = ""
            elif keypressed == "\b":
                inpt = inpt[:len(inpt)-1]
            else:
                inpt = inpt+keypressed
        except:
            pass

requests.post(domain+"/postmsg", data=(f"00           ({username} joined.)".encode(encoding="UTF-8")))
get_msg()

def exit_handler():
    requests.post(domain+"/postmsg", data=(f"00           ({username} left.)".encode(encoding="UTF-8")))

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
    for i in range(0, curses.COLOR_PAIRS-1):
        curses.init_pair(i + 1, i, -1)
    if ("debug" in sys.argv):
        try:
            for i in range(0, 255):
                stdscr.addstr(str(i), curses.color_pair(i))
        except curses.ERR:
            # End of screen reached
            pass
        stdscr.refresh()
        time.sleep(5)

while __name__ == "__main__":
    stdscr.addstr(curses.LINES-4, 0, "-"*curses.COLS)
    stdscr.addstr(curses.LINES-3, 0, "> "+inpt+" "*(curses.COLS-len("> "+inpt)-1))

    for i in range(len(messages)):
        stdscr.addstr(curses.LINES-5-i, 0, messages[i][2:]+" "*(curses.COLS-len(messages[i])-1), curses.color_pair(int(messages[i][:2])))

    stdscr.refresh()
