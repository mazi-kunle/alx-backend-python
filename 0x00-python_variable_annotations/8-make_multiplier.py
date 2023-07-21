#!/usr/bin/env python3
'''This is a module'''


from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    '''
    A function that takes a float as parameter and
    returns a function that multiplies a float by
    multiplier
    '''
    def func(n: float) -> float:
        '''
        returns n * multiplier
        '''
        return n * multiplier

    return func
