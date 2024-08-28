from time import sleep
from random import randint
import pygame
import sys
import tkinter as tk
from tkinter import simpledialog


def createScreen():
    print('available resolutions', pygame.display.list_modes(0))
    screen_width, screen_height = pygame.display.list_modes(0)[0]
    options = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    screen = pygame.display.set_mode((screen_width, screen_height), options)
    print("screen created, size is:", screen.get_size())
    return screen


def evolve_cell(alive, neighbours):
    return neighbours == 3 or (alive and neighbours == 2)


def count_neighbours(grid, position):
    x, y = position
    max_x = len(grid)
    max_y = len(grid[0])
    neighbour_cells = [(x - 1, y - 1), (x - 1, y + 0), (x - 1, y + 1),
                       (x + 0, y - 1), (x + 0, y + 1),
                       (x + 1, y - 1), (x + 1, y + 0), (x + 1, y + 1)]
    count = 0
    for nx, ny in neighbour_cells:
        nx = (nx + max_x) % max_x
        ny = (ny + max_y) % max_y
        count += grid[nx][ny]
    return count


def make_empty_grid(x, y):
    grid = []
    for r in range(x):
        row = []
        for c in range(y):
            row.append(0)
        grid.append(row)
    return grid


def make_random_grid(x, y):
    grid = []
    for r in range(x):
        row = []
        for c in range(y):
            row.append(randint(0, 1))
        grid.append(row)
    return grid


def evolve(grid):
    x = len(grid)
    y = len(grid[0])
    new_grid = make_empty_grid(x, y)
    for r in range(x):
        for c in range(y):
            cell = grid[r][c]
            neighbours = count_neighbours(grid, (r, c))
            new_grid[r][c] = 1 if evolve_cell(cell, neighbours) else 0
    return new_grid


BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)

def draw_block(x, y, alive_color):
    block_size = 9
    x *= block_size
    y *= block_size
    rect = pygame.Rect(x, y, block_size, block_size)
    pygame.draw.rect(screen, alive_color, rect)


def handleInputEvents(xlen, ylen):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                global world
                world = make_random_grid(xlen, ylen)
        if event.type == pygame.KEYDOWN:
            sys.exit(0)  # quit on any key
        if event.type == pygame.QUIT:  # pygame issues a quit event, for e.g. by closing the window
            print("quitting")
            sys.exit(0)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    global screen
    screen = createScreen()
    (xmax, ymax) = screen.get_size()
    cell_number = 0

    # Fix the float to int conversion issue
    xlen = int(xmax / 9)
    ylen = int(ymax / 9)

    global world
    world = make_random_grid(xlen, ylen)

    global iteration_count
    iteration_count = 0

    font = pygame.font.SysFont(None, 36)

    while True:
        handleInputEvents(xlen, ylen)
        clock.tick(40)
        for x in range(xlen):
            for y in range(ylen):
                alive = world[x][y]
                cell_number += 1
                cell_color = LIGHT_BLUE if alive else BLACK
                draw_block(x, y, cell_color)

        iteration_count += 1

        # Draw background rectangle for iteration count
        pygame.draw.rect(screen, (0, 0, 0), (10, 10, 200, 40))
        iteration_text = font.render(f"Iteration: {iteration_count}", True, (255, 255, 255))
        screen.blit(iteration_text, (15, 15))

        pygame.display.flip()
        world = evolve(world)
        cell_number = 0


if __name__ == '__main__':
    main()