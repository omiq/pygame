import os

# Initialize Pygame without the start message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame


# Constants
TILE_SIZE = 32
GRID_SIZE = 32
SCREEN_SIZE = TILE_SIZE * GRID_SIZE

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Tile Grid")

# Try loading the tile image
tile_path = "floor.png"
if os.path.exists(tile_path):
    tile_image = pygame.image.load(tile_path)
    tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
else:
    # Create a fallback tile if the image isn't found
    tile_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile_image.fill((150, 150, 150))  # Grey background
    
    # Draw black lines on bottom and right
    pygame.draw.line(tile_image, (0, 0, 0), (0, TILE_SIZE - 1), (TILE_SIZE - 1, TILE_SIZE - 1), 2)  # Bottom line
    pygame.draw.line(tile_image, (0, 0, 0), (TILE_SIZE - 1, 0), (TILE_SIZE - 1, TILE_SIZE - 1), 2)  # Right line

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Black background
    
    # Draw the tile grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            screen.blit(tile_image, (col * TILE_SIZE, row * TILE_SIZE))

    pygame.display.flip()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
