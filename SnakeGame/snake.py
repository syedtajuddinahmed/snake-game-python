import pygame
import math

from settings import *
import settings
from snake_effects import SnakeEffects


class Snake:

    def __init__(self):

        self.body = [
        (200,200),
        (180,200),
        (160,200)
]

        self.direction = "RIGHT"
        self.grow_body = False

        # Snake Effects
        self.effects = SnakeEffects()

    # =================================
    # Change Direction
    # =================================

    def change_direction(self, new_direction):

        if new_direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"

        elif new_direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"

        elif new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"

        elif new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

    # =================================
    # Move Snake
    # =================================

    def move(self):

        x, y = self.body[0]

        if self.direction == "UP":
            y -= BLOCK_SIZE

        elif self.direction == "DOWN":
            y += BLOCK_SIZE

        elif self.direction == "LEFT":
            x -= BLOCK_SIZE

        elif self.direction == "RIGHT":
            x += BLOCK_SIZE

        self.body.insert(0, (x, y))

        if not self.grow_body:
            self.body.pop()
        else:
            self.grow_body = False

    # =================================
    # Grow Snake
    # =================================

    def grow(self):
        self.grow_body = True

    # =================================
    # Snake Head
    # =================================

    def head(self):
        return self.body[0]

    # =================================
    # Wall Collision
    # =================================

    def wall_collision(self):

        x, y = self.head()

        return (
            x < 0 or
            x >= settings.WIDTH or
            y < 0 or
            y >= settings.HEIGHT
        )

    # =================================
    # Self Collision
    # =================================

    def self_collision(self):
        return self.head() in self.body[1:]

    # =================================
    # HUD Panel Collision
    # =================================

    def hud_collision(self):
        return in_hud_zone(self.head())

    # =================================
    # Render Positions (with slither wave)
    # =================================
    # Body cells stay perfectly grid-aligned for movement/collision.
    # For drawing only, each segment is nudged sideways (perpendicular
    # to the direction it's travelling) in a small sine wave, so the
    # snake reads as a flexible body rather than a rigid chain of
    # blocks. The head (i = 0) always has zero offset so the eyes,
    # tongue and steering stay crisp.

    def _render_positions(self):

        n = len(self.body)
        positions = []

        for i in range(n):

            x, y = self.body[i]
            cx = x + BLOCK_SIZE // 2
            cy = y + BLOCK_SIZE // 2

            prev_x, prev_y = self.body[max(i - 1, 0)]
            next_x, next_y = self.body[min(i + 1, n - 1)]

            dx = next_x - prev_x
            dy = next_y - prev_y
            length = math.hypot(dx, dy)

            if length == 0:
                perp = (0, 0)
            else:
                perp = (-dy / length, dx / length)

            t = i / max(1, n - 1)
            amplitude = 2.5 * min(1.0, t * 2)

            wave = math.sin(self.effects.timer * 2.2 - i * 0.9) * amplitude

            positions.append(
                (cx + perp[0] * wave, cy + perp[1] * wave)
            )

        return positions

    @staticmethod
    def _ipos(point):
        return (int(round(point[0])), int(round(point[1])))

    # =================================
    # Draw Snake
    # =================================

    def draw(self, screen):

        # Update animation timer
        self.effects.update()

        n = len(self.body)
        positions = self._render_positions()

        # Realistic green snake-skin palette, bright near the head and
        # deepening toward the tail for a natural scaled look
        LIGHT = (118, 195, 72)    # fresh grass green, near the head
        MID = (62, 140, 58)       # rich mid green
        DARK = (24, 74, 40)       # deep forest green, toward the tail
        BLOTCH = (18, 56, 30)     # dark saddle-blotch markings

        def segment_color(i):
            t = i / max(1, n - 1)
            if t < 0.5:
                a, b, k = LIGHT, MID, t / 0.5
            else:
                a, b, k = MID, DARK, (t - 0.5) / 0.5
            return tuple(int(a[c] + (b[c] - a[c]) * k) for c in range(3))

        def segment_radius(i):
            t = i / max(1, n - 1)
            return max(4, int(BLOCK_SIZE // 2 - t * 4))

        def segment_is_horizontal(i):
            x0, y0 = self.body[max(i - 1, 0)]
            x1, y1 = self.body[min(i + 1, n - 1)]
            return abs(x1 - x0) >= abs(y1 - y0)

        # -------------------------
        # Drop shadow (grounds the snake instead of floating on the grid)
        # -------------------------

        shadow = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        for i in range(n):
            p = self._ipos(positions[i])
            r = segment_radius(i)
            pygame.draw.circle(shadow, (0, 0, 0, 50), (p[0] + 3, p[1] + 5), r)

        screen.blit(shadow, (0, 0))

        # -------------------------
        # Body tube (tail to neck), one continuous shape
        # -------------------------

        for i in range(n - 1, 0, -1):

            p1 = self._ipos(positions[i])
            p2 = self._ipos(positions[i - 1])
            r1 = segment_radius(i)
            r2 = segment_radius(i - 1)
            color = segment_color(i)

            # Thick connecting line + circle joints keep the tube smooth
            # through turns instead of showing blocky rectangle corners
            pygame.draw.line(screen, color, p1, p2, r1 + r2)
            pygame.draw.circle(screen, color, p1, r1)

        if n > 1:
            p1 = self._ipos(positions[1])
            pygame.draw.circle(screen, segment_color(1), p1, segment_radius(1))

        # -------------------------
        # Dorsal saddle-blotch markings (like a python/viper pattern)
        # -------------------------

        for i in range(n - 1, 0, -1):

            if i % 3 != 0:
                continue

            p = self._ipos(positions[i])
            r = segment_radius(i)

            if segment_is_horizontal(i):
                rect = (p[0] - int(r * 0.55), p[1] - int(r * 0.85), int(r * 1.1), int(r * 1.7))
            else:
                rect = (p[0] - int(r * 0.85), p[1] - int(r * 0.55), int(r * 1.7), int(r * 1.1))

            pygame.draw.ellipse(screen, BLOTCH, rect)

        # -------------------------
        # Fine scale texture on top of the tube
        # -------------------------

        for i in range(n - 1, 0, -1):

            p = self._ipos(positions[i])
            color = segment_color(i)
            r = segment_radius(i)
            scale_color = tuple(max(0, c - 22) for c in color)

            offset = 0 if i % 2 == 0 else max(2, r // 2)

            for side in (-1, 1):
                sx = p[0] + side * max(2, r // 2)
                sy = p[1] + offset - r // 2
                pygame.draw.ellipse(
                    screen,
                    scale_color,
                    (sx - 2, sy - 2, 4, 3)
                )

        # -------------------------
        # Head
        # -------------------------

        segment = self.body[0]
        center = self._ipos(positions[0])

        # Head shape, elongated and slightly narrower than the neck,
        # like a real snake's head tapering to the snout
        if self.direction in ("LEFT", "RIGHT"):
            head_rect = pygame.Rect(0, 0, BLOCK_SIZE + 8, BLOCK_SIZE - 3)
        else:
            head_rect = pygame.Rect(0, 0, BLOCK_SIZE - 3, BLOCK_SIZE + 8)

        head_rect.center = center

        HEAD_COLOR = (128, 200, 78)
        HEAD_OUTLINE = (22, 58, 32)

        pygame.draw.ellipse(
            screen,
            HEAD_COLOR,
            head_rect
        )

        # Dark post-ocular stripe running back from the eye, a marking
        # common to many real snake species
        DIR_VECTOR = {
            "RIGHT": (1, 0),
            "LEFT": (-1, 0),
            "UP": (0, -1),
            "DOWN": (0, 1),
        }
        dxh, dyh = DIR_VECTOR[self.direction]
        perph = (-dyh, dxh)

        stripe_a = (
            center[0] - dxh * 2 + perph[0] * 6,
            center[1] - dyh * 2 + perph[1] * 6,
        )
        stripe_b = (
            center[0] - dxh * (BLOCK_SIZE // 2) + perph[0] * 6,
            center[1] - dyh * (BLOCK_SIZE // 2) + perph[1] * 6,
        )
        stripe_c = (
            center[0] - dxh * 2 - perph[0] * 6,
            center[1] - dyh * 2 - perph[1] * 6,
        )
        stripe_d = (
            center[0] - dxh * (BLOCK_SIZE // 2) - perph[0] * 6,
            center[1] - dyh * (BLOCK_SIZE // 2) - perph[1] * 6,
        )
        pygame.draw.line(screen, HEAD_OUTLINE, stripe_a, stripe_b, 2)
        pygame.draw.line(screen, HEAD_OUTLINE, stripe_c, stripe_d, 2)

        pygame.draw.ellipse(
            screen,
            HEAD_OUTLINE,
            head_rect,
            2
        )
        perp = perph

        nose = (
            center[0] + dxh * (BLOCK_SIZE // 2 - 3),
            center[1] + dyh * (BLOCK_SIZE // 2 - 3),
        )

        # Nostrils, placed toward the front of the snout
        for side in (-1, 1):
            pygame.draw.circle(
                screen,
                (8, 22, 12),
                (
                    int(nose[0] + perp[0] * 3 * side),
                    int(nose[1] + perp[1] * 3 * side),
                ),
                1
            )

        # Eyes - amber iris with a vertical slit pupil, like a pit viper
        eye_radius = 3
        IRIS = (200, 165, 40)
        PUPIL = (12, 9, 5)

        if self.direction == "RIGHT":
            eyes = [(14, 5), (14, 15)]

        elif self.direction == "LEFT":
            eyes = [(6, 5), (6, 15)]

        elif self.direction == "UP":
            eyes = [(6, 6), (14, 6)]

        else:
            eyes = [(6, 14), (14, 14)]

        for ex, ey in eyes:

            eye_pos = (segment[0] + ex, segment[1] + ey)

            # Dark ring grounds the eye against the head color
            pygame.draw.circle(screen, (18, 40, 22), eye_pos, eye_radius + 1)
            pygame.draw.circle(screen, IRIS, eye_pos, eye_radius)

            # Vertical slit pupil, oriented across the direction of travel
            if self.direction in ("LEFT", "RIGHT"):
                pupil_rect = (eye_pos[0] - 1, eye_pos[1] - eye_radius, 2, eye_radius * 2)
            else:
                pupil_rect = (eye_pos[0] - eye_radius, eye_pos[1] - 1, eye_radius * 2, 2)
            pygame.draw.ellipse(screen, PUPIL, pupil_rect)

            # Tiny glint for a bit of life
            pygame.draw.circle(
                screen,
                (255, 245, 210),
                (eye_pos[0] - 1, eye_pos[1] - 1),
                1
            )

        # Animated forked tongue
        self.effects.draw_tongue(
            screen,
            segment,
            self.direction
        )