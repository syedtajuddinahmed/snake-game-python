import pygame
import random
import math

from settings import *
import settings
from image_loader import bonus_food


class BonusFood:

    def __init__(self):

        self.position = self.generate()
        self.timer = 0

    # =================================
    # Generate Random Position
    # =================================

    def generate(self):

        while True:

            pos = (
                random.randrange(0, settings.WIDTH, BLOCK_SIZE),
                random.randrange(0, settings.HEIGHT, BLOCK_SIZE)
            )

            if not in_hud_zone(pos):
                return pos

    # =================================
    # Spawn New Bonus Food
    # =================================

    def new_food(self):

        self.position = self.generate()

    # =================================
    # Animation Timer
    # =================================

    def update(self):

        self.timer += 0.20

    # =================================
    # Draw Bonus Food
    # =================================

    def draw(self, screen):

        self.update()

        # Floating animation
        offset = math.sin(self.timer) * 3

        # Pulsing animation
        scale = 1 + math.sin(self.timer * 2) * 0.08

        size = int(BLOCK_SIZE * scale)

        image = pygame.transform.smoothscale(
            bonus_food,
            (size, size)
        )

        # Blue Glow
        glow = pygame.Surface(
            (BLOCK_SIZE + 20, BLOCK_SIZE + 20),
            pygame.SRCALPHA
        )

        alpha = int(80 + 60 * abs(math.sin(self.timer)))

        pygame.draw.circle(
            glow,
            (80, 170, 255, alpha),
            (
                glow.get_width() // 2,
                glow.get_height() // 2
            ),
            BLOCK_SIZE // 2 + 6
        )

        screen.blit(
            glow,
            (
                self.position[0] - 10,
                self.position[1] - 10 + offset
            )
        )

        screen.blit(
            image,
            (
                self.position[0] - (size - BLOCK_SIZE) // 2,
                self.position[1] - (size - BLOCK_SIZE) // 2 + offset
            )
        )