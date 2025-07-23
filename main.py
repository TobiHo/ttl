from games import breakout, pixel_jump, tap_race, pong


def main():
    spiele = {
        '1': ('Pong', pong.run),
        '2': ('Breakout', breakout.run),
        '3': ('Pixel Jump', pixel_jump.run),
        '4': ('Tap Race', tap_race.run),
    }
    print('Waehle ein Spiel:')
    for key, (name, _) in spiele.items():
        print(f'{key}) {name}')
    auswahl = input('> ').strip()
    spiel = spiele.get(auswahl)
    if spiel:
        spiel[1]()
    else:
        print('Ungueltige Wahl')


if __name__ == '__main__':
    main()
