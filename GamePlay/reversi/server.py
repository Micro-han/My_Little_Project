import socket
from _thread import *
import pickle
from reversi import game_manager

server = "100.80.199.200" # your ipv4
port = 5550

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    print(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    # choose different game state to continue game
                    game.play()
                    # if data == "reset":
                    #     game.resetWent()
                    # elif data != "get":
                    #     game.play()

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

gameId = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    # set different game state
    idCount += 1
    p = 0
    if games.get(gameId) is None:
        games[gameId] = game_manager()
        print("Creating a new game...")
    elif games[gameId].board.is_game_ended():
        gameId += 1
        games[gameId] = game_manager()
        print("Creating a new game...")
    elif games[gameId].current_playing == 0:
        games[gameId].current_playing = 1
        p = 1
    else:
        games[gameId].current_playing = 0
        p = 2


    start_new_thread(threaded_client, (conn, p, gameId))