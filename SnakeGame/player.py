import pygame
from settings import *
import settings
from display_utils import present, get_mouse_pos, handle_resize_event
from menu import draw_button


def get_player_name(screen):

    name = ""

    waiting = True

    clock = pygame.time.Clock()

    cursor_timer = 0
    cursor_visible = True

    max_len = 12

    while waiting:

        clock.tick(60)

        # -----------------------------
        # Gradient background (same style as the other menu screens)
        # -----------------------------

        for y in range(settings.HEIGHT):
            color = (
                10,
                int(20 + (y / settings.HEIGHT) * 25),
                10,
            )
            pygame.draw.line(screen, color, (0, y), (settings.WIDTH, y))

        center_x = settings.WIDTH // 2
        center_y = settings.HEIGHT // 2

        # -----------------------------
        # Title with a soft glow (auto-shrinks on very narrow windows)
        # -----------------------------

        title_font_size = 54
        while True:
            title_font = pygame.font.SysFont("Arial", title_font_size, bold=True)
            title = title_font.render("ENTER YOUR NAME", True, GREEN)
            if title.get_width() <= settings.WIDTH - 40 or title_font_size <= 26:
                break
            title_font_size -= 2

        title_y = center_y - 140

        for offset in range(8, 0, -2):
            glow = title_font.render("ENTER YOUR NAME", True, (0, 120, 0))
            glow.set_alpha(40)
            screen.blit(
                glow,
                (center_x - glow.get_width() // 2, title_y + offset),
            )

        screen.blit(
            title,
            (center_x - title.get_width() // 2, title_y),
        )

        # -----------------------------
        # Name input box
        # -----------------------------

        box_width = 420
        box_height = 64

        box_rect = pygame.Rect(
            center_x - box_width // 2,
            center_y - box_height // 2,
            box_width,
            box_height,
        )

        box_color = (25, 25, 25)
        border_color = (0, 220, 0) if name else (90, 90, 90)

        pygame.draw.rect(screen, box_color, box_rect, border_radius=14)
        pygame.draw.rect(screen, border_color, box_rect, 3, border_radius=14)

        name_font = pygame.font.SysFont("Arial", 36, bold=True)
        name_text = name_font.render(name, True, WHITE)

        # Blinking cursor
        cursor_timer += clock.get_time()
        if cursor_timer >= 500:
            cursor_timer = 0
            cursor_visible = not cursor_visible

        text_x = box_rect.centerx - name_text.get_width() // 2
        text_y = box_rect.centery - name_text.get_height() // 2

        screen.blit(name_text, (text_x, text_y))

        if cursor_visible:
            cursor_x = text_x + name_text.get_width() + 4
            pygame.draw.line(
                screen,
                GREEN,
                (cursor_x, box_rect.centery - 18),
                (cursor_x, box_rect.centery + 18),
                3,
            )

        # Placeholder hint when empty
        if not name:
            hint_font = pygame.font.SysFont("Arial", 26)
            placeholder = hint_font.render("Type your name...", True, (110, 110, 110))
            screen.blit(
                placeholder,
                (
                    box_rect.centerx - placeholder.get_width() // 2,
                    box_rect.centery - placeholder.get_height() // 2,
                ),
            )

        # Character count
        count_font = pygame.font.SysFont("Arial", 18)
        count_text = count_font.render(
            f"{len(name)}/{max_len}", True, (150, 150, 150)
        )
        screen.blit(
            count_text,
            (box_rect.right - count_text.get_width(), box_rect.bottom + 8),
        )

        # -----------------------------
        # "Press ENTER" hint, gently pulsing
        # -----------------------------

        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500  # 0 -> 1 -> 0
        hint_alpha = 140 + int(pulse * 115)

        active = bool(name)
        hint_color = YELLOW if active else (110, 90, 0)

        info_font = pygame.font.SysFont("Arial", 28, bold=True)
        info_text = "Press ENTER to Continue" if active else "Enter a name to continue"
        info = info_font.render(info_text, True, hint_color)
        info.set_alpha(hint_alpha if active else 200)

        screen.blit(
            info,
            (center_x - info.get_width() // 2, box_rect.bottom + 50),
        )

        # -----------------------------
        # Back button
        # -----------------------------

        back_button = pygame.Rect(0, 0, 160, 44)
        back_button.centerx = center_x
        back_button.y = box_rect.bottom + 100

        draw_button(screen, "BACK", back_button, (150, 130, 0))

        present(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.VIDEORESIZE:
                new_w, new_h = handle_resize_event(event)
                screen = pygame.Surface((new_w, new_h))

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    if name != "":
                        waiting = False

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif event.key == pygame.K_ESCAPE:
                    return None

                else:
                    if len(name) < max_len and event.unicode.strip() != "":
                        name += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if back_button.collidepoint(get_mouse_pos()):
                    return None

    return name
