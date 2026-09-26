import pygame


class Achievement:

    def __init__(self):

        self.message = ""

        self.timer = 0

    # -----------------------------
    # Unlock Achievement
    # -----------------------------
    def unlock(self, text):

        self.message = text

        self.timer = 180      # 3 seconds at 60 FPS

    # -----------------------------
    # Update
    # -----------------------------
    def update(self):

        if self.timer > 0:
            self.timer -= 1

    # -----------------------------
    # Draw Popup
    # -----------------------------
    def draw(self, screen):

        if self.timer <= 0:
            return

        box = pygame.Surface((300,70), pygame.SRCALPHA)
        box.fill((30,30,30,220))

        screen.blit(box, (150,15))

        pygame.draw.rect(
            screen,
            (255,215,0),
            (150,15,300,70),
            2,
            border_radius=10
        )

        title_font = pygame.font.SysFont("Arial",24,True)
        text_font = pygame.font.SysFont("Arial",18)

        title = title_font.render(
            "Achievement Unlocked!",
            True,
            (255,215,0)
        )

        text = text_font.render(
            self.message,
            True,
            (255,255,255)
        )

        screen.blit(title,(165,23))
        screen.blit(text,(165,50))