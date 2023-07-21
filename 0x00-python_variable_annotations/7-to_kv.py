#!/usr/bin/env python3
'''This is a module'''


from typing import Union, Tuple


def to_kv(k: str, v: Union[float, int]) -> Tuple[str, float]:
    '''
    A function that takes a string and an int or float
    and returns a tuple
    '''
    return (k, v ** 2)
