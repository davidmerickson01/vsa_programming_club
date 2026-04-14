import socket
import threading

HOST = '0.0.0.0'
PORT = 5555

clients = []

def broadcast(data, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(data)
            except:
                clients.remove(client)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")
    clients.append(conn)

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            broadcast(data, conn)
    except:
        pass

    print(f"[DISCONNECTED] {addr}")
    clients.remove(conn)
    conn.close()

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER RUNNING] {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start()