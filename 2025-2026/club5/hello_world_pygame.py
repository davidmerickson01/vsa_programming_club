import pygame
import sys

# from chatgpt prompt:
# create a python program that uses pygame to say Hello World
# and draw a few shapes on the screen with different colors

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello World - Pygame")

# Colors (RGB)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
BLACK = (0, 0, 0)

# Font setup
font = pygame.font.SysFont(None, 48)
text_surface = font.render("Hello Cade!", True, BLUE)

# Clock
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    screen.fill(WHITE)

    # Draw text
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 30))

    # Draw shapes
    pygame.draw.rect(screen, BLACK, (0, 0, 100, 100))        # Rectangle
    pygame.draw.circle(screen, BLUE, (350, 200), 50)         # Circle
    pygame.draw.line(screen, GREEN, (100, 350), (500, 350), 5)  # Line

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Clean exit
pygame.quit()
sys.exit()
