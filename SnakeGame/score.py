import os
import pygame

from settings import *


class Score:

    def __init__(self):

        self.score = 0

        self.high_score = 0

        self.file = "high_score.txt"

        self.load()

    # =====================================
    # ADD SCORE
    # =====================================

    def add(self, points=10):

        self.score += points

        if self.score > self.high_score:

            self.high_score = self.score

    # =====================================
    # LOAD HIGH SCORE
    # =====================================

    def load(self):

        if os.path.exists(self.file):

            with open(self.file, "r") as f:

                data = f.read().strip()

                if data.isdigit():

                    self.high_score = int(data)

                else:

                    self.high_score = 0

        else:

            self.high_score = 0

    # =====================================
    # SAVE HIGH SCORE
    # =====================================

    def save(self):

        with open(self.file, "w") as f:

            f.write(str(self.high_score))

    # =====================================
    # RESET SCORE
    # =====================================

    def reset(self):

        self.score = 0

    # =====================================
    # DRAW SCORE PANEL
    # =====================================

    def draw(self, screen, level):

        font = pygame.font.SysFont(
            "Arial",
            15,
            bold=True
        )

        # Background Box
        pygame.draw.rect(
            screen,
            (25, 25, 25),
            (6, 6, 130, 72),
            border_radius=8
        )

        # Border
        pygame.draw.rect(
            screen,
            (80, 80, 80),
            (6, 6, 130, 72),
            2,
            border_radius=8
        )

        # Score
        score_text = font.render(
            f"Score : {self.score}",
            True,
            WHITE
        )

        # High Score
        high_text = font.render(
            f"High : {self.high_score}",
            True,
            (255, 215, 0)
        )

        # Level
        level_text = font.render(
            f"Level : {level.level}",
            True,
            (0, 255, 0)
        )

        screen.blit(score_text, (14, 12))
        screen.blit(high_text, (14, 34))
        screen.blit(level_text, (14, 56))