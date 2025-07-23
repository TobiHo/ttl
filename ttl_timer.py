import time


class TtlTimer:
    """Timer mit Unterstuetzung fuer Pausieren und Fortsetzen."""

    def __init__(self):
        self.start = time.time()
        self.paused_time = 0.0
        self.pause_start = None

    def pause(self):
        if self.pause_start is None:
            self.pause_start = time.time()

    def resume(self):
        if self.pause_start is not None:
            self.paused_time += time.time() - self.pause_start
            self.pause_start = None

    def elapsed(self):
        current_pause = 0.0
        if self.pause_start is not None:
            current_pause = time.time() - self.pause_start
        return time.time() - self.start - self.paused_time - current_pause


def start_ttl_timer():
    """Rueckwaertskompatible Funktion, liefert einen ``TtlTimer``."""
    return TtlTimer()
