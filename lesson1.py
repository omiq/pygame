import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600 # Adjust the WIDTH and HEIGHT to your preferred screen size.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Window title
pygame.display.set_caption("UFO Game (Move the Sprite with Cursor Keys)")


# Function to safely load an image
def load_image(filename):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        pygame.quit()
        sys.exit()

    try:
        image = pygame.image.load(filename).convert_alpha()
        return image
    except pygame.error:
        print(f"Error loading image: {filename}")
        pygame.quit()
        sys.exit()

# Load images with error trapping
background = load_image("background.png")
sprite = load_image("sprite.png")

# Sprite initial position
sprite_x, sprite_y = (WIDTH - sprite.get_width()) // 2, (HEIGHT - sprite.get_height()) // 2

# The sprite's movement speed can be adjusted by changing sprite_speed
sprite_speed = 5

# Internal game clock
clock = pygame.time.Clock()

# Main loop
running = True # Change to False to quit
while running:
    screen.blit(background, (0, 0))
    screen.blit(sprite, (sprite_x, sprite_y))

    # Go through any events that have been raised
    for event in pygame.event.get():

        # Closing the window doesn't shut off the game!
        if event.type == pygame.QUIT: # Check to see if we need to exit
            running = False           # If so, set our variable to False

    # Get any currently depressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        sprite_x -= sprite_speed
    if keys[pygame.K_RIGHT]:
        sprite_x += sprite_speed
    if keys[pygame.K_UP]:
        sprite_y -= sprite_speed
    if keys[pygame.K_DOWN]:
        sprite_y += sprite_speed

    # Swap the screen buffer to display
    pygame.display.flip()

    # Limit the game loop to a steady 60 frames per second
    clock.tick(60)

# Need both to be sure we release memory and processor
pygame.quit()
sys.exit()
