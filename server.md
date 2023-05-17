import socket
import threading
import pickle
from colorama import Fore, Back
import colorama

colorama.init()

HOST, PORT = socket.gethostbyname(socket.gethostname()), 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print(f"{Fore.LIGHTBLACK_EX}Socket bound to {HOST}:{PORT}{Fore.RESET}")

conn_list = []

def connection(conn, addr):
    global conn_list
    print(f"{Fore.LIGHTBLACK_EX}Connected by {addr}{Fore.RESET}")
    conn_list.append(conn)
    while __name__ == "__main__":
        try:
            data = conn.recv(1024)#.decode(encoding="UTF-8")
            print(data.decode(encoding="UTF-8"))
            for i in conn_list:
                i.send(data)
        except:
            print(f"{Fore.LIGHTBLACK_EX}Client {addr} disconnected.{Fore.RESET}")
            conn_list.remove(conn)
            break


while __name__ == "__main__":
    s.listen()
    print(f"{Fore.LIGHTBLACK_EX}Listening...{Fore.RESET}")
    conn, addr = s.accept()
    threading.Thread(target=connection, args=(conn,addr)).start()
