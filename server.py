import socket
from _thread import *
import pickle
from gameComms import Game

server = "0.0.0.0" # put own ip address here 
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)

print("Waiting for a connection, Server Started")

connected = set() # store ip addresses of connected clients
games = {} # stores games with an id
idCount = 0 # so 2 games dont have same id

def is_int(n):
    try:
        n = int(n)
        return True
    except ValueError:
        return False

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    get_ships = True
    get_az = False

    reply = ""
    while True:
        try:
            data = conn.recv(2048*2).decode() # if you get run out of input increase the 4096

            if gameId in games: # if game id still exist, in case the opponent disconnects
                game = games[gameId]

                if not data:
                    break
                else:
                    if is_int(data):
                        game.player_ready(p)
                    elif data == "ship":
                        get_ships = False
                        get_az = True
                    elif data == "az":
                        get_az = False
                    elif data == "end":
                        game.winnerP = p
                    elif data == "restart":
                        game.player_reset(p)
                    elif data == "new":
                        get_ships = True
                        get_az = False
                        game.reset(p)
                    elif data != "get":
                        print((p, type(p), data))
                        if get_ships:
                            game.append_ships(p, data)
                        elif get_az:
                            game.append_az(p, data)
                        else:
                            game.append_shots(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    # if we break out of connection, if one leaves or data doesn't send then delete game
    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1 # how many people are connected
    p = 0
    gameId = (idCount - 1)//2 # every 2 people enter, game id increases
    if idCount % 2 == 1: # create game
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else: # assign to a game
        games[gameId].connect = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))



