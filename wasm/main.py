import asyncio
import os
import random

# Suppress Pygame startup message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

# Constants
TILE_SIZE = 16
GRID_SIZE = 30
SCREEN_WIDTH = TILE_SIZE * GRID_SIZE
SCREEN_HEIGHT = TILE_SIZE * GRID_SIZE + 50  # Extra space for message
FONT_SIZE = 24

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Generator")

# Load font
font = pygame.font.Font(None, FONT_SIZE)

# Load and set window icon (optional)
try:
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
except FileNotFoundError:
    pass  # If no icon is found, continue without error

# Create tile surfaces
def create_tile(right_line=True, bottom_line=True, left_line=True, top_line=True):
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile.fill((150, 150, 150))  # Grey background

    if bottom_line:
        pygame.draw.line(tile, (0, 0, 0), (0, TILE_SIZE - 1), (TILE_SIZE - 1, TILE_SIZE - 1), 2)  # Bottom
    if right_line:
        pygame.draw.line(tile, (0, 0, 0), (TILE_SIZE - 1, 0), (TILE_SIZE - 1, TILE_SIZE - 1), 2)  # Right
    if left_line:
        pygame.draw.line(tile, (0, 0, 0), (0, 0), (0, TILE_SIZE - 1), 2)  # Left
    if top_line:
        pygame.draw.line(tile, (0, 0, 0), (0, 0), (TILE_SIZE - 1, 0), 2)  # Top

    return tile

# Maze generation function
async def generate_maze():
    # Generate full grid with walls
    tile_grid = [[create_tile() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    visited = set()
    stack = []

    # Directions: (dx, dy, opposite_direction)
    DIRECTIONS = {
        "N": (0, -1, "S"),
        "S": (0, 1, "N"),
        "E": (1, 0, "W"),
        "W": (-1, 0, "E"),
    }

    # Start at (0,0)
    current_x, current_y = 0, 0
    visited.add((current_x, current_y))
    stack.append((current_x, current_y))

    # Store wall states
    tile_walls = {(x, y): {"N": True, "S": True, "E": True, "W": True} for x in range(GRID_SIZE) for y in range(GRID_SIZE)}

    # Maze generation loop
    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear screen

        # Draw the grid with updated tiles
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                walls = tile_walls[(col, row)]
                tile_grid[row][col] = create_tile(walls["E"], walls["S"], walls["W"], walls["N"])
                screen.blit(tile_grid[row][col], (col * TILE_SIZE, row * TILE_SIZE))

        # Highlight the current tile in red
        pygame.draw.rect(screen, (255, 0, 0), (current_x * TILE_SIZE, current_y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

        pygame.display.flip()
        await asyncio.sleep(0)  # Yield control to avoid blocking the event loop

        # Get unvisited neighbors
        neighbors = []
        for direction, (dx, dy, opposite) in DIRECTIONS.items():
            nx, ny = current_x + dx, current_y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in visited:
                neighbors.append((nx, ny, direction, opposite))

        if neighbors:
            # Choose a random unvisited neighbor
            next_x, next_y, direction, opposite = random.choice(neighbors)

            # Remove walls between the current and next tile
            tile_walls[(current_x, current_y)][direction] = False
            tile_walls[(next_x, next_y)][opposite] = False

            # Mark as visited and move
            visited.add((next_x, next_y))
            stack.append((next_x, next_y))
            current_x, current_y = next_x, next_y
        else:
            # Backtrack
            if stack:
                current_x, current_y = stack.pop()
            else:
                running = False  # Exit when all tiles are visited
                
    pygame.display.update()
    await asyncio.sleep(0)
    return tile_grid, tile_walls

# Main game loop
async def main():
    while True:  # Infinite loop to allow maze regeneration
        # Generate a new maze
        tile_grid, tile_walls = await generate_maze()

        # Show the message after the maze is complete
        message = "Press ENTER to generate a new maze."
        text_surface = font.render(message, True, (255, 255, 255))
        screen.blit(text_surface, (20, SCREEN_HEIGHT - 40))
        pygame.display.flip()

        # Wait for user to press ENTER to regenerate
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Press ENTER to restart
                        waiting = False  # Exit waiting loop, regenerate the maze
                elif event.type == pygame.QUIT:  # Close tab to exit in browser
                    return  # Exit the function, stopping the game

            pygame.display.update()
            await asyncio.sleep(0)  # Yield control

# Ensure Pygbag works correctly
if __name__ == "__main__":
    asyncio.ensure_future(main())
