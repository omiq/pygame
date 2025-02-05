import os
import random

# Suppress Pygame startup message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

# Constants
TILE_SIZE = 32
GRID_SIZE = 32
SCREEN_SIZE = TILE_SIZE * GRID_SIZE

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Tile Maze Generation")

# Create tile surfaces
def create_tile(right_line=True, bottom_line=True):
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile.fill((150, 150, 150))  # Grey background
    
    if bottom_line:
        pygame.draw.line(tile, (0, 0, 0), (0, TILE_SIZE - 1), (TILE_SIZE - 1, TILE_SIZE - 1), 2)  # Bottom line
    if right_line:
        pygame.draw.line(tile, (0, 0, 0), (TILE_SIZE - 1, 0), (TILE_SIZE - 1, TILE_SIZE - 1), 2)  # Right line
    
    return tile

# Create all tile variations
tile_default = create_tile(True, True)     # Both walls
tile_no_right = create_tile(False, True)   # No right wall
tile_no_bottom = create_tile(True, False)  # No bottom wall
tile_open = create_tile(False, False)      # No walls

# Grid to store tile types
tile_grid = [[tile_default for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Directions for movement
DIRECTIONS = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0)
}

# Create stack and visited set
stack = []
visited = set()

# Start at (0,0)
current_x, current_y = 0, 0
visited.add((current_x, current_y))
stack.append((current_x, current_y))

# Maze generation loop
running = True
while running:
    screen.fill((0, 0, 0))  # Black background

    # Draw the grid with updated tiles
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            screen.blit(tile_grid[row][col], (col * TILE_SIZE, row * TILE_SIZE))

    pygame.display.flip()

    # Check possible unvisited neighbors
    neighbors = []
    for direction, (dx, dy) in DIRECTIONS.items():
        nx, ny = current_x + dx, current_y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in visited:
            neighbors.append((nx, ny, direction))

    if neighbors:
        # Choose a random unvisited neighbor
        next_x, next_y, direction = random.choice(neighbors)

        # Update the current tile based on movement
        if direction == "E":  # Moving right
            if tile_grid[current_y][current_x] == tile_no_bottom:
                tile_grid[current_y][current_x] = tile_open  # Already removed bottom, now remove right
            else:
                tile_grid[current_y][current_x] = tile_no_right  # Remove right only
        elif direction == "S":  # Moving down
            if tile_grid[current_y][current_x] == tile_no_right:
                tile_grid[current_y][current_x] = tile_open  # Already removed right, now remove bottom
            else:
                tile_grid[current_y][current_x] = tile_no_bottom  # Remove bottom only

        # Mark as visited and continue
        visited.add((next_x, next_y))
        stack.append((next_x, next_y))
        current_x, current_y = next_x, next_y
    else:
        # Backtrack if no unvisited neighbors
        if stack:
            current_x, current_y = stack.pop()
        else:
            running = False  # Exit when all tiles visited

# Wait for a keypress or mouse click before quitting
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            waiting = False  # Exit on keypress or mouse click

pygame.quit()
