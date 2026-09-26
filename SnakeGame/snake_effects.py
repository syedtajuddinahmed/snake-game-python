import pygame
import math

from settings import *


class SnakeEffects:

    def __init__(self):

        self.timer = 0

    def update(self):

        self.timer += 0.2

    def draw_tongue(self, screen, position, direction):

        x = position[0] + BLOCK_SIZE // 2
        y = position[1] + BLOCK_SIZE // 2

        length = 8 + abs(math.sin(self.timer * 5)) * 4
        TONGUE = (30, 20, 20)
        fork = 3

        DIR_VECTOR = {
            "RIGHT": (1, 0),
            "LEFT": (-1, 0),
            "UP": (0, -1),
            "DOWN": (0, 1),
        }
        dx, dy = DIR_VECTOR[direction]
        perp = (-dy, dx)

        base = (x + dx * 8, y + dy * 8)
        tip = (x + dx * (8 + length), y + dy * (8 + length))

        # A short straight base with a small forked tip, like a real
        # flicking snake tongue rather than a solid red line
        pygame.draw.line(screen, TONGUE, base, tip, 2)

        for side in (-1, 1):
            fork_tip = (
                tip[0] + dx * 3 + perp[0] * fork * side,
                tip[1] + dy * 3 + perp[1] * fork * side,
            )
            pygame.draw.line(screen, TONGUE, tip, fork_tip, 2)