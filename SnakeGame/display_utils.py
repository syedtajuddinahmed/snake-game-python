import pygame

import settings
from settings import BLOCK_SIZE

# Smallest playable canvas size, so a tiny/weird window size never
# breaks the grid-based game logic.
MIN_WIDTH = BLOCK_SIZE * 12
MIN_HEIGHT = BLOCK_SIZE * 12


def present(canvas):
    """Blit the game canvas onto the real window and flip.

    The canvas is kept the same size as the window (see
    handle_resize_event), so normally this is a direct 1:1 blit with
    no scaling or letterboxing -- the game fills the whole window.
    The smoothscale fallback only kicks in for the rare frame where
    the two sizes haven't caught up with each other yet.
    """

    window = pygame.display.get_surface()

    if window is None:
        return

    win_size = window.get_size()
    canvas_size = canvas.get_size()

    window.fill((0, 0, 0))

    if canvas_size == win_size:
        window.blit(canvas, (0, 0))
    else:
        scaled = pygame.transform.smoothscale(canvas, win_size)
        window.blit(scaled, (0, 0))

    pygame.display.flip()


def get_mouse_pos():
    """Mouse position in game-canvas coordinates.

    Since the canvas is always resized to match the window, this is
    normally just the raw mouse position -- kept as a function (instead
    of calling pygame.mouse.get_pos() directly everywhere) so menus /
    buttons keep working correctly even during the rare mismatched
    frame described in present().
    """

    window = pygame.display.get_surface()

    if window is None:
        return pygame.mouse.get_pos()

    win_w, win_h = window.get_size()
    canvas_w, canvas_h = settings.WIDTH, settings.HEIGHT

    if win_w <= 0 or win_h <= 0 or (win_w, win_h) == (canvas_w, canvas_h):
        return pygame.mouse.get_pos()

    mx, my = pygame.mouse.get_pos()

    cx = mx * canvas_w / win_w
    cy = my * canvas_h / win_h

    return (int(cx), int(cy))


def handle_resize_event(event):
    """Call this on pygame.VIDEORESIZE events.

    Grows/shrinks the actual game canvas (settings.WIDTH / HEIGHT) to
    match the real window size -- e.g. maximizing the window now makes
    the game itself fill the screen, instead of scaling a fixed-size
    canvas inside black letterbox bars.

    Returns the new (width, height) the caller should build a fresh
    `screen = pygame.Surface((width, height))` canvas with.
    """

    new_w = max(MIN_WIDTH, event.w)
    new_h = max(MIN_HEIGHT, event.h)

    settings.WIDTH = new_w
    settings.HEIGHT = new_h

    pygame.display.set_mode(
        (event.w, event.h),
        pygame.RESIZABLE
    )

    return new_w, new_h
