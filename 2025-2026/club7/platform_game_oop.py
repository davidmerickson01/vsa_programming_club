import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

WHITE = (255,255,255)
BLUE = (50,120,255)
GREEN = (40,200,100)
GOLD = (255,210,0)
BG = (30,30,40)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 50)
        self.vel_y = 0
        self.speed = 5
        self.jump_strength = -12
        self.gravity = 0.6
        self.on_ground = False

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

    def check_platforms(self, platforms):
        self.on_ground = False

        for p in platforms:
            if self.rect.colliderect(p.rect) and self.vel_y >= 0:
                self.rect.bottom = p.rect.top
                self.vel_y = 0
                self.on_ground = True

    def update(self, platforms):
        self.handle_input()
        self.apply_gravity()
        self.check_platforms(platforms)

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)


class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)


class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)

    def draw(self, screen):
        pygame.draw.circle(screen, GOLD, self.rect.center, 7)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("OOP Platformer")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.player = Player(100, 400)

        self.platforms = [
            Platform(0,550,800,50),
            Platform(150,450,200,20),
            Platform(450,380,200,20),
            Platform(300,300,200,20)
        ]

        self.coins = []
        for _ in range(5):
            x = random.randint(50,750)
            y = random.randint(100,500)
            self.coins.append(Coin(x,y))

        self.score = 0
        self.running = True

    def check_coins(self):
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.score += 10

    def draw(self):
        self.screen.fill(BG)

        self.player.draw(self.screen)

        for p in self.platforms:
            p.draw(self.screen)

        for coin in self.coins:
            coin.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10,10))

        pygame.display.flip()

    def run(self):

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.player.update(self.platforms)

            self.check_coins()

            self.draw()

            self.clock.tick(60)

        pygame.quit()


game = Game()
game.run()
