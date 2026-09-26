import pygame
import random

from settings import *
import settings
from image_loader import obstacle



class Obstacle:

    def __init__(self):

        self.blocks = []



    # Generate obstacles
    def generate(self, level):

        self.blocks = []


        count = level + 2


        for i in range(count):

            while True:

                x = random.randrange(
                    0,
                    settings.WIDTH,
                    BLOCK_SIZE
                )

                y = random.randrange(
                    0,
                    settings.HEIGHT,
                    BLOCK_SIZE
                )

                if not in_hud_zone((x, y)):
                    break

            self.blocks.append(
                (x,y)
            )




    # Draw obstacle image
    def draw(self, screen):


        for block in self.blocks:


            screen.blit(
                obstacle,
                block
            )




    # Collision check
    def collision(self, snake_head):

        return snake_head in self.blocks