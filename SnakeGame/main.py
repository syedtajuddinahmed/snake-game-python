import pygame
import sys

# ==========================
# Import Game Files
# ==========================

from settings import *
import settings

from snake import Snake
from food import Food
from bonus_food import BonusFood
from golden_food import GoldenFood

from obstacle import Obstacle

from score import Score
from level import Level

from leaderboard import Leaderboard

from menu import start_menu
from player import get_player_name
from difficulty import choose_difficulty

# Effects
from background import Background
from particles import ParticleSystem, ScreenShake
from floating_text import FloatingTextManager
from achievement import Achievement

from display_utils import present, handle_resize_event

# ==========================
# Initialize Pygame
# ==========================

pygame.init()
pygame.mixer.init()

# ==========================
# Sounds
# ==========================

eat_sound = pygame.mixer.Sound("sounds/eat.mp3")
bonus_sound = pygame.mixer.Sound("sounds/bonus.mp3")
gameover_sound = pygame.mixer.Sound("sounds/gameover.mp3")

eat_sound.set_volume(0.5)
bonus_sound.set_volume(0.6)
gameover_sound.set_volume(0.6)

# ==========================
# Background Music
# ==========================

pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(-1)

# ==========================
# Create Window
# ==========================
# The real OS window is resizable so the title-bar maximize button
# works (click to maximize, click again to restore). All game code
# still draws onto a fixed-size "screen" canvas at (settings.WIDTH, settings.HEIGHT);
# that canvas is scaled to fit the real window every frame by
# display_utils.present().

window = pygame.display.set_mode(
    (settings.WIDTH, settings.HEIGHT),
    pygame.RESIZABLE
)

screen = pygame.Surface((settings.WIDTH, settings.HEIGHT))

pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

# ==========================
# Visual Effects
# ==========================

background = Background()

particles = ParticleSystem()

floating_text = FloatingTextManager()

shake = ScreenShake()

achievement = Achievement()

# ==========================
# Leaderboard
# ==========================

leaderboard = Leaderboard()

# ==========================
# Menus
# ==========================

start_menu(screen, leaderboard)

# Pick up any resize (e.g. maximize) that happened during that screen
screen = pygame.Surface((settings.WIDTH, settings.HEIGHT))

selected_speed = choose_difficulty(screen)

screen = pygame.Surface((settings.WIDTH, settings.HEIGHT))

player_name = get_player_name(screen)

# If the player clicked BACK (or pressed ESC) on the name screen,
# return to difficulty selection and try again.
while player_name is None:

    screen = pygame.Surface((settings.WIDTH, settings.HEIGHT))
    selected_speed = choose_difficulty(screen)

    screen = pygame.Surface((settings.WIDTH, settings.HEIGHT))
    player_name = get_player_name(screen)

screen = pygame.Surface((settings.WIDTH, settings.HEIGHT))

# ======================================
# Restart Game
# ======================================

def restart_game():

    global snake
    global food
    global bonus_food
    global golden_food
    global obstacle
    global score
    global level
    global speed

    # Snake
    snake = Snake()

    # Foods
    food = Food()

    bonus_food = BonusFood()

    golden_food = GoldenFood()

    # Score
    score = Score()

    # Level
    level = Level()

    # Obstacles
    obstacle = Obstacle()

    obstacle.generate(level.level)

    # Game Speed
    speed = selected_speed

    # Clear Effects
    particles.clear()

    floating_text.clear()

    shake.reset()

    # Re-scatter background stars across the current canvas size
    background.resize()


# ======================================
# Start First Game
# ======================================

restart_game()


# ======================================
# Game Variables
# ======================================

running = True

paused = False

game_over = False


# ======================================
# Timer
# ======================================

start_ticks = pygame.time.get_ticks()

# ======================================
# MAIN GAME LOOP
# ======================================

