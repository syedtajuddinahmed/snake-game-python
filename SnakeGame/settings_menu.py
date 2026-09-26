import pygame
from settings import *
import settings
from display_utils import present, get_mouse_pos, handle_resize_event

# ----------------------------
# Settings Variables
# ----------------------------

music_on = True
sound_on = True

music_volume = 0.5
sound_volume = 0.5


# ----------------------------
# Small helpers
# ----------------------------

def _hover_color(color, rect):
    mouse = get_mouse_pos()
    if rect.collidepoint(mouse):
        return tuple(min(c + 35, 255) for c in color)
    return color


def draw_toggle_card(screen, icon_on, icon_off, label, is_on, rect):
    """A big ON/OFF card with an icon, e.g. Music / Sound."""

    color = (0, 140, 70) if is_on else (110, 30, 30)
    color = _hover_color(color, rect)

    pygame.draw.rect(screen, color, rect, border_radius=14)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=14)

    icon_font = pygame.font.SysFont("Segoe UI Emoji", 26)
    icon_img = icon_font.render(icon_on if is_on else icon_off, True, WHITE)

    text_font = pygame.font.SysFont("Arial", 24, bold=True)
    text_img = text_font.render(
        f"{label} : {'ON' if is_on else 'OFF'}", True, WHITE
    )

    total_w = icon_img.get_width() + 12 + text_img.get_width()
    x = rect.centerx - total_w // 2

    screen.blit(icon_img, (x, rect.centery - icon_img.get_height() // 2))
    screen.blit(
        text_img,
        (x + icon_img.get_width() + 12, rect.centery - text_img.get_height() // 2),
    )


def draw_round_button(screen, text, rect, color):
    color = _hover_color(color, rect)

    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)

    font = pygame.font.SysFont("Arial", 24, bold=True)
    text_img = font.render(text, True, WHITE)

    screen.blit(
        text_img,
        (
            rect.centerx - text_img.get_width() // 2,
            rect.centery - text_img.get_height() // 2,
        ),
    )


def draw_volume_bar(screen, label, value, bar_rect, accent):
    """Label above a filled progress-bar track."""

    label_font = pygame.font.SysFont("Arial", 19, bold=True)
    label_img = label_font.render(
        f"{label} : {int(value * 100)}%", True, (210, 210, 210)
    )
    screen.blit(
        label_img,
        (bar_rect.centerx - label_img.get_width() // 2, bar_rect.y - 26),
    )

    pygame.draw.rect(screen, (35, 35, 35), bar_rect, border_radius=8)

    fill_width = int(bar_rect.width * value)
    if fill_width > 0:
        fill_rect = pygame.Rect(
            bar_rect.x, bar_rect.y, fill_width, bar_rect.height
        )
        pygame.draw.rect(screen, accent, fill_rect, border_radius=8)

    pygame.draw.rect(screen, (90, 90, 90), bar_rect, 2, border_radius=8)


# ----------------------------
# Settings Menu
# ----------------------------

def settings_menu(screen):

    global music_on
    global sound_on
    global music_volume
    global sound_volume

    clock = pygame.time.Clock()

    running = True

    while running:

        clock.tick(60)

        # -----------------------------
        # Gradient background, matching the other menu screens
        # -----------------------------

        for y in range(settings.HEIGHT):
            color = (10, int(20 + (y / settings.HEIGHT) * 25), 10)
            pygame.draw.line(screen, color, (0, y), (settings.WIDTH, y))

        center_x = settings.WIDTH // 2

        # -----------------------------
        # Title with glow
        # -----------------------------

        title_font = pygame.font.SysFont("Arial", 52, bold=True)
        title = title_font.render("SETTINGS", True, GREEN)

        title_y = 45

        for offset in range(8, 0, -2):
            glow = title_font.render("SETTINGS", True, (0, 120, 0))
            glow.set_alpha(40)
            screen.blit(glow, (center_x - glow.get_width() // 2, title_y + offset))

        screen.blit(title, (center_x - title.get_width() // 2, title_y))

        # -----------------------------
        # Layout (recomputed every frame so it stays centered even
        # if the window is resized/maximized while this menu is open)
        # -----------------------------

        toggle_width = 340
        toggle_height = 56

        panel_top = title_y + title.get_height() + 45

        music_button = pygame.Rect(
            center_x - toggle_width // 2, panel_top, toggle_width, toggle_height
        )

        sound_button = pygame.Rect(
            center_x - toggle_width // 2,
            panel_top + toggle_height + 18,
            toggle_width,
            toggle_height,
        )

        bar_width = 260
        button_size = 38
        gap = 16

        row_width = button_size + gap + bar_width + gap + button_size
        row_x = center_x - row_width // 2

        music_vol_y = sound_button.bottom + 55

        music_minus = pygame.Rect(row_x, music_vol_y - 3, button_size, button_size + 4)
        music_bar = pygame.Rect(
            music_minus.right + gap, music_vol_y, bar_width, button_size - 4
        )
        music_plus = pygame.Rect(music_bar.right + gap, music_vol_y - 3, button_size, button_size + 4)

        sound_vol_y = music_vol_y + 90

        sound_minus = pygame.Rect(row_x, sound_vol_y - 3, button_size, button_size + 4)
        sound_bar = pygame.Rect(
            sound_minus.right + gap, sound_vol_y, bar_width, button_size - 4
        )
        sound_plus = pygame.Rect(sound_bar.right + gap, sound_vol_y - 3, button_size, button_size + 4)

        back_button = pygame.Rect(
            center_x - toggle_width // 2,
            sound_vol_y + 75,
            toggle_width,
            toggle_height,
        )

        # -----------------------------
        # Draw everything
        # -----------------------------

        draw_toggle_card(screen, "\U0001f3b5", "\U0001f507", "Music", music_on, music_button)
        draw_toggle_card(screen, "\U0001f50a", "\U0001f507", "Sound", sound_on, sound_button)

        draw_volume_bar(screen, "Music Volume", music_volume, music_bar, (100, 200, 255))
        draw_round_button(screen, "-", music_minus, RED)
        draw_round_button(screen, "+", music_plus, GREEN)

        draw_volume_bar(screen, "Sound Volume", sound_volume, sound_bar, (255, 180, 90))
        draw_round_button(screen, "-", sound_minus, RED)
        draw_round_button(screen, "+", sound_plus, GREEN)

        draw_round_button(screen, "BACK", back_button, (150, 130, 0))

        present(screen)

        # Events

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                exit()

            if event.type == pygame.VIDEORESIZE:

                new_w, new_h = handle_resize_event(event)
                screen = pygame.Surface((new_w, new_h))

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse = get_mouse_pos()

                # Music ON/OFF

                if music_button.collidepoint(mouse):

                    music_on = not music_on

                    if music_on:

                        pygame.mixer.music.unpause()

                    else:

                        pygame.mixer.music.pause()

                # Sound ON/OFF

                elif sound_button.collidepoint(mouse):

                    sound_on = not sound_on

                # Music +

                elif music_plus.collidepoint(mouse):

                    music_volume = min(
                        1.0,
                        music_volume + 0.1
                    )

                    pygame.mixer.music.set_volume(
                        music_volume
                    )

                # Music -

                elif music_minus.collidepoint(mouse):

                    music_volume = max(
                        0.0,
                        music_volume - 0.1
                    )

                    pygame.mixer.music.set_volume(
                        music_volume
                    )

                # Sound +

                elif sound_plus.collidepoint(mouse):

                    sound_volume = min(
                        1.0,
                        sound_volume + 0.1
                    )

                # Sound -

                elif sound_minus.collidepoint(mouse):

                    sound_volume = max(
                        0.0,
                        sound_volume - 0.1
                    )

                # Back

                elif back_button.collidepoint(mouse):

                    running = False
