import time
from itertools import cycle


def permLoopingChar(sleep: bool = False):
    chars = '\|/-'
    states = cycle(chars)
    while True:
        txt = next(states)
        yield txt
        if sleep:
            time.sleep(0.15)


gen = permLoopingChar()
