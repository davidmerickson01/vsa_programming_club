import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mandelbrot Seahorse Valley")

clock = pygame.time.Clock()

# Seahorse valley coordinates in Mandelbrot set
xmin = -0.9
xmax = -0.4
ymin = 0.05
ymax = 0.15

max_iter = 120

def mandelbrot(c):
    z = 0
    for i in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return i
    return max_iter

running = True
y = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw one row per frame so the fractal appears gradually
    if y < HEIGHT:
        for x in range(WIDTH):

            real = xmin + (x / WIDTH) * (xmax - xmin)
            imag = ymin + (y / HEIGHT) * (ymax - ymin)

            c = complex(real, imag)
            m = mandelbrot(c)

            color = (m % 8 * 32, m % 16 * 16, m % 32 * 8)

            screen.set_at((x, y), color)

        y += 1
        pygame.display.update()

    clock.tick(100000)

pygame.quit()
