from ttl_timer import start_ttl_timer


def run():
    print('Tap Race – tippe so schnell wie moeglich zwei Mal Enter wenn "GO" kommt!')
    input('Bereit? Enter druecken...')
    timer = start_ttl_timer()
    input('GO!')
    input('Nochmal!')
    elapsed = timer()
    print(f'Deine Zeit: {elapsed:.2f}s')
    return elapsed
