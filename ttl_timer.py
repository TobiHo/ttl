import time

def start_ttl_timer():
    start = time.time()
    return lambda: time.time() - start
