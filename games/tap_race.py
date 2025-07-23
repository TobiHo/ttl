import pygame
import random

WIDTH, HEIGHT = 640, 480
CELL_SIZE = 80
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
BACKGROUND_COLOR = (30, 30, 30)
CELL_COLOR = (200, 30, 30)
GRID_COLOR = (50, 50, 50)


def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tap Race")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    spawn_delay = 500
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, spawn_delay)

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game_over and event.type == spawn_event:
                empty = [
                    (r, c)
                    for r in range(ROWS)
                    for c in range(COLS)
                    if not grid[r][c]
                ]
                if not empty:
                    game_over = True
                else:
                    r, c = random.choice(empty)
                    grid[r][c] = 1
                    spawn_delay = max(50, spawn_delay - 40)
                    pygame.time.set_timer(spawn_event, spawn_delay)
            elif not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                c = x // CELL_SIZE
                r = y // CELL_SIZE
                if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c]:
                    grid[r][c] = 0

        screen.fill(BACKGROUND_COLOR)
        for r in range(ROWS):
            for c in range(COLS):
                rect = pygame.Rect(
                    c * CELL_SIZE,
                    r * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                if grid[r][c]:
                    pygame.draw.rect(screen, CELL_COLOR, rect)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)

        if game_over:
            text = font.render("Game Over", True, (255, 255, 255))
            screen.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - text.get_height() // 2,
                ),
            )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
