import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

def receive_messages(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print("\nClient:", data.decode())
        except:
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server listening on port", PORT)

conn, addr = server.accept()
print("Connected by", addr)

# Start thread for receiving messages
threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()

# Main thread sends messages
while True:
    msg = input("Server: ")
    conn.sendall(msg.encode())
