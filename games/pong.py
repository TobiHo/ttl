import pygame

WIDTH, HEIGHT = 640, 480
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80


def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    ball_speed_x = 4
    ball_speed_y = 4
    ball_rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2,
                             HEIGHT // 2 - BALL_SIZE // 2,
                             BALL_SIZE, BALL_SIZE)
    player_rect = pygame.Rect(20, HEIGHT // 2 - PADDLE_HEIGHT // 2,
                              PADDLE_WIDTH, PADDLE_HEIGHT)
    computer_rect = pygame.Rect(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2,
                                PADDLE_WIDTH, PADDLE_HEIGHT)

    player_score = 0
    computer_score = 0

    running = True
    while running and computer_score < 10:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_rect.move_ip(0, -5)
        if keys[pygame.K_DOWN]:
            player_rect.move_ip(0, 5)
        player_rect.clamp_ip(screen.get_rect())

        computer_rect.centery = ball_rect.centery
        computer_rect.clamp_ip(screen.get_rect())

        ball_rect.x += ball_speed_x
        ball_rect.y += ball_speed_y

        if ball_rect.top <= 0 or ball_rect.bottom >= HEIGHT:
            ball_speed_y *= -1

        if ball_rect.colliderect(player_rect) and ball_speed_x < 0:
            ball_speed_x *= -1
        if ball_rect.colliderect(computer_rect) and ball_speed_x > 0:
            ball_speed_x *= -1

        if ball_rect.left <= 0:
            computer_score += 1
            ball_speed_x = abs(ball_speed_x) + 1
            ball_rect.center = (WIDTH // 2, HEIGHT // 2)
        if ball_rect.right >= WIDTH:
            player_score += 1
            ball_speed_x = -abs(ball_speed_x)
            ball_rect.center = (WIDTH // 2, HEIGHT // 2)

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), player_rect)
        pygame.draw.rect(screen, (255, 255, 255), computer_rect)
        pygame.draw.ellipse(screen, (255, 255, 255), ball_rect)
        score_surf = font.render(f"{player_score} : {computer_score}", True, (255, 255, 255))
        screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 10))
        pygame.display.flip()
        clock.tick(60)

    if running:
        screen.fill((0, 0, 0))
        msg = font.render("Computer gewinnt!", True, (255, 0, 0))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2,
                          HEIGHT // 2 - msg.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    pygame.quit()

