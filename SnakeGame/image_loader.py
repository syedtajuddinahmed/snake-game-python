import os
import pygame

from settings import *

# ---------------------------------
# Image Path Helper
# ---------------------------------

def load_image(filename):
    path = os.path.join(IMAGE_PATH, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")

    return pygame.image.load(path)


# ---------------------------------
# Load Images
# ---------------------------------

snake_head = load_image("snake_head.png")
snake_body = load_image("snake_body.png")
food = load_image("food.png")
bonus_food = load_image("bonus_food.png")

# Use the same image for Golden Food
golden_food = load_image("bonus_food.png")

obstacle = load_image("obstacle.png")


# ---------------------------------
# Resize Images
# ---------------------------------

snake_head = pygame.transform.scale(
    snake_head,
    (BLOCK_SIZE, BLOCK_SIZE)
)

snake_body = pygame.transform.scale(
    snake_body,
    (BLOCK_SIZE, BLOCK_SIZE)
)

food = pygame.transform.scale(
    food,
    (BLOCK_SIZE, BLOCK_SIZE)
)

bonus_food = pygame.transform.scale(
    bonus_food,
    (BLOCK_SIZE, BLOCK_SIZE)
)

golden_food = pygame.transform.scale(
    golden_food,
    (BLOCK_SIZE, BLOCK_SIZE)
)

obstacle = pygame.transform.scale(
    obstacle,
    (BLOCK_SIZE, BLOCK_SIZE)
)