import socket
import threading
import pickle
from enum import Enum, auto
from copy import deepcopy

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

lobby = {}
lobby_ = {} #usernames only

games = {}

gameid_ = 0

class Pieces(Enum):
	KING = 1
	QUEEN = 2
	KNIGHT = 3
	BISHOP = 4
	ROOK = 5
	PAWN = 6

class dTypes(Enum):
    JOINLOBBY = auto()
    ACCEPTREQUEST = auto()
    SENDREQUEST = auto()
    REQUESTLOBBY = auto()
    GAMEDATA = auto()
    STARTGAME = auto()
    LOBBYDATA = auto()
    GAMEID = auto()

def connection(conn, addr):
    global lobby, games, gameid_, lobby_
    print(f"Connected by {addr}")
    print(conn)
    opponent = None
    gameid = deepcopy(gameid_)
    gameid_ += 1
    lobby.update({gameid:["anonymous",conn]})
    conn.send(pickle.dumps({"type":dTypes.GAMEID, "gameid":gameid}))
    try:
        while __name__ == "__main__":
            data = conn.recv(4096)
            data = pickle.loads(data)
            datatype = data["type"]
            if (datatype == dTypes.JOINLOBBY):
                lobby.update({gameid:["anonymous",conn]})
                lobby_.update({gameid:data["username"]})
            elif (datatype == dTypes.REQUESTLOBBY):
                conn.send(pickle.dumps({"type":dTypes.LOBBYDATA, "lobby":lobby_}))
            elif (datatype == dTypes.SENDREQUEST):
                print(lobby[data["gameid"]])
                opponent = lobby[data["gameid"]][1]
                opponent.send(pickle.dumps(data))
            elif (datatype == dTypes.ACCEPTREQUEST):
                p1colour = data["p1colour"]
                p2colour = data["p2colour"]
                opponent = lobby[data["gameid2"]][1]
                conn.send(pickle.dumps({"type":dTypes.STARTGAME, "colour":p1colour}))
                opponent.send(pickle.dumps({"type":dTypes.STARTGAME, "colour":p2colour}))
                lobby.pop(gameid)
                lobby.pop(data["gameid2"])
                games.update({gameid:[conn,opponent]})
            elif (datatype == dTypes.GAMEDATA):
                print(data)
                opponent.send(pickle.dumps(data))
    except:
        print(f"Client {addr} disconnected")
        if gameid in lobby_:
            lobby_.pop(gameid)
        if gameid in lobby:
            lobby.pop(gameid)
        if gameid in games:
            games.pop(gameid)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while __name__ == "__main__":
        s.listen()
        conn, addr = s.accept()
        threading.Thread(target=connection, args=(conn,addr)).start()
