import os

# ======================================
# SCREEN SETTINGS
# ======================================

WIDTH = 600
HEIGHT = 560

TITLE = "Snake Game"

# ======================================
# GAME SETTINGS
# ======================================

BLOCK_SIZE = 20

# Difficulty Speeds
EASY_SPEED = 5
MEDIUM_SPEED = 8
HARD_SPEED = 12

# Default Speed
FPS = MEDIUM_SPEED

# ======================================
# HUD SAFE ZONE
# ======================================
# The Score / High / Level panel is drawn in the top-left corner
# (see score.py). Nothing (food, obstacles, the snake) should be
# allowed to occupy this rectangle.

HUD_ZONE = (0, 0, 140, 80)  # (x, y, width, height) in pixels


def in_hud_zone(position):

    x, y = position
    hx, hy, hw, hh = HUD_ZONE

    return (
        hx <= x < hx + hw
        and hy <= y < hy + hh
    )

# ======================================
# COLORS
# ======================================

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# ======================================
# IMAGE FOLDER
# ======================================

IMAGE_PATH = os.path.join(
    os.path.dirname(__file__),
    "images"
)