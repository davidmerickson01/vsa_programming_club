import pygame
import sys

# chatgpt
# create a program using pygame and python which has a box that
# moves around the screen and bounces on the sides

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Box")

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)

# Box settings
box_size = 50
box_x = 100
box_y = 100
speed_x = 4
speed_y = 3

clock = pygame.time.Clock()

# Main loop
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move box
    box_x += speed_x
    box_y += speed_y

    # Bounce on walls
    if box_x <= 0 or box_x + box_size >= WIDTH:
        speed_x *= -1
    if box_y <= 0 or box_y + box_size >= HEIGHT:
        speed_y *= -1

    # Draw
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (box_x, box_y, box_size, box_size))
    pygame.display.flip()

pygame.quit()
sys.exit()
