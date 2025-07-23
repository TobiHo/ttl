import json
import os
import time
import pygame
from ttl_timer import TtlTimer

from games import breakout, pixel_jump, tap_race, pong

LEADERBOARD_FILE = 'leaderboard.json'


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_leaderboard(entries):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(entries, f)


def show_start_screen(entries):
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('TTL')
    font = pygame.font.SysFont(None, 36)

    start_button = pygame.Rect(270, 400, 100, 40)

    running = True
    start = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
                start = True
                running = False

        screen.fill((0, 0, 0))
        title = font.render('TTL – Minispiele', True, (255, 255, 255))
        screen.blit(title, (320 - title.get_width() // 2, 20))

        y = 80
        label = font.render('Beste Zeiten', True, (200, 200, 200))
        screen.blit(label, (40, y))
        y += 40
        for idx, entry in enumerate(sorted(entries, key=lambda e: e['time'])[:5], start=1):
            text = font.render(f"{idx}. {entry['name']} - {entry['time']:.2f}s", True, (255, 255, 255))
            screen.blit(text, (40, y))
            y += 30

        runs_text = font.render(f"Durchlaeufe: {len(entries)}", True, (255, 255, 255))
        screen.blit(runs_text, (40, 360))

        pygame.draw.rect(screen, (255, 255, 255), start_button)
        btn_text = font.render('Start', True, (0, 0, 0))
        screen.blit(btn_text, (start_button.centerx - btn_text.get_width() // 2,
                               start_button.centery - btn_text.get_height() // 2))

        pygame.display.flip()
        pygame.time.wait(30)

    pygame.quit()
    return start


def show_end_screen(total_time):
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Ergebnis')
    font = pygame.font.SysFont(None, 36)

    input_box = pygame.Rect(220, 220, 200, 40)
    save_button = pygame.Rect(270, 280, 100, 40)
    name = ''
    active = False
    running = True
    result = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if save_button.collidepoint(event.pos):
                    result = name.strip()
                    running = False
            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    result = name.strip()
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if event.unicode.isprintable() and len(name) < 20:
                        name += event.unicode

        screen.fill((0, 0, 0))
        time_surf = font.render(f'Gesamtzeit: {total_time:.2f}s', True, (255, 255, 255))
        screen.blit(time_surf, (320 - time_surf.get_width() // 2, 150))

        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        name_surf = font.render(name, True, (255, 255, 255))
        screen.blit(name_surf, (input_box.x + 5, input_box.y + 5))

        pygame.draw.rect(screen, (255, 255, 255), save_button)
        btn_text = font.render('OK', True, (0, 0, 0))
        screen.blit(btn_text, (save_button.centerx - btn_text.get_width() // 2,
                               save_button.centery - btn_text.get_height() // 2))

        pygame.display.flip()
        pygame.time.wait(30)

    pygame.quit()
    return result


def run_all_games(ttl: TtlTimer):
    total = 0.0
    for game in (pong.run, breakout.run, pixel_jump.run, tap_race.run):
        total += game(ttl)
    return total


def main():
    leaderboard = load_leaderboard()
    while True:
        if not show_start_screen(leaderboard):
            break

        ttl = TtlTimer()
        total_time = run_all_games(ttl)

        name = show_end_screen(total_time)
        if name:
            leaderboard.append({'name': name, 'time': total_time})
            save_leaderboard(leaderboard)


if __name__ == '__main__':
    main()
