import pygame
import sys

from settings import *
import settings
from settings_menu import settings_menu
from display_utils import present, get_mouse_pos, handle_resize_event


# ===========================
# DRAW BUTTON
# ===========================
def draw_button(screen, text, rect, color):
    mouse = get_mouse_pos()

    button_color = color

    if rect.collidepoint(mouse):
        button_color = (
            min(color[0] + 40, 255),
            min(color[1] + 40, 255),
            min(color[2] + 40, 255),
        )

    pygame.draw.rect(screen, button_color, rect, border_radius=12)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=12)

    font_size = 32

    while True:
        font = pygame.font.SysFont("Arial", font_size, bold=True)
        text_img = font.render(text, True, WHITE)

        if text_img.get_width() <= rect.width - 20 or font_size <= 20:
            break

        font_size -= 1

    screen.blit(
        text_img,
        (
            rect.centerx - text_img.get_width() // 2,
            rect.centery - text_img.get_height() // 2,
        ),
    )


# ===========================
# MAIN MENU
# ===========================
def start_menu(screen, leaderboard):
    clock = pygame.time.Clock()

    button_width = 300
    button_height = 50
    button_gap = 16

    # -----------------------------
    # Title (re-measured every frame so it re-centers on resize)
    # -----------------------------
    title_y = 30

    while True:
        clock.tick(60)

        # Recompute layout every frame so buttons/title stay centered
        # even if the window was resized (e.g. maximized) mid-menu.
        center_x = settings.WIDTH // 2 - button_width // 2

        title_font_size = 64
        while True:
            title_font = pygame.font.SysFont("Arial", title_font_size, bold=True)
            title = title_font.render("SNAKE GAME", True, GREEN)
            if title.get_width() <= settings.WIDTH - 40 or title_font_size <= 30:
                break
            title_font_size -= 2

        title_gap = 35
        first_y = title_y + title.get_height() + title_gap

        start_button = pygame.Rect(
            center_x, first_y, button_width, button_height
        )

        instruction_button = pygame.Rect(
            center_x,
            first_y + (button_height + button_gap),
            button_width,
            button_height,
        )

        settings_button = pygame.Rect(
            center_x,
            first_y + 2 * (button_height + button_gap),
            button_width,
            button_height,
        )

        leaderboard_button = pygame.Rect(
            center_x,
            first_y + 3 * (button_height + button_gap),
            button_width,
            button_height,
        )

        exit_button = pygame.Rect(
            center_x,
            first_y + 4 * (button_height + button_gap),
            button_width,
            button_height,
        )

        # Gradient Background
        for y in range(settings.HEIGHT):
            color = (
                10,
                int(40 + (y / settings.HEIGHT) * 40),
                10,
            )
            pygame.draw.line(screen, color, (0, y), (settings.WIDTH, y))

        # Title (font/surface already built above the loop)
        for offset in range(8, 0, -2):
            glow = title_font.render(
                "SNAKE GAME",
                True,
                (0, 120, 0),
            )
            glow.set_alpha(40)

            screen.blit(
                glow,
                (
                    settings.WIDTH // 2 - glow.get_width() // 2,
                    title_y + offset,
                ),
            )

        screen.blit(
            title,
            (
                settings.WIDTH // 2 - title.get_width() // 2,
                title_y,
            ),
        )

        # Buttons
        draw_button(screen, "START", start_button, GREEN)
        draw_button(screen, "INSTRUCTIONS", instruction_button, BLUE)
        draw_button(screen, "SETTINGS", settings_button, (150, 100, 255))
        draw_button(screen, "LEADERBOARD", leaderboard_button, YELLOW)
        draw_button(screen, "EXIT", exit_button, RED)

        # Version
        small_font = pygame.font.SysFont("Arial", 18)

        version = small_font.render(
            "Snake Game • Version 2.0",
            True,
            (180, 180, 180),
        )

        screen.blit(
            version,
            (
                settings.WIDTH // 2 - version.get_width() // 2,
                settings.HEIGHT - 28,
            ),
        )

        present(screen)

        # Events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                new_w, new_h = handle_resize_event(event)
                screen = pygame.Surface((new_w, new_h))

            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouse = get_mouse_pos()

                if start_button.collidepoint(mouse):
                 return

                elif instruction_button.collidepoint(mouse):
                   show_instructions(screen)

                elif settings_button.collidepoint(mouse):
                     settings_menu(screen)

                elif leaderboard_button.collidepoint(mouse):
                      show_leaderboard(screen, leaderboard)

                elif exit_button.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()             
