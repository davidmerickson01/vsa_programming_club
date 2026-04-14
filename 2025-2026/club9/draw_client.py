import socket
import threading
import pygame
import random

SERVER_IP = "127.0.0.1"  # change to your server IP
PORT = 5555

WIDTH, HEIGHT = 800, 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Drawing")

clock = pygame.time.Clock()

# Random color per client
color = (
    random.randint(50, 255),
    random.randint(50, 255),
    random.randint(50, 255)
)

# Networking
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))


def receive():
    while True:
        try:
            data = client.recv(1024).decode()
            if data:
                x, y, r, g, b = map(int, data.split())
                pygame.draw.circle(screen, (r, g, b), (x, y), 5)
        except:
            break


threading.Thread(target=receive, daemon=True).start()

running = True
drawing = False

screen.fill((255, 255, 255))

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

    if drawing:
        x, y = pygame.mouse.get_pos()

        # Draw locally
        pygame.draw.circle(screen, color, (x, y), 5)

        # Send to server
        message = f"{x} {y} {color[0]} {color[1]} {color[2]}"
        try:
            client.send(message.encode())
        except:
            pass

    pygame.display.flip()

pygame.quit()
client.close()
