import pygame


class FloatingText:

    def __init__(self, x, y, text, color):

        self.x = x
        self.y = y

        self.text = text
        self.color = color

        self.life = 60

        self.font = pygame.font.SysFont(
            "Arial",
            24,
            bold=True
        )

    def update(self):

        self.y -= 1
        self.life -= 1

    def draw(self, screen):

        alpha = max(0, min(255, self.life * 4))

        surface = self.font.render(
            self.text,
            True,
            self.color
        )

        surface.set_alpha(alpha)

        screen.blit(
            surface,
            (self.x, self.y)
        )


class FloatingTextManager:

    def __init__(self):

        self.texts = []

    # ==============================
    # Add Floating Text
    # ==============================

    def add(self, x, y, text, color):

        self.texts.append(
            FloatingText(
                x,
                y,
                text,
                color
            )
        )

    # ==============================
    # Update
    # ==============================

    def update(self):

        for text in self.texts[:]:

            text.update()

            if text.life <= 0:

                self.texts.remove(text)

    # ==============================
    # Draw
    # ==============================

    def draw(self, screen):

        for text in self.texts:

            text.draw(screen)

    # ==============================
    # Clear All Text
    # ==============================

    def clear(self):

        self.texts.clear()