while True:

    while running:

        clock.tick(speed)

        # -----------------------------
        # EVENTS
        # -----------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                new_w, new_h = handle_resize_event(event)
                screen = pygame.Surface((new_w, new_h))
                background.resize()

            elif event.type == pygame.KEYDOWN:

                # Pause
                if event.key == pygame.K_p:
                    paused = not paused

                # Movement
                elif event.key == pygame.K_UP:
                    snake.change_direction("UP")

                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")

                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")

                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")

        # -----------------------------
        # Pause
        # -----------------------------

        if paused:

            screen.fill((0, 0, 0))

            background.draw(screen)

            snake.draw(screen)

            food.draw(screen)

            bonus_food.draw(screen)

            if golden_food.active:
                golden_food.draw(screen)

            obstacle.draw(screen)

            score.draw(screen, level)

            font = pygame.font.SysFont("Arial", 50, True)

            text = font.render("PAUSED", True, WHITE)

            screen.blit(
                text,
                (
                    settings.WIDTH // 2 - text.get_width() // 2,
                    settings.HEIGHT // 2 - text.get_height() // 2
                )
            )

            present(screen)

            continue

        # -----------------------------
        # Update Snake
        # -----------------------------

        snake.move()

        # -----------------------------
        # Normal Food
        # -----------------------------

        if snake.head() == food.position:

            snake.grow()

            eat_sound.play()

            score.add()

            floating_text.add(
                food.position[0],
                food.position[1],
                "+10",
                GREEN
            )

            particles.create(
                food.position[0] + BLOCK_SIZE // 2,
                food.position[1] + BLOCK_SIZE // 2,
                GREEN,
                25
            )

            shake.start()

            food.new_food()

        # -----------------------------
        # Bonus Food
        # -----------------------------

        if snake.head() == bonus_food.position:

            snake.grow()

            score.add(50)

            bonus_sound.play()

            floating_text.add(
                bonus_food.position[0],
                bonus_food.position[1],
                "+50",
                YELLOW
            )

            particles.create(
                bonus_food.position[0] + BLOCK_SIZE // 2,
                bonus_food.position[1] + BLOCK_SIZE // 2,
                YELLOW,
                40
            )

            shake.start(10, 12)

            bonus_food.new_food()

        # -----------------------------
        # Spawn Golden Food
        # -----------------------------

        if (
            score.score > 0
            and score.score % 200 == 0
            and not golden_food.active
        ):

            golden_food.new_food()

        # -----------------------------
        # Golden Food
        # -----------------------------

        if (
            golden_food.active
            and snake.head() == golden_food.position
        ):

            snake.grow()

            score.add(100)

            bonus_sound.play()

            floating_text.add(
                golden_food.position[0],
                golden_food.position[1],
                "+100",
                (255, 215, 0)
            )

            particles.create(
                golden_food.position[0] + BLOCK_SIZE // 2,
                golden_food.position[1] + BLOCK_SIZE // 2,
                (255, 215, 0),
                50
            )

            shake.start(12, 15)

            golden_food.hide()

            achievement.unlock("Golden Hunter!")

        # -----------------------------
        # Update Level
        # -----------------------------

        level.update(score.score)

        speed = level.get_speed()

        # -----------------------------
        # Collision
        # -----------------------------

        if (
            snake.wall_collision()
            or snake.self_collision()
            or snake.hud_collision()
            or obstacle.collision(snake.head())
        ):

            pygame.mixer.music.pause()

            gameover_sound.play()

            score.save()

            leaderboard.add_score(
                player_name,
                score.score
            )

            game_over = True

            running = False

        # -----------------------------
        # Update Effects
        # -----------------------------

        particles.update()

        floating_text.update()

        achievement.update()

        shake.update()

            # ======================================
        # DRAW BACKGROUND
        # ======================================

        screen.fill((0, 0, 0))

        background.draw(screen)

        # ======================================
        # DRAW GRID
        # ======================================

        for x in range(0, settings.WIDTH, BLOCK_SIZE):

            pygame.draw.line(
                screen,
                (40, 40, 40),
                (x, 0),
                (x, settings.HEIGHT)
            )

        for y in range(0, settings.HEIGHT, BLOCK_SIZE):

            pygame.draw.line(
                screen,
                (40, 40, 40),
                (0, y),
                (settings.WIDTH, y)
            )

        # ======================================
        # DRAW OBJECTS
        # ======================================

        obstacle.draw(screen)

        food.draw(screen)

        bonus_food.draw(screen)

        if golden_food.active:
            golden_food.draw(screen)

        snake.draw(screen)

        particles.draw(screen)

        floating_text.draw(screen)

        # ======================================
        # DRAW HUD
        # ======================================

        score.draw(screen, level)

        level.draw(screen)

        achievement.draw(screen)

        # ======================================
        # TIMER
        # ======================================

        font = pygame.font.SysFont(
            "Arial",
            18,
            bold=True
        )

        seconds = (
            pygame.time.get_ticks() - start_ticks
        ) // 1000

        timer = font.render(
            f"Time : {seconds}s",
            True,
            WHITE
        )

        screen.blit(
            timer,
            (
                settings.WIDTH - 120,
                10
            )
        )

        # ======================================
        # FPS
        # ======================================

        fps = font.render(
            f"FPS : {int(clock.get_fps())}",
            True,
            WHITE
        )

        screen.blit(
            fps,
            (
                settings.WIDTH - 120,
                35
            )
        )

        # ======================================
        # UPDATE SCREEN
        # ======================================

        present(screen)

        # ======================================
    # GAME OVER SCREEN
    # ======================================


    if not game_over:
        break

    while game_over:

        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                new_w, new_h = handle_resize_event(event)
                screen = pygame.Surface((new_w, new_h))
                background.resize()

            elif event.type == pygame.KEYDOWN:

                # Restart
                if event.key == pygame.K_r:

                    restart_game()

                    start_ticks = pygame.time.get_ticks()

                    pygame.mixer.music.unpause()

                    running = True

                    game_over = False

                # Exit
                elif event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

        # -----------------------------
        # Background
        # -----------------------------

        screen.fill((0, 0, 0))

        background.draw(screen)

        overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT))
        overlay.set_alpha(190)
        overlay.fill((0, 0, 0))

        screen.blit(overlay, (0, 0))

        # -----------------------------
        # Box (with a soft pulsing glow behind it)
        # -----------------------------

        BOX_WIDTH = 460
        BOX_HEIGHT = 385

        BOX_X = settings.WIDTH // 2 - BOX_WIDTH // 2
        BOX_Y = settings.HEIGHT // 2 - BOX_HEIGHT // 2

        pulse = abs(pygame.time.get_ticks() % 1600 - 800) / 800  # 0 -> 1 -> 0

        for i, pad in enumerate((18, 12, 6)):
            glow_surface = pygame.Surface(
                (BOX_WIDTH + pad * 2, BOX_HEIGHT + pad * 2),
                pygame.SRCALPHA,
            )
            glow_alpha = int((10 + pulse * 12) * (3 - i))
            pygame.draw.rect(
                glow_surface,
                (255, 215, 0, glow_alpha),
                glow_surface.get_rect(),
                border_radius=24,
            )
            screen.blit(glow_surface, (BOX_X - pad, BOX_Y - pad))

        pygame.draw.rect(
            screen,
            (30,30,34),
            (BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT),
            border_radius=20
        )

        border_glow = int(200 + pulse * 55)
        pygame.draw.rect(
            screen,
            (border_glow, 215, 0),
            (BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT),
            3,
            border_radius=20
        )

        # Thin accent line under the header area
        pygame.draw.line(
            screen,
            (70, 70, 74),
            (BOX_X + 30, BOX_Y + 100),
            (BOX_X + BOX_WIDTH - 30, BOX_Y + 100),
            1,
        )

        # -----------------------------
        # Fonts
        # -----------------------------

        title_font = pygame.font.SysFont(
            "Arial",
            42,
            True
        )

        label_font = pygame.font.SysFont(
            "Arial",
            21
        )

        value_font = pygame.font.SysFont(
            "Arial",
            21,
            True
        )

        small_font = pygame.font.SysFont(
            "Arial",
            22,
            True
        )

        # -----------------------------
        # Title
        # -----------------------------

        emoji_font = pygame.font.SysFont(
            "Segoe UI Emoji",
            38
        )

        trophy = emoji_font.render(
            "🏆",
            True,
            (255,215,0)
        )

        screen.blit(
            trophy,
            (
                settings.WIDTH//2 - trophy.get_width()//2,
                BOX_Y + 7
            )
        )

        title = title_font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            title,
            (
                settings.WIDTH // 2 - title.get_width() // 2,
                BOX_Y + 53
            )
        )

        # -----------------------------
        # Information (label / value pairs, color-coded)
        # -----------------------------

        is_new_high = score.score > 0 and score.score >= score.high_score

        info = [
            ("Player", player_name, WHITE),
            ("Score", str(score.score), (120, 230, 120)),
            ("High Score", str(score.high_score), (255, 215, 0)),
            ("Level", str(level.level), (120, 200, 255)),
        ]

        y = BOX_Y + 118

        for label_str, value_str, value_color in info:

            label = label_font.render(f"{label_str} :", True, (170, 170, 170))
            value = value_font.render(value_str, True, value_color)

            total_width = label.get_width() + 8 + value.get_width()
            x = settings.WIDTH // 2 - total_width // 2

            screen.blit(label, (x, y))
            screen.blit(value, (x + label.get_width() + 8, y))

            y += 24

        if is_new_high:

            badge_alpha = int(170 + pulse * 85)

            badge_font = pygame.font.SysFont("Arial", 20, bold=True)
            badge = badge_font.render("★ NEW HIGH SCORE ★", True, (255, 215, 0))
            badge.set_alpha(badge_alpha)

            screen.blit(
                badge,
                (settings.WIDTH // 2 - badge.get_width() // 2, y + 4),
            )

        # ==================================
        # Restart Button
        # ==================================

        restart_glow = int(150 + pulse * 40)

        restart_rect = pygame.Rect(
            settings.WIDTH // 2 - 130, BOX_Y + 250, 260, 38
        )

        pygame.draw.rect(
            screen,
            (0, 150, 0),
            restart_rect,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (0, restart_glow, 0),
            restart_rect,
            2,
            border_radius=10
        )

        restart = small_font.render(
            "\u21bb  Press R to Restart",
            True,
            WHITE
        )

        screen.blit(
            restart,
            (
                restart_rect.centerx - restart.get_width() // 2,
                restart_rect.centery - restart.get_height() // 2
            )
        )

        # ==================================
        # Exit Button
        # ==================================

        exit_rect = pygame.Rect(
            settings.WIDTH // 2 - 130, BOX_Y + 296, 260, 38
        )

        pygame.draw.rect(
            screen,
            (160, 0, 0),
            exit_rect,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (min(160 + restart_glow - 100, 255), 0, 0),
            exit_rect,
            2,
            border_radius=10
        )

        exit_text = small_font.render(
            "\u2715  Press ESC to Exit",
            True,
            WHITE
        )

        screen.blit(
            exit_text,
            (
                exit_rect.centerx - exit_text.get_width() // 2,
                exit_rect.centery - exit_text.get_height() // 2
            )
        )

        present(screen)


pygame.quit()