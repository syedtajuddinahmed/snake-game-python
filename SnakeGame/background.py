import pygame
import random

from settings import *
import settings

class Star:

    def __init__(self):

        self.x = random.randint(0, settings.WIDTH)
        self.y = random.randint(0, settings.HEIGHT)

        self.radius = random.randint(1, 3)

        self.speed = random.uniform(0.3, 1.0)

    def update(self):

        self.y += self.speed

        if self.y > settings.HEIGHT:
            self.y = 0
            self.x = random.randint(0, settings.WIDTH)

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            (90, 90, 90),
            (int(self.x), int(self.y)),
            self.radius
        )


class Background:

    def __init__(self):

        self.stars = []

        for _ in range(80):
            self.stars.append(Star())

    def update(self):

        for star in self.stars:
            star.update()

    def draw(self, screen):

        for star in self.stars:
            star.draw(screen)

    def resize(self):
        # Re-scatter the stars so they cover the whole (possibly
        # newly maximized) canvas instead of only the old corner.
        self.stars = []

        for _ in range(80):
            self.stars.append(Star())