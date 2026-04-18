import pygame
import random
import sys

"""
chatgpt prompt:
create a python game using pygame which loads maze.txt into an array of strings, then draws that into a grid on the screen with fixed size graphic elements corresponding to the strings. the X should look like a rock. the O should look like a gem. then randomly pick a place which is a space and place a person there. then allow the the arrow keys to move the person around the maze. one press moves one space. diagonal moves are not allowed. the person cannot be where a rock is. and if the person lands on a gem, it should erase it and win 10 points. the point total should be printed above the maze. when all the gems are gone, the game is done.

Then I did a variety of manual touchups:

1) defined HEADER_HEIGHT
2) switched from rectangle and circle for rock and gem to images, which I generated on gemini.google.com using:

create a 20x20 pixel image of a green cut gem where the background is alpha 0
draw a 20x20 pixel image of a square piece of brown and gray stone

then touched up and downscaled in Paint.

"""

# --- CONFIG ---
TILE_SIZE = 20
FONT_SIZE = 28
HEADER_HEIGHT = 50

# Colors
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
DARK_GRAY = (60, 60, 60)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)

gem_img = pygame.image.load('gem.png')
stone_img = pygame.image.load('stone.png')

# --- LOAD MAZE ---
def load_maze(filename):
    with open(filename, "r") as f:
        maze = [line.rstrip("\n") for line in f]
    return maze

maze = load_maze("maze.txt")
ROWS = len(maze)
COLS = max(len(row) for row in maze)

# Pad rows so all are equal length
maze = [row.ljust(COLS) for row in maze]

# --- INIT GAME ---
pygame.init()
screen = pygame.display.set_mode((COLS * TILE_SIZE, ROWS * TILE_SIZE + HEADER_HEIGHT))
pygame.display.set_caption("Maze Game")

font = pygame.font.SysFont(None, FONT_SIZE)

# --- FIND EMPTY SPOTS ---
empty_spaces = []
gems = set()

for r in range(ROWS):
    for c in range(COLS):
        ch = maze[r][c].lower()
        if ch == ' ':
            empty_spaces.append((r, c))
        elif ch == 'o':
            gems.add((r, c))

# --- PLACE PLAYER ---
player_pos = list(random.choice(empty_spaces))

score = 0
game_over = False

# --- DRAW FUNCTIONS ---
def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, DARK_GRAY, (0,0,COLS * TILE_SIZE,HEADER_HEIGHT))

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw maze
    for r in range(ROWS):
        for c in range(COLS):
            x = c * TILE_SIZE
            y = r * TILE_SIZE + HEADER_HEIGHT

            ch = maze[r][c].lower()

            if ch == 'x':
                screen.blit(stone_img, (x, y, TILE_SIZE, TILE_SIZE))
            elif (r, c) in gems:
                screen.blit(gem_img, (x, y, TILE_SIZE, TILE_SIZE))

    # Draw player
    pr, pc = player_pos
    px = pc * TILE_SIZE
    py = pr * TILE_SIZE + HEADER_HEIGHT
    pygame.draw.circle(screen, GREEN, (px + TILE_SIZE//2, py + TILE_SIZE//2), TILE_SIZE//3)

    if game_over:
        text = font.render("ALL GEMS COLLECTED!", True, WHITE)
        screen.blit(text, (screen.get_width()//2 - 150, 10))

    pygame.display.flip()

# --- GAME LOOP ---
clock = pygame.time.Clock()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and not game_over:
            dr, dc = 0, 0

            if event.key == pygame.K_UP:
                dr = -1
            elif event.key == pygame.K_DOWN:
                dr = 1
            elif event.key == pygame.K_LEFT:
                dc = -1
            elif event.key == pygame.K_RIGHT:
                dc = 1

            new_r = player_pos[0] + dr
            new_c = player_pos[1] + dc

            # Bounds check
            if 0 <= new_r < ROWS and 0 <= new_c < COLS:
                if maze[new_r][new_c].lower() != 'x':  # not a rock
                    player_pos = [new_r, new_c]

                    # Collect gem
                    if (new_r, new_c) in gems:
                        gems.remove((new_r, new_c))
                        score += 10

                        if len(gems) == 0:
                            game_over = True

    draw()
