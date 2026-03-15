import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Radial Fractal")

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (220, 220, 255)

def draw_fractal(x, y, angle, length, depth):
    if depth <= 0 or length < 2:
        return

    # calculate new point
    x2 = x + math.cos(math.radians(angle)) * length
    y2 = y + math.sin(math.radians(angle)) * length

    pygame.draw.line(screen, WHITE, (x, y), (x2, y2), 1)

    # branch in several directions
    for new_angle in [angle - 30, angle, angle + 30]:
        draw_fractal(x2, y2, new_angle, length * 0.75, depth - 1)


running = True
depth = 1
max_depth = 8

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # start from the center and spread in many directions
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    for angle in range(0, 360, 30):
        draw_fractal(center_x, center_y, angle, 80, depth)

    if depth < max_depth:
        depth += 1
        pygame.time.delay(300)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
