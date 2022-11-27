import pygame
import random
import numpy as np
import sys
import copy

FPS = 20

STRIDE = 20
ROWS = 50
COLS = 50
WIDTH = COLS * STRIDE
HEIGHT = ROWS * STRIDE

COLOR = (150,150,150)
RADIUS = 5

ALL_OPTIONS = [(-1,0),(1,0),(0,-1),(0,1)]

def init_grid():
    return np.ones((ROWS,COLS), dtype=np.bool)

def update_grid(grid):
    return grid

def t(grid):
    x = grid[0] * STRIDE
    y = grid[1] * STRIDE
    return (x,y)

def is_valid(curr, grid, option):
    x = int(curr[0] + option[0])
    y = int(curr[1] + option[1])
    within_bounds = x > 0 and x < COLS and y > 0 and y < ROWS
    return within_bounds and not grid[x,y]

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self-Avoiding Walk")

animate = True
exit = False

curr = (ROWS / 2, COLS / 2)
pygame.draw.circle(screen, COLOR, t(curr), RADIUS)
grid = np.zeros((ROWS,COLS))

while not exit:

    clock.tick(FPS)

    if animate:
        options = []
        for option in ALL_OPTIONS:
            if is_valid(curr, grid, option):
                options.append(option)
        if options == []:
            print("Got stuck!")
            animate = False
        else:
            option = random.choice(options)
            prev = copy.deepcopy(curr)
            curr = (int(curr[0] + option[0]), int(curr[1] + option[1]))
            pygame.draw.circle(screen, COLOR, t(curr), RADIUS)
            pygame.draw.line(screen, COLOR, t(prev), t(curr))
            grid[curr] = True

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
