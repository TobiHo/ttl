"""Simple Pong game using pygame.

This module implements a minimal two-player Pong clone. It can be started
directly or run via :mod:`main`.
"""

import pygame


WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
BALL_SPEED = [4, 4]


def run() -> None:
    """Run the Pong game loop."""

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    left_paddle = pygame.Rect(10, (HEIGHT - PADDLE_HEIGHT) // 2,
                              PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 20, (HEIGHT - PADDLE_HEIGHT) // 2,
                               PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect((WIDTH - BALL_SIZE) // 2,
                       (HEIGHT - BALL_SIZE) // 2,
                       BALL_SIZE, BALL_SIZE)
    ball_speed = BALL_SPEED[:]
    left_score = 0
    right_score = 0
    font = pygame.font.Font(None, 74)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= 5
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += 5
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= 5
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += 5

        # Move ball
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Collisions with top/bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]

        # Collisions with paddles
        if ball.colliderect(left_paddle) and ball_speed[0] < 0:
            ball_speed[0] = -ball_speed[0]
        if ball.colliderect(right_paddle) and ball_speed[0] > 0:
            ball_speed[0] = -ball_speed[0]

        # Scoring
        if ball.left <= 0:
            right_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed = BALL_SPEED[:]
            ball_speed[0] = -ball_speed[0]
        elif ball.right >= WIDTH:
            left_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed = BALL_SPEED[:]

        # Drawing
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), left_paddle)
        pygame.draw.rect(screen, (255, 255, 255), right_paddle)
        pygame.draw.ellipse(screen, (255, 255, 255), ball)

        score_surf = font.render(f"{left_score} {right_score}", True, (255, 255, 255))
        screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    run()

