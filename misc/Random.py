import random


def random_bool() -> bool:
    return bool(random.getrandbits(1))
