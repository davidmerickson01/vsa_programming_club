import pygame
import random
import math
import sys

# chatgpt prompt
# create an asteriods game using python and pygame. the asteroids should
# move at random and be of different size. it should keep score as you
# shoot them with bullets.

pygame.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

# ---------------- UTIL ----------------
def wrap_position(pos):
    return pos[0] % WIDTH, pos[1] % HEIGHT

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# ---------------- PLAYER ----------------
class Player:
    def __init__(self):
        self.pos = [WIDTH // 2, HEIGHT // 2]
        self.vel = [0, 0]
        self.angle = 0

    def rotate(self, direction):
        self.angle += direction * 4

    def thrust(self):
        rad = math.radians(self.angle)
        self.vel[0] += math.cos(rad) * 0.15
        self.vel[1] += math.sin(rad) * 0.15

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos = list(wrap_position(self.pos))

    def draw(self):
        rad = math.radians(self.angle)
        tip = (
            self.pos[0] + math.cos(rad) * 15,
            self.pos[1] + math.sin(rad) * 15,
        )
        left = (
            self.pos[0] + math.cos(rad + 2.5) * 15,
            self.pos[1] + math.sin(rad + 2.5) * 15,
        )
        right = (
            self.pos[0] + math.cos(rad - 2.5) * 15,
            self.pos[1] + math.sin(rad - 2.5) * 15,
        )
        pygame.draw.polygon(screen, WHITE, [tip, left, right], 2)

# ---------------- BULLET ----------------
class Bullet:
    def __init__(self, pos, angle):
        self.pos = list(pos)
        self.vel = [
            math.cos(math.radians(angle)) * 6,
            math.sin(math.radians(angle)) * 6,
        ]
        self.life = 60

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos = list(wrap_position(self.pos))
        self.life -= 1

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.pos, 2)

# ---------------- ASTEROID ----------------
class Asteroid:
    def __init__(self):
        self.size = random.randint(20, 60)
        self.pos = [
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
        ]
        angle = random.uniform(0, 360)
        speed = random.uniform(0.5, 2.5)
        self.vel = [
            math.cos(math.radians(angle)) * speed,
            math.sin(math.radians(angle)) * speed,
        ]

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos = list(wrap_position(self.pos))

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.pos, self.size, 2)

# ---------------- MAIN ----------------
def main():
    player = Player()
    bullets = []
    asteroids = [Asteroid() for _ in range(6)]
    score = 0

    while True:
        clock.tick(60)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.pos, player.angle))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rotate(-1)
        if keys[pygame.K_RIGHT]:
            player.rotate(1)
        if keys[pygame.K_UP]:
            player.thrust()

        player.move()
        player.draw()

        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()
            if bullet.life <= 0:
                bullets.remove(bullet)

        for asteroid in asteroids[:]:
            asteroid.move()
            asteroid.draw()

            for bullet in bullets[:]:
                if distance(asteroid.pos, bullet.pos) < asteroid.size:
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    score += int(100 / asteroid.size)
                    asteroids.append(Asteroid())
                    break

        score_text = FONT.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
