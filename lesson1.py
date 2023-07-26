import pygame
import sys

pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UFO Game (Move the Sprite with Cursor Keys)")

# Load images
background = pygame.image.load("background.png").convert_alpha()
sprite = pygame.image.load("sprite.png").convert_alpha()

# Sprite initial position
sprite_x, sprite_y = (WIDTH - sprite.get_width()) // 2, (HEIGHT - sprite.get_height()) // 2
sprite_speed = 5

clock = pygame.time.Clock()

# Main loop
running = True
while running:
    screen.blit(background, (0, 0))
    screen.blit(sprite, (sprite_x, sprite_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        sprite_x -= sprite_speed
    if keys[pygame.K_RIGHT]:
        sprite_x += sprite_speed
    if keys[pygame.K_UP]:
        sprite_y -= sprite_speed
    if keys[pygame.K_DOWN]:
        sprite_y += sprite_speed

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
