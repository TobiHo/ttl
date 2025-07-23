from ttl_timer import start_ttl_timer


def run():
    print('Pixel Jump – warte auf "LOS" und druecke dann Enter!')
    input('Bereit? Enter druecken...')
    timer = start_ttl_timer()
    input('LOS!')
    elapsed = timer()
    print(f'Deine Zeit: {elapsed:.2f}s')
    return elapsed
