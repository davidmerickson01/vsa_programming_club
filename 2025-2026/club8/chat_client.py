import socket

HOST = "127.0.0.1"   # server address
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to server")

while True:
    msg = input("You: ")
    client.sendall(msg.encode())

    data = client.recv(1024)
    print("Server:", data.decode())

client.close()
