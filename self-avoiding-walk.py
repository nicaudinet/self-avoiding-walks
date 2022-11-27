import pygame
import random
import copy

FPS = 21

STRIDE = 50
ROWS = 5
COLS = 5
WIDTH = COLS * STRIDE
HEIGHT = ROWS * STRIDE

COLOR = (150,150,150)
RADIUS = 15

ALL_OPTIONS = [(-1,0),(1,0),(0,-1),(0,1)]


class Step:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.tried = False

def all_options():
    return [Step(-1,0), Step(1,0), Step(0,-1), Step(0,1)]

class Spot:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.pos = (i * STRIDE + STRIDE / 2, j * STRIDE + STRIDE / 2)
        self.visited = False
        self.options = all_options()

    def is_valid(self, i, j, grid):
        within_bounds = i >= 0 and i < COLS and j >= 0 and j < ROWS
        return within_bounds and not grid[i][j].visited

    def step(self, grid):
        steps = []
        for step in self.options:
            i = self.i + step.dx
            j = self.j + step.dy
            if not step.tried and self.is_valid(i, j, grid):
                steps.append(step)
        if steps == []:
            return None
        else:
            step = random.choice(steps)
            step.tried = True
            i = self.i + step.dx
            j = self.j + step.dy
            return grid[i][j]

    def clear(self):
        self.visited = False
        for option in self.options:
            option.tried = False

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
curr.visited = True
path = [curr]
pygame.draw.circle(screen, COLOR, curr.pos, RADIUS)

while not exit:

    clock.tick(FPS)

    if animate:
        screen.fill((0,0,0))
        prev = copy.deepcopy(curr)
        curr = curr.step(grid)
        if not curr:
            stuck = path.pop()
            stuck.clear()
            curr = path[-1]
        else:
            curr.visited = True
            path.append(curr)
        # Draw the path on the screen
        pygame.draw.circle(screen, COLOR, path[0].pos, RADIUS)
        for i in range(1, len(path)):
            pygame.draw.circle(screen, COLOR, path[i].pos, RADIUS)
            pygame.draw.line(screen, COLOR, path[i-1].pos, path[i].pos, width=5)
        # Stop if the path fills the whole screen
        if (len(path) == ROWS * COLS):
            print("Done!")
            animate = False

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
