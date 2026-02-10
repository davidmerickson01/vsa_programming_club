import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("From Brain Fog to Idea!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
PINK = (255, 180, 200)
YELLOW = (255, 240, 100)

# Fonts
font_big = pygame.font.SysFont(None, 72)
font_small = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

# Timing
start_time = time.time()
BRAIN_TIME = 4  # seconds before idea appears


def draw_brain():
    screen.fill(WHITE)

    # Brain base
    pygame.draw.ellipse(screen, PINK, (250, 200, 300, 200))

    # Brain squiggles
    for i in range(6):
        pygame.draw.arc(
            screen,
            GRAY,
            (260 + i * 40, 220, 80, 140),
            0,
            3.14,
            3,
        )

    # ZZZ text
    zzz = font_big.render("Z Z Z", True, GRAY)
    screen.blit(zzz, (330, 140))

    # Status text
    text = font_small.render("Jude's brain not working...", True, BLACK)
    screen.blit(text, (300, 430))


def draw_idea():
    screen.fill(WHITE)

    # Light bulb
    pygame.draw.circle(screen, YELLOW, (400, 260), 80)
    pygame.draw.rect(screen, GRAY, (360, 330, 80, 40))
    pygame.draw.rect(screen, BLACK, (360, 330, 80, 40), 2)

    # Glow effect
    for r in range(90, 130, 10):
        pygame.draw.circle(screen, YELLOW, (400, 260), r, 2)

    # IDEA text
    idea_text = font_big.render("IDEA!", True, BLACK)
    screen.blit(idea_text, (330, 430))


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    elapsed = time.time() - start_time

    if elapsed < BRAIN_TIME:
        draw_brain()
    else:
        draw_idea()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
