import pygame
import random
from ttl_timer import TtlTimer

WIDTH, HEIGHT = 640, 480
GROUND_HEIGHT = 40
PLAYER_SIZE = 20
PLAYER_SPEED = 5
JUMP_VELOCITY = -12
GRAVITY = 0.6
FPS = 60
SPAWN_EVENT = pygame.USEREVENT + 1


def run(ttl_timer: TtlTimer):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pixel Jump")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    ground = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
    player = pygame.Rect(100, ground.top - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
    player_vel_y = 0

    obstacles = []
    spawn_delay = 1500
    obstacle_speed = 4
    pygame.time.set_timer(SPAWN_EVENT, spawn_delay)

    running = True
    game_over = False
    start_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_EVENT and not game_over:
                height = random.randint(20, 80)
                top = ground.top - height
                if random.random() < 0.3:
                    top -= random.choice([40, 80])
                obstacles.append(pygame.Rect(WIDTH, top, 40, height))
                spawn_delay = max(500, spawn_delay - 20)
                obstacle_speed += 0.05
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

        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, (200, 200, 200), ground)
        for obs in obstacles:
            pygame.draw.rect(screen, (50, 200, 50), obs)
        pygame.draw.rect(screen, (200, 50, 50), player)

        ttl_surf = font.render(f"TTL: {ttl_timer.elapsed():.2f}s", True, (200, 200, 200))
        screen.blit(ttl_surf, (10, 10))

        if game_over:
            pygame.display.flip()
            break

        pygame.display.flip()
        clock.tick(FPS)

    player_time = (pygame.time.get_ticks() - start_time) / 1000.0
    ttl_timer.pause()
    screen.fill((30, 30, 30))
    text = font.render(f"Time: {player_time:.2f}s", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    ttl_timer.resume()

    pygame.quit()
    return player_time