# ===========================
# INSTRUCTIONS
# ===========================
def show_instructions(screen):
    clock = pygame.time.Clock()

    # (icon, text, accent color)
    lines = [
        ("\U0001f579", "Arrow Keys : Move", (120, 200, 255)),
        ("\u23f8", "P : Pause Game", (200, 160, 255)),
        ("\U0001f34e", "Eat Food to Grow", (120, 230, 120)),
        ("\U0001f9f1", "Avoid Walls", (255, 180, 80)),
        ("\U0001faa8", "Avoid Obstacles", (255, 120, 120)),
        ("\u238b", "ESC : Back to Menu", (200, 200, 200)),
    ]

    while True:
        clock.tick(60)

        # Gradient background, matching the other menu screens
        for y in range(settings.HEIGHT):
            color = (10, int(20 + (y / settings.HEIGHT) * 25), 10)
            pygame.draw.line(screen, color, (0, y), (settings.WIDTH, y))

        center_x = settings.WIDTH // 2

        # -----------------------------
        # Title with glow
        # -----------------------------

        title_font = pygame.font.SysFont("Arial", 50, bold=True)
        title = title_font.render("INSTRUCTIONS", True, GREEN)

        title_y = 45

        for offset in range(8, 0, -2):
            glow = title_font.render("INSTRUCTIONS", True, (0, 120, 0))
            glow.set_alpha(40)
            screen.blit(glow, (center_x - glow.get_width() // 2, title_y + offset))

        screen.blit(title, (center_x - title.get_width() // 2, title_y))

        # -----------------------------
        # Instruction cards
        # -----------------------------

        card_width = min(520, settings.WIDTH - 80)
        card_height = 56
        card_gap = 14
        card_x = center_x - card_width // 2

        list_top = title_y + title.get_height() + 35

        icon_font = pygame.font.SysFont("Segoe UI Emoji", 26)
        text_font = pygame.font.SysFont("Arial", 26, bold=True)

        for i, (icon, line, accent) in enumerate(lines):

            card_y = list_top + i * (card_height + card_gap)
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)

            pygame.draw.rect(screen, (18, 18, 18), card_rect, border_radius=12)
            pygame.draw.rect(screen, accent, card_rect, 2, border_radius=12)

            # Small accent bar on the left edge
            accent_bar = pygame.Rect(card_rect.x, card_rect.y, 6, card_rect.height)
            pygame.draw.rect(screen, accent, accent_bar)

            icon_img = icon_font.render(icon, True, accent)
            screen.blit(
                icon_img,
                (card_rect.x + 26, card_rect.centery - icon_img.get_height() // 2),
            )

            txt = text_font.render(line, True, WHITE)
            screen.blit(
                txt,
                (card_rect.x + 80, card_rect.centery - txt.get_height() // 2),
            )

        # -----------------------------
        # Back button
        # -----------------------------

        back_button = pygame.Rect(0, 0, 160, 44)
        back_button.centerx = center_x
        back_button.y = list_top + len(lines) * (card_height + card_gap) + 10

        draw_button(screen, "BACK", back_button, (150, 130, 0))

        present(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                new_w, new_h = handle_resize_event(event)
                screen = pygame.Surface((new_w, new_h))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(get_mouse_pos()):
                    return


# ===========================
# LEADERBOARD
# ===========================
def show_leaderboard(screen, leaderboard):
    clock = pygame.time.Clock()

    medal_colors = {
        0: (255, 215, 0),    # Gold
        1: (200, 200, 210),  # Silver
        2: (205, 127, 50),   # Bronze
    }

    while True:
        clock.tick(60)

        # Gradient background, matching the other menu screens
        for y in range(settings.HEIGHT):
            color = (10, int(20 + (y / settings.HEIGHT) * 25), 10)
            pygame.draw.line(screen, color, (0, y), (settings.WIDTH, y))

        center_x = settings.WIDTH // 2

        # -----------------------------
        # Title with glow + trophy
        # -----------------------------

        title_font = pygame.font.SysFont("Arial", 50, bold=True)
        title = title_font.render("LEADERBOARD", True, GREEN)

        title_y = 45

        for offset in range(8, 0, -2):
            glow = title_font.render("LEADERBOARD", True, (0, 120, 0))
            glow.set_alpha(40)
            screen.blit(glow, (center_x - glow.get_width() // 2, title_y + offset))

        screen.blit(title, (center_x - title.get_width() // 2, title_y))

        emoji_font = pygame.font.SysFont("Segoe UI Emoji", 40)
        trophy = emoji_font.render("🏆", True, (255, 215, 0))
        screen.blit(
            trophy,
            (center_x - title.get_width() // 2 - trophy.get_width() - 12, title_y - 5),
        )
        screen.blit(
            trophy,
            (center_x + title.get_width() // 2 + 12, title_y - 5),
        )

        # -----------------------------
        # Score rows / cards
        # -----------------------------

        font = pygame.font.SysFont("Arial", 28, bold=True)

        scores = leaderboard.get_scores()

        list_top = title_y + title.get_height() + 40

        if not scores:

            txt = font.render("No Scores Yet", True, WHITE)

            screen.blit(
                txt,
                (center_x - txt.get_width() // 2, list_top + 30),
            )

        else:

            card_width = min(560, settings.WIDTH - 80)
            card_height = 48
            card_gap = 12
            card_x = center_x - card_width // 2

            for i, (name, score) in enumerate(scores[:10]):

                card_y = list_top + i * (card_height + card_gap)

                accent = medal_colors.get(i, (60, 90, 60))

                card_rect = pygame.Rect(card_x, card_y, card_width, card_height)

                pygame.draw.rect(screen, (20, 20, 20), card_rect, border_radius=10)
                pygame.draw.rect(screen, accent, card_rect, 2, border_radius=10)

                # Rank badge
                rank_font = pygame.font.SysFont("Arial", 22, bold=True)
                rank_text = rank_font.render(f"#{i+1}", True, accent)
                screen.blit(
                    rank_text,
                    (card_rect.x + 18, card_rect.centery - rank_text.get_height() // 2),
                )

                # Name
                name_color = accent if i < 3 else WHITE
                name_text = font.render(name, True, name_color)
                screen.blit(
                    name_text,
                    (card_rect.x + 80, card_rect.centery - name_text.get_height() // 2),
                )

                # Score
                score_text = font.render(str(score), True, YELLOW)
                screen.blit(
                    score_text,
                    (
                        card_rect.right - score_text.get_width() - 18,
                        card_rect.centery - score_text.get_height() // 2,
                    ),
                )

        # -----------------------------
        # Back button
        # -----------------------------

        back_button = pygame.Rect(0, 0, 160, 44)
        back_button.centerx = center_x
        back_button.bottom = settings.HEIGHT - 16

        draw_button(screen, "BACK", back_button, (150, 130, 0))

        present(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                new_w, new_h = handle_resize_event(event)
                screen = pygame.Surface((new_w, new_h))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(get_mouse_pos()):
                    return