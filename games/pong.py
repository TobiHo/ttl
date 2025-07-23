from ttl_timer import start_ttl_timer


def run():
    print('Pong – druecke Enter sobald "START" erscheint!')
    input('Bereit? Enter druecken...')
    timer = start_ttl_timer()
    input('START!')
    elapsed = timer()
    print(f'Deine Zeit: {elapsed:.2f}s')
    return elapsed
