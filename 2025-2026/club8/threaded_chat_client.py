import socket
import threading

HOST = "127.0.0.1"   # server address
PORT = 5000

def receive_messages(client):
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            print("\nServer:", data.decode())
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to server")

# Thread to receive messages
threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

# Main thread sends messages
while True:
    msg = input("You: ")
    client.sendall(msg.encode())
