from random import randint
import pygame
import sys


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

def draw_block(x, y, alive_color):
    block_size = 9
    x *= block_size
    y *= block_size
    center_point = (int(x + (block_size / 2)), int(y + (block_size / 2)))
    pygame.draw.circle(screen, alive_color, center_point, int(block_size / 2), 0)

def is_point_in_rect(point, rect):
    px, py = point
    rx, ry, rw, rh = rect
    return rx <= px <= rx + rw and ry <= py <= ry + rh

pause_menu_active = False

def set_opacity(screen, opacity):
    temp_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    temp_surface.fill((0, 0, 0, opacity))
    screen.blit(temp_surface, (0, 0))

def pause_menu(screen, xlen, ylen):
    global world, iteration_count, pause_menu_active
    pause_menu_active = True
    font = pygame.font.SysFont(None, 36)
    menu_options = ["Continue", "Reset", "Close"]
    selected_option = 0
    option_rects = []

    while pause_menu_active:
        screen.fill((0, 0, 0))
        set_opacity(screen, 255)
        option_rects.clear()
        for i, option in enumerate(menu_options):
            color = (255, 255, 255) if i == selected_option else (100, 100, 100)
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 200 + i * 50))
            option_rects.append(text_rect)
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Continue
                        pause_menu_active = False
                    elif selected_option == 1:  # Reset
                        world = make_random_grid(xlen, ylen)
                        iteration_count = 0
                        pause_menu_active = False
                    elif event.key == pygame.K_ESCAPE:
                        pause_menu_active = False
                    elif selected_option == 2:  # Close
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    mouse_pos = event.pos
                    for i, rect in enumerate(option_rects):
                        if is_point_in_rect(mouse_pos, rect):
                            selected_option = i
                            if selected_option == 0:  # Continue
                                pause_menu_active = False
                            elif selected_option == 1:  # Reset
                                world = make_random_grid(xlen, ylen)
                                iteration_count = 0
                                pause_menu_active = False
                            elif selected_option == 2:  # Close
                                pygame.quit()
                                sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def handleInputEvents(xlen, ylen):
    global pause_menu_active
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                global world, iteration_count
                world = make_random_grid(xlen, ylen)
                iteration_count = 0  # Reset iteration count
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if pause_menu_active:
                    pause_menu_active = False
                else:
                    pause_menu(screen, xlen, ylen)
        if event.type == pygame.QUIT:  # pygame issues a quit event, for e.g. by closing the window
            print("quitting")
            sys.exit(0)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    global screen
    screen = createScreen()
    (xmax, ymax) = screen.get_size()
    h = 0
    cell_number = 0
    alive_color = pygame.Color(0, 0, 0)
    alive_color.hsva = [h, 100, 100]

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
        screen.fill((0, 0, 0))  # Clear the screen before drawing
        if not pause_menu_active:
            set_opacity(screen, 0)
            clock.tick(40)
            for x in range(xlen):
                for y in range(ylen):
                    alive = world[x][y]
                    cell_number += 1
                    cell_color = alive_color if alive else BLACK
                    draw_block(x, y, cell_color)

            iteration_count += 1

            # Draw background rectangle for iteration count
            pygame.draw.rect(screen, (0, 0, 0), (10, 10, 200, 40))
            iteration_text = font.render(f"Iteration: {iteration_count}", True, (255, 255, 255))
            screen.blit(iteration_text, (15, 15))

            pygame.display.flip()
            h = (h + 2) % 360
            alive_color.hsva = (h, 100, 100)
            world = evolve(world)
            cell_number = 0
        else:
            set_opacity(screen, 255)

if __name__ == '__main__':
    main()