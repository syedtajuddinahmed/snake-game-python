import pygame

from settings import *
import settings


class Level:

    def __init__(self):

        self.level = 1

        self.speed = 5
        self.show_level_up = False

        self.level_timer = 0

    # =====================================
    # UPDATE LEVEL
    # =====================================

    def update(self, score):

        new_level = score // 100 + 1

        if new_level > self.level:

            self.level = new_level

            self.speed = 5 + (self.level - 1)

            self.show_level_up = True

            self.level_timer = 60

    # =====================================
    # GET SPEED
    # =====================================

    def get_speed(self):

        return self.speed

    # =====================================
    # DRAW LEVEL-UP ANIMATION
    # =====================================

    def draw(self, screen):

        if self.show_level_up:

            font_size = 45 + (60 - self.level_timer) // 2

            font = pygame.font.SysFont(
                "Arial",
                font_size,
                bold=True
            )

            text = font.render(
                "LEVEL UP!",
                True,
                (255, 215, 0)
            )

            screen.blit(
                text,
                (
                    settings.WIDTH // 2 - text.get_width() // 2,
                    settings.HEIGHT // 2 - text.get_height() // 2
                )
            )

            self.level_timer -= 1

            if self.level_timer <= 0:

                self.show_level_up = False