import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (50,120,255)
GREEN = (40,200,100)
GOLD = (255,210,0)

# Player
player = pygame.Rect(100, 400, 40, 50)
vel_y = 0
speed = 5
jump_strength = -12
gravity = 0.6
on_ground = False

# Platforms
platforms = [
    pygame.Rect(0,550,800,50),
    pygame.Rect(150,450,200,20),
    pygame.Rect(450,380,200,20),
    pygame.Rect(300,300,200,20)
]

# Coins
coins = []
for _ in range(5):
    coins.append(pygame.Rect(random.randint(50,750), random.randint(100,500), 15,15))

score = 0

running = True
while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed

    if keys[pygame.K_SPACE] and on_ground:
        vel_y = jump_strength
        on_ground = False

    # Apply gravity
    vel_y += gravity
    player.y += vel_y

    # Platform collision
    on_ground = False
    for p in platforms:
        if player.colliderect(p) and vel_y >= 0:
            player.bottom = p.top
            vel_y = 0
            on_ground = True

    # Coin collection
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 10

    # Draw
    screen.fill((30,30,40))

    pygame.draw.rect(screen, BLUE, player)

    for p in platforms:
        pygame.draw.rect(screen, GREEN, p)

    for coin in coins:
        pygame.draw.circle(screen, GOLD, coin.center, 7)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10,10))

    pygame.display.flip()

pygame.quit()
