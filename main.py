import json
import os
from ttl_timer import start_ttl_timer
from games import breakout, pixel_jump, pong, tap_race

SCORES_FILE = 'scores.json'


def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    return {
        'breakout': [],
        'pixel_jump': [],
        'pong': [],
        'tap_race': []
    }


def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)


def show_ranking(scores):
    print('\n-- Aktuelle Bestzeiten --')
    for game, times in scores.items():
        best = min(times) if times else None
        if best is not None:
            print(f"{game}: {best:.2f}s")
        else:
            print(f"{game}: noch keine Zeit")
    print()


def main_menu():
    scores = load_scores()
    while True:
        show_ranking(scores)
        print('Waehle ein Spiel:')
        print('1) Breakout')
        print('2) Pixel Jump')
        print('3) Pong')
        print('4) Tap Race')
        print('5) Beenden')
        choice = input('> ')
        if choice == '1':
            t = breakout.run()
            scores['breakout'].append(t)
            save_scores(scores)
        elif choice == '2':
            t = pixel_jump.run()
            scores['pixel_jump'].append(t)
            save_scores(scores)
        elif choice == '3':
            t = pong.run()
            scores['pong'].append(t)
            save_scores(scores)
        elif choice == '4':
            t = tap_race.run()
            scores['tap_race'].append(t)
            save_scores(scores)
        elif choice == '5':
            break
        else:
            print('Ungueltige Eingabe')


if __name__ == '__main__':
    main_menu()
