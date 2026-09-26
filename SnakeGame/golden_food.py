import pygame
import random
import math

from settings import *
import settings
from image_loader import golden_food


class GoldenFood:

    def __init__(self):

        self.position = self.generate()

        self.active = False

        self.timer = 0

        self.spawn_counter = 0

        self.life_time = 0


    # ---------------------------------
    # Generate Random Position
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
    # Spawn Golden Food
    # ---------------------------------

    def new_food(self):

        self.position = self.generate()

        self.active = True

        self.life_time = 0


    # ---------------------------------
    # Hide Golden Food
    # ---------------------------------

    def hide(self):

        self.active = False

        self.spawn_counter = 0


    # ---------------------------------
    # Automatic Spawn & Remove
    # ---------------------------------

    def logic(self):

        if self.active:

            self.life_time += 1

            # Disappear after about 8 seconds
            if self.life_time > FPS * 8:
                self.hide()

        else:

            self.spawn_counter += 1

            # Spawn every 25 seconds
            if self.spawn_counter > FPS * 25:
                self.new_food()


    # ---------------------------------
    # Animation
    # ---------------------------------

    def update(self):

        self.logic()

        self.timer += 0.25


    # ---------------------------------
    # Draw Golden Food
    # ---------------------------------

    def draw(self, screen):

        self.update()

        if not self.active:
            return

        # Pulsing Size
        scale = 1 + math.sin(self.timer) * 0.12
        size = int(BLOCK_SIZE * scale)

        image = pygame.transform.smoothscale(
            golden_food,
            (size, size)
        )

        # Glow
        glow = pygame.Surface(
            (BLOCK_SIZE + 30, BLOCK_SIZE + 30),
            pygame.SRCALPHA
        )

        alpha = int(
            120 + 70 * abs(math.sin(self.timer))
        )

        pygame.draw.circle(
            glow,
            (255, 215, 0, alpha),
            (
                glow.get_width() // 2,
                glow.get_height() // 2
            ),
            BLOCK_SIZE // 2 + 10
        )

        screen.blit(
            glow,
            (
                self.position[0] - 15,
                self.position[1] - 15
            )
        )

        screen.blit(
            image,
            (
                self.position[0] - (size - BLOCK_SIZE) // 2,
                self.position[1] - (size - BLOCK_SIZE) // 2
            )
        )

        # Sparkles
        for angle in range(0, 360, 45):

            x = (
                self.position[0]
                + BLOCK_SIZE // 2
                + math.cos(
                    math.radians(angle + self.timer * 40)
                ) * 18
            )

            y = (
                self.position[1]
                + BLOCK_SIZE // 2
                + math.sin(
                    math.radians(angle + self.timer * 40)
                ) * 18
            )

            pygame.draw.circle(
                screen,
                (255, 255, 180),
                (int(x), int(y)),
                2
            )