import pygame
import random
import os
import sys

try:
    from ttl_timer import start_ttl_timer
except ImportError:  # allow running this module directly
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from ttl_timer import start_ttl_timer

WIDTH, HEIGHT = 640, 480
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 20
BULLET_WIDTH, BULLET_HEIGHT = 4, 10
BLOCK_SIZE = 30
BACKGROUND_COLOR = (0, 0, 0)
PLAYER_COLOR = (255, 255, 255)
BULLET_COLOR = (0, 255, 0)
BLOCK_COLOR = (255, 0, 0)


def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Breakout")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    timer = start_ttl_timer()

    player_rect = pygame.Rect(
        WIDTH // 2 - PLAYER_WIDTH // 2,
        HEIGHT - PLAYER_HEIGHT - 10,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )
    bullets = []
    blocks = []

    spawn_delay = 1000
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, spawn_delay)

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = pygame.Rect(
                    player_rect.centerx - BULLET_WIDTH // 2,
                    player_rect.top - BULLET_HEIGHT,
                    BULLET_WIDTH,
                    BULLET_HEIGHT,
                )
                bullets.append(bullet)
            elif not game_over and event.type == spawn_event:
                x = random.randint(0, WIDTH - BLOCK_SIZE)
                block = pygame.Rect(x, -BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                blocks.append(block)
                spawn_delay = max(200, spawn_delay - 20)
                pygame.time.set_timer(spawn_event, spawn_delay)

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_rect.x -= 5
            if keys[pygame.K_RIGHT]:
                player_rect.x += 5
            player_rect.clamp_ip(screen.get_rect())

            for bullet in bullets[:]:
                bullet.y -= 10
                if bullet.bottom < 0:
                    bullets.remove(bullet)

            for block in blocks[:]:
                block.y += 3
                if block.bottom >= HEIGHT:
                    game_over = True
                for bullet in bullets[:]:
                    if block.colliderect(bullet):
                        blocks.remove(block)
                        bullets.remove(bullet)
                        break

            screen.fill(BACKGROUND_COLOR)
            pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
            for bullet in bullets:
                pygame.draw.rect(screen, BULLET_COLOR, bullet)
            for block in blocks:
                pygame.draw.rect(screen, BLOCK_COLOR, block)

            pygame.display.flip()
            clock.tick(60)
        else:
            player_time = timer()
            screen.fill(BACKGROUND_COLOR)
            text = font.render(f"Time: {player_time:.2f}s", True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

    pygame.quit()
