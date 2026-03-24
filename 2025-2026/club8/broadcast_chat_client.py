import socket
import threading

HOST = "vsaprogrammingclub.duckdns.org"
PORT = 5000

name = input("Enter your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Send name immediately after connecting
client.sendall(name.encode())


def receive_messages():
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            print("\n" + message.decode())
        except:
            break


threading.Thread(target=receive_messages, daemon=True).start()

while True:
    msg = input()
    client.sendall(msg.encode())
