import pygame
import sys
import time

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((720,480))
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

# object oriented program
class Creature:
    def __init__(self, name, st, hp, filename):
        self.name = name
        self.strength = st
        self.hit_points = hp
        self.rect = pygame.Rect(0,0,100,100)
        self.image = pygame.image.load(filename)
    def print(self):
        print(self.name, self.strength, self.hit_points)
    def attack(self, damage):
        self.hit_points -= damage
    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
    def draw(self):
        screen.blit(self.image, self.rect)

elf = Creature("Elf", 20, 10, "elf.png")
goblin = Creature("Goblin", 18, 12, "goblin.jpg")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    

    screen.fill(BLACK)
    elf.move(1,1)
    goblin.move(2,2)
    elf.draw()
    goblin.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

