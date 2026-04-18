import socket
import threading
import pygame
import random
import sys

# --- CONFIG ---
SERVER_IP = "127.0.0.1"
PORT = 5000
TILE_SIZE = 20
HEADER_HEIGHT = 50
GREEN_PLAYER = (0, 200, 0) # Local player default (or use random)

# --- NETWORKING ---
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

# 1. Receive Maze Data immediately
n = int.from_bytes(client.recv(4), 'big')
maze_raw = client.recv(n).decode().split('\n')

# Process Maze
ROWS = len(maze_raw)
COLS = max(len(row) for row in maze_raw)
maze = [row.ljust(COLS) for row in maze_raw]

# --- INIT PYGAME ---
pygame.init()
screen = pygame.display.set_mode((COLS * TILE_SIZE, ROWS * TILE_SIZE + HEADER_HEIGHT))
pygame.display.set_caption("Multiplayer Maze")
font = pygame.font.SysFont(None, 28)

gem_img = pygame.image.load('gem.png')
stone_img = pygame.image.load('stone.png')

# Setup local state
other_players = {} # Key: address/id, Value: (r, c, (color))
my_color = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
empty_spaces = [(r, c) for r in range(ROWS) for c in range(COLS) if maze[r][c].lower() == ' ']
gems = {(r, c) for r in range(ROWS) for c in range(COLS) if maze[r][c].lower() == 'o'}
player_pos = list(random.choice(empty_spaces))
score = 0

def send_move():
    # Format: "row col r g b"
    msg = f"{player_pos[0]} {player_pos[1]} {my_color[0]} {my_color[1]} {my_color[2]}".encode()
    client.send(len(msg).to_bytes(4, 'big'))
    client.send(msg)

def receive():
    while True:
        try:
            header = client.recv(4)
            if not header: break
            n = int.from_bytes(header, 'big')
            data = client.recv(n).decode().split()
            if data:
                # Store by unique combo of color as a proxy for ID
                r, c, cr, cg, cb = map(int, data)
                other_players[f"{cr}{cg}{cb}"] = (r, c, (cr, cg, cb))
        except:
            break

threading.Thread(target=receive, daemon=True).start()
send_move() # Initial position broadcast

# --- LOOP ---
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            dr, dc = 0, 0
            if event.key == pygame.K_UP: dr = -1
            elif event.key == pygame.K_DOWN: dr = 1
            elif event.key == pygame.K_LEFT: dc = -1
            elif event.key == pygame.K_RIGHT: dc = 1
            
            if dr != 0 or dc != 0:
                nr, nc = player_pos[0] + dr, player_pos[1] + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc].lower() != 'x':
                    player_pos = [nr, nc]
                    send_move()
                    if (nr, nc) in gems:
                        gems.remove((nr, nc))
                        score += 10

    # Draw
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (60,60,60), (0,0, COLS*TILE_SIZE, HEADER_HEIGHT))
    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10, 15))

    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * TILE_SIZE, r * TILE_SIZE + HEADER_HEIGHT
            if maze[r][c].lower() == 'x':
                screen.blit(stone_img, (x, y))
            elif (r, c) in gems:
                screen.blit(gem_img, (x, y))

    # Draw Others, and consume gems
    for pid in other_players:
        orow, ocol, ocolr = other_players[pid]
        if (orow, ocol) in gems:
            gems.remove((orow, ocol))
        pygame.draw.circle(screen, ocolr, (ocol*TILE_SIZE+10, orow*TILE_SIZE+HEADER_HEIGHT+10), 7)

    # Draw Me
    pygame.draw.circle(screen, my_color, (player_pos[1]*TILE_SIZE+10, player_pos[0]*TILE_SIZE+HEADER_HEIGHT+10), 8)
    
    pygame.display.flip()
    clock.tick(60)
