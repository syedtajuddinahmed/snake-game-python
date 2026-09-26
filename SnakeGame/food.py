import pygame
import random
import math

from settings import *
import settings
from image_loader import food


class Food:

    def __init__(self):
        self.position = self.generate()
        self.size = BLOCK_SIZE
        self.timer = 0

    # ---------------------------------
    # Generate random position
    # ---------------------------------
    def generate(self):
        while True:
            pos = (
                random.randrange(0, settings.WIDTH, BLOCK_SIZE),
                random.randrange(0, settings.HEIGHT, BLOCK_SIZE)
            )
            if not in_hud_zone(pos):
                return pos

    # ---------------------------------
    # Create new food
    # ---------------------------------
    def new_food(self):
        self.position = self.generate()

    # ---------------------------------
    # Update animation
    # ---------------------------------
    def update(self):
        self.timer += 0.15

    # ---------------------------------
    # Draw animated food
    # ---------------------------------
    def draw(self, screen):

        self.update()

        # Floating animation
        offset = math.sin(self.timer) * 4

        # Glowing animation
        glow = abs(math.sin(self.timer)) * 25

        glow_surface = pygame.Surface(
            (BLOCK_SIZE + 12, BLOCK_SIZE + 12),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow_surface,
            (255, 80, 80, int(glow)),
            (
                glow_surface.get_width() // 2,
                glow_surface.get_height() // 2
            ),
            BLOCK_SIZE // 2 + 6
        )

        screen.blit(
            glow_surface,
            (
                self.position[0] - 6,
                self.position[1] - 6 + offset
            )
        )

        screen.blit(
            food,
            (
                self.position[0],
                self.position[1] + offset
            )
        )