from ttl_timer import start_ttl_timer


def run():
    print('Pixel Jump – wer reagiert schneller?')
    input('Bereit? Enter druecken...')
    timer = start_ttl_timer()
    input('LOS!')
    player_time = timer()
    computer_time = 0.05
    print(f'Deine Zeit: {player_time:.2f}s')
    print(f'Computer Zeit: {computer_time:.2f}s')
    print('Computer gewinnt!')
    return player_time, computer_time
