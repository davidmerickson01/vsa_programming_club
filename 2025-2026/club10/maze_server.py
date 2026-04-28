import socket
import threading

"""
gemini prompt:

create maze_server.py and maze_client.py where the server loads maze.txt, then when each client connects it transmits the maze data structure to each client as the first transaction using the same protocol (with a four byte size header, followed by payload). each client draws the maze and places its guy at a random location with a random color. every time the client moves its guy, it transmits its x,y coordinate to the server along with its color (in the same way as draw_client). the server broadcasts that message to all other clients. each client then renders all the guys at their specified locations. collisions are ok. gem consumption is done in each client. the client only gets points if it gets the gem itself.

manual edits:
1) gems consumed by another client weren't removed from the other clients
"""

HOST = '0.0.0.0'
PORT = 5000

# Load maze once at startup
def load_maze(filename):
    try:
        with open(filename, "r") as f:
            return [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        return ["XXXXX", "X   X", "XXXXX"] # Fallback

MAZE_DATA = load_maze("maze.txt")
# Convert maze list to a single string joined by newlines for transmission
MAZE_STR = "\n".join(MAZE_DATA)

clients = []

def broadcast(data, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(len(data).to_bytes(4, 'big'))
                client.send(data)
            except Exception as e:
                print(f"Type: {type(e).__name__} | Message: {e}")
                if client in clients:
                    print("removing client",client)
                    clients.remove(client)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")
    clients.append(conn)

    try:
        # First Transaction: Send the Maze Data
        payload = MAZE_STR.encode()
        conn.send(len(payload).to_bytes(4, 'big'))
        conn.send(payload)

        while True:
            # Relay movement: "row col r g b"
            header = conn.recv(4)
            if not header: break
            n = int.from_bytes(header, 'big')
            data = conn.recv(n)
            if not data: break
            broadcast(data, conn)
    except Exception as e:
        print(f"Error handling {addr}: {e}")
    finally:
        print(f"[DISCONNECTED] {addr}")
        if conn in clients:
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
