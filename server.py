import socket
import threading
import pickle
from enum import Enum, auto
from copy import deepcopy
import random

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 17  # Port to listen on (non-privileged ports are > 1023)

lobby = {}
lobby_ = {} #usernames only

games = {}

gameid_ = 0

minstockval = 1#0.007

def clamp(val, min, max):
	if (val > max):
		return max
	if (val < min):
		return min
	return val

def fixData(data, length=4096):
	addonlen = length-len(data)
	addonlen_ = str(addonlen)
	while len(addonlen_) < 4:
		addonlen_ = "0"+addonlen_
	addon = addonlen_.encode()+(b" "*(addonlen-4))
	return addon+data

def recvData(data):
	try:
		return data[int(data[0:4]):]
	except:
		return b''

class Pieces(Enum):
	KING = 1
	QUEEN = 2
	KNIGHT = 3
	BISHOP = 4
	ROOK = 5
	PAWN = 6

stock_multiplier = 0.1

stock_variations = {
	Pieces.KING:[-0.1,0.1],
	Pieces.QUEEN:[-0.4,0.4],
	Pieces.BISHOP:[-0.05,0.05],
	Pieces.KNIGHT:[-0.05,0.05],
	Pieces.ROOK:[-0.1,0.1],
	Pieces.PAWN:[-0.01,0.01]
}

class dTypes(Enum):
	JOINLOBBY = auto()
	ACCEPTREQUEST = auto()
	SENDREQUEST = auto()
	REQUESTLOBBY = auto()
	GAMEDATA = auto()
	STARTGAME = auto()
	LOBBYDATA = auto()
	GAMEID = auto()
	STOCKUPDATE = auto()

def randfloat(min, max):
	return random.randint(min*100000, max*100000)/100000

def connection(conn, addr):
	global lobby, games, gameid_, lobby_
	print(f"Connected by {addr}")
	print(conn)
	opponent = None
	gameid = deepcopy(gameid_)
	gameid_ += 1
	lobby.update({gameid:["anonymous",conn]})
	conn.send(fixData(pickle.dumps({"type":dTypes.GAMEID, "gameid":gameid})))
	try:
		while __name__ == "__main__":
			data = recvData(conn.recv(4096))
			if data == b'':
				continue
			data = pickle.loads(data)
			datatype = data["type"]
			if (datatype == dTypes.JOINLOBBY):
				lobby.update({gameid:["anonymous",conn]})
				lobby_.update({gameid:data["username"]})
				print("Added player "+data["username"]+" to lobby")
				conn.send(fixData(pickle.dumps({"type":dTypes.LOBBYDATA, "lobby":lobby_})))
			elif (datatype == dTypes.REQUESTLOBBY):
				conn.send(fixData(pickle.dumps({"type":dTypes.LOBBYDATA, "lobby":lobby_})))
				print("sent lobby data")
			elif (datatype == dTypes.SENDREQUEST):
				print(lobby[data["gameid"]])
				opponent = lobby[data["gameid"]][1]
				opponent.send(fixData(pickle.dumps(data)))
			elif (datatype == dTypes.ACCEPTREQUEST):
				p1colour = data["p1colour"]
				p2colour = data["p2colour"]
				opponent = lobby[data["gameid2"]][1]
				conn.send(fixData(pickle.dumps({"type":dTypes.STARTGAME, "colour":p1colour})))
				opponent.send(fixData(pickle.dumps({"type":dTypes.STARTGAME, "colour":p2colour})))
				lobby.pop(gameid)
				lobby.pop(data["gameid2"])
				games.update({gameid:[conn,opponent]})
			elif (datatype == dTypes.GAMEDATA):
				opponent.send(fixData(pickle.dumps(data)))
			elif (datatype == dTypes.STOCKUPDATE):
				board = data["board"]
				stocks = data["stocks"]
				num_pieces = {
					Pieces.KING:0,
					Pieces.QUEEN:0,
					Pieces.KNIGHT:0,
					Pieces.BISHOP:0,
					Pieces.ROOK:0,
					Pieces.PAWN:0,
					None:0
				}
				for x in range(8):
					for y in range(8):
						num_pieces[board[x][y][0]] += 1
				for i in num_pieces:
					if i == None:
						continue
					value = stocks[i][0]
					momentum = stocks[i][2]
					momentum += randfloat(stock_variations[i][0],stock_variations[i][1])
					value = clamp(value+momentum*stock_multiplier,minstockval,100)
					stocks[i][0] = value
					stocks[i][2] = momentum
				conn.send(fixData(pickle.dumps({"type":dTypes.STOCKUPDATE, "stocks":stocks})))
				opponent.send(fixData(pickle.dumps({"type":dTypes.STOCKUPDATE, "stocks":stocks})))
	except Exception as e:
		print(e)
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
