from ttl_timer import start_ttl_timer


def run():
    print('Breakout – druecke Enter so schnell wie moeglich wenn "GO" erscheint.')
    input('Bereit? Enter druecken...')
    timer = start_ttl_timer()
    input('GO!')
    elapsed = timer()
    print(f'Deine Zeit: {elapsed:.2f}s')
    return elapsed
