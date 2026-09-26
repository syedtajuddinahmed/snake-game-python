import pygame

from settings import *
import settings
from menu import draw_button
from display_utils import present, get_mouse_pos, handle_resize_event


def choose_difficulty(screen):

    clock = pygame.time.Clock()

    selected = None

    # -----------------------------
    # Title (sized once, same pattern as the main menu)
    # -----------------------------

    title_y = 50

    button_width = 280
    button_height = 55
    button_gap = 22

    hint_font = pygame.font.SysFont("Arial", 18)
    hint = hint_font.render(
        "Click a difficulty, or press 1 / 2 / 3",
        True,
        (180, 180, 180),
    )

    while selected is None:

        clock.tick(60)

        # Recompute layout every frame so it stays centered even if
        # the window is resized (e.g. maximized) mid-screen.
        title_font_size = 46
        while True:
            title_font = pygame.font.SysFont("Arial", title_font_size, bold=True)
            title = title_font.render("SELECT DIFFICULTY", True, GREEN)
            if title.get_width() <= settings.WIDTH - 40 or title_font_size <= 24:
                break
            title_font_size -= 2

        title_gap = 45
        first_y = title_y + title.get_height() + title_gap

        center_x = settings.WIDTH // 2 - button_width // 2

        easy_button = pygame.Rect(
            center_x, first_y, button_width, button_height
        )

        medium_button = pygame.Rect(
            center_x,
            first_y + (button_height + button_gap),
            button_width,
            button_height,
        )

        hard_button = pygame.Rect(
            center_x,
            first_y + 2 * (button_height + button_gap),
            button_width,
            button_height,
        )

        # Gradient background, matching the main menu's style
        for y in range(settings.HEIGHT):
            color = (10, int(20 + (y / settings.HEIGHT) * 25), 10)
            pygame.draw.line(screen, color, (0, y), (settings.WIDTH, y))

        screen.blit(
            title,
            (settings.WIDTH // 2 - title.get_width() // 2, title_y),
        )

        draw_button(screen, "1. EASY", easy_button, GREEN)
        draw_button(screen, "2. MEDIUM", medium_button, YELLOW)
        draw_button(screen, "3. HARD", hard_button, RED)

        screen.blit(
            hint,
            (settings.WIDTH // 2 - hint.get_width() // 2, settings.HEIGHT - 36),
        )

        present(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.VIDEORESIZE:
                new_w, new_h = handle_resize_event(event)
                screen = pygame.Surface((new_w, new_h))

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    selected = EASY_SPEED

                elif event.key == pygame.K_2:
                    selected = MEDIUM_SPEED

                elif event.key == pygame.K_3:
                    selected = HARD_SPEED

            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouse = get_mouse_pos()

                if easy_button.collidepoint(mouse):
                    selected = EASY_SPEED

                elif medium_button.collidepoint(mouse):
                    selected = MEDIUM_SPEED

                elif hard_button.collidepoint(mouse):
                    selected = HARD_SPEED

    return selected