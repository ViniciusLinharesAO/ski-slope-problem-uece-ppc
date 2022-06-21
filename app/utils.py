"""app.utils

Module that contains util functions.
"""
import random


def random_bool():
    return bool(random.getrandbits(1))
