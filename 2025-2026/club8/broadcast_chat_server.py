import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = []
names = {}

def broadcast(message):
    for client in clients:
        try:
            client.sendall(message.encode())
        except:
            pass


def handle_client(conn, addr):
    try:
        # First message from client is their name
        name = conn.recv(1024).decode().strip()
        names[conn] = name
        clients.append(conn)

        join_msg = f"{name} has joined the chat"
        print(join_msg)
        broadcast(join_msg)

        while True:
            data = conn.recv(1024)
            if not data:
                break

            text = data.decode().strip()
            message = f"{name}: {text}"

            print(message)
            broadcast(message)

    except:
        pass

    finally:
        if conn in clients:
            clients.remove(conn)

        name = names.get(conn, "Unknown")
        leave_msg = f"{name} has left the chat"
        print(leave_msg)
        broadcast(leave_msg)

        conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Chat server running on port {PORT}")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    