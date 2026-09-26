import pygame
import random


class Particle:

    def __init__(self, x, y, color):

        self.x = x
        self.y = y

        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(-3, 3)

        self.radius = random.randint(3, 6)

        self.life = 30

        self.color = color

    def update(self):

        self.x += self.dx
        self.y += self.dy

        self.life -= 1

        if self.radius > 0.1:
            self.radius *= 0.94

    def draw(self, screen):

        if self.life > 0:

            pygame.draw.circle(
                screen,
                self.color,
                (int(self.x), int(self.y)),
                int(self.radius)
            )


class ParticleSystem:

    def __init__(self):

        self.particles = []

    # ==============================
    # Create Particles
    # ==============================

    def create(self, x, y, color, amount=20):

        for _ in range(amount):

            self.particles.append(
                Particle(x, y, color)
            )

    # ==============================
    # Update Particles
    # ==============================

    def update(self):

        for particle in self.particles[:]:

            particle.update()

            if particle.life <= 0:

                self.particles.remove(particle)

    # ==============================
    # Draw Particles
    # ==============================

    def draw(self, screen):

        for particle in self.particles:

            particle.draw(screen)

    # ==============================
    # Clear All Particles
    # ==============================

    def clear(self):

        self.particles.clear()


class ScreenShake:

    def __init__(self):

        self.timer = 0

        self.intensity = 0

    # =====================================
    # Start Shake
    # =====================================

    def start(self, intensity=8, duration=12):

        self.intensity = intensity

        self.timer = duration

    # =====================================
    # Update
    # =====================================

    def update(self):

        if self.timer > 0:
            self.timer -= 1

    # =====================================
    # Camera Offset
    # =====================================

    def offset(self):

        if self.timer <= 0:
            return (0, 0)

        return (

            random.randint(
                -self.intensity,
                self.intensity
            ),

            random.randint(
                -self.intensity,
                self.intensity
            )

        )

    # =====================================
    # Reset Shake
    # =====================================

    def reset(self):

        self.timer = 0

        self.intensity = 0