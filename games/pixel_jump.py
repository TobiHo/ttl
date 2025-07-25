import pygame
import random
from ttl_timer import TtlTimer

WIDTH, HEIGHT = 640, 480
GROUND_HEIGHT = 40
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 30
BACKGROUND_COLOR = (0, 0, 0)
GROUND_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (255, 255, 255)
PLAYER_SPEED = 5
JUMP_VELOCITY = -12
GRAVITY = 0.6
FPS = 60
SPAWN_EVENT = pygame.USEREVENT + 1

# simple pixel figure for the player (5x8 grid)
PIXEL_MAN = [
    "  X  ",
    " XXX ",
    "X X X",
    "XXXXX",
    "X X X",
    "X X X",
    "X   X",
    "X   X",
]


def draw_pixel_man(surface, rect, color=(255, 255, 255)):
    pixel_w = rect.width // len(PIXEL_MAN[0])
    pixel_h = rect.height // len(PIXEL_MAN)
    for r, line in enumerate(PIXEL_MAN):
        for c, ch in enumerate(line):
            if ch == "X":
                pygame.draw.rect(
                    surface,
                    color,
                    pygame.Rect(
                        rect.x + c * pixel_w,
                        rect.y + r * pixel_h,
                        pixel_w,
                        pixel_h,
                    ),
                )


def run(ttl_timer: TtlTimer):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pixel Jump")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    ground = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
    player = pygame.Rect(
        100,
        ground.top - PLAYER_HEIGHT,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )
    player_vel_y = 0

    obstacles = []
    spawn_delay = 1200
    obstacle_speed = 5
    pygame.time.set_timer(SPAWN_EVENT, spawn_delay)

    running = True
    game_over = False
    start_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_EVENT and not game_over:
                width = random.randint(40, 80)
                height = random.randint(40, 120)
                top = ground.top - height
                if random.random() < 0.3:
                    top -= random.choice([40, 80, 120])
                if random.random() < 0.2:
                    width = random.randint(80, 120)
                obstacles.append(pygame.Rect(WIDTH, top, width, height))
                spawn_delay = max(400, spawn_delay - 25)
                obstacle_speed += 0.1
                pygame.time.set_timer(SPAWN_EVENT, spawn_delay)

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT]:
                player.x -= PLAYER_SPEED
                if player.x < 0:
                    player.x = 0
            if keys[pygame.K_RIGHT]:
                player.x += PLAYER_SPEED
                if player.right > WIDTH:
                    player.right = WIDTH
            if keys[pygame.K_SPACE] and player_vel_y == 0:
                player_vel_y = JUMP_VELOCITY

        player_vel_y += GRAVITY
        player.y += player_vel_y

        if player.colliderect(ground) and player_vel_y >= 0:
            player.bottom = ground.top
            player_vel_y = 0

        for obs in obstacles[:]:
            obs.x -= int(obstacle_speed)
            if obs.right < 0:
                obstacles.remove(obs)
                continue
            if player.colliderect(obs):
                if player_vel_y > 0 and player.bottom - player_vel_y <= obs.top:
                    player.bottom = obs.top
                    player_vel_y = 0
                else:
                    player.right = obs.left
                    if player.left <= 0:
                        game_over = True

        if player.top > HEIGHT:
            game_over = True

        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, GROUND_COLOR, ground)
        for obs in obstacles:
            pygame.draw.rect(screen, OBSTACLE_COLOR, obs)
        draw_pixel_man(screen, player)

        ttl_surf = font.render(f"TTL: {ttl_timer.elapsed():.2f}s", True, (200, 200, 200))
        screen.blit(ttl_surf, (10, 10))

        if game_over:
            pygame.display.flip()
            break

        pygame.display.flip()
        clock.tick(FPS)

    player_time = (pygame.time.get_ticks() - start_time) / 1000.0
    ttl_timer.pause()
    screen.fill(BACKGROUND_COLOR)
    text = font.render(f"Time: {player_time:.2f}s", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    ttl_timer.resume()

    pygame.quit()
    return player_time
