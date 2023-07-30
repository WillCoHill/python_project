import socket
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

rng = "Los Angeles: Sunny. Temperature: 95 degrees"

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!!")
    clientsocket.send(str.encode(rng, "utf-8"))