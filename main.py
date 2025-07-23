import json
import os
import time
import pygame

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

        screen.fill((30, 30, 30))
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

        pygame.draw.rect(screen, (50, 200, 50), start_button)
        btn_text = font.render('Start', True, (0, 0, 0))
        screen.blit(btn_text, (start_button.centerx - btn_text.get_width() // 2,
                               start_button.centery - btn_text.get_height() // 2))

        pygame.display.flip()
        pygame.time.wait(30)

    pygame.quit()
    return start


def run_all_games():
    start = time.time()
    for game in (pong.run, breakout.run, pixel_jump.run, tap_race.run):
        game()
    return time.time() - start


def main():
    leaderboard = load_leaderboard()
    if not show_start_screen(leaderboard):
        return

    total_time = run_all_games()
    print(f'Gesamtzeit: {total_time:.2f}s')
    name = input('Name fuer Bestenliste: ').strip()
    if name:
        leaderboard.append({'name': name, 'time': total_time})
        save_leaderboard(leaderboard)


if __name__ == '__main__':
    main()
