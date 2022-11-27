import pygame
import random
import copy

FPS = 20

STRIDE = 50
ROWS = 10
COLS = 10
WIDTH = COLS * STRIDE
HEIGHT = ROWS * STRIDE

COLOR = (150,150,150)
RADIUS = 15

ALL_OPTIONS = [(-1,0),(1,0),(0,-1),(0,1)]

class Spot:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.pos = (i * STRIDE + STRIDE / 2, j * STRIDE + STRIDE / 2)
        self.visited = False

    def is_valid(self, i, j, grid):
        within_bounds = i >= 0 and i < COLS and j >= 0 and j < ROWS
        return within_bounds and not grid[i][j].visited

    def step(self, grid):
        options = []
        for option in ALL_OPTIONS:
            i = self.i + option[0]
            j = self.j + option[1]
            if self.is_valid(i, j, grid):
                options.append(option)
        if options == []:
            return None
        else:
            option = random.choice(options)
            i = self.i + option[0]
            j = self.j + option[1]
            return grid[i][j]

def init_grid():
    grid = []
    for i in range(COLS):
        row = []
        for j in range(ROWS):
            row.append(Spot(i,j))
        grid.append(row)
    return grid

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self-Avoiding Walk")

animate = True
exit = False

grid = init_grid()
curr = grid[0][0]
pygame.draw.circle(screen, COLOR, curr.pos, RADIUS)

while not exit:

    clock.tick(FPS)

    if animate:
        prev = copy.deepcopy(curr)
        curr = curr.step(grid)
        if not curr:
            print("Got stuck!")
            animate = False
        else:
            pygame.draw.circle(screen, COLOR, curr.pos, RADIUS)
            pygame.draw.line(screen, COLOR, prev.pos, curr.pos, width=5)
            curr.visited = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'q':
                exit = True
            if event.unicode == ' ':
                animate = not animate
            if event.key == 1073741906: # Up arrow
                FPS = min(61, FPS + 5)
            if event.key == 1073741905: # Down arrow
                FPS = max(1, FPS - 5)

    pygame.display.update()
