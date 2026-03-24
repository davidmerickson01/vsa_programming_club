import socket

HOST = "127.0.0.1"   # localhost
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server listening on port", PORT)

conn, addr = server.accept()
print("Connected by", addr)

while True:
    data = conn.recv(1024)
    if not data:
        break

    message = data.decode()
    print("Client:", message)

    reply = input("Server reply: ")
    conn.sendall(reply.encode())

conn.close()
server.close()
