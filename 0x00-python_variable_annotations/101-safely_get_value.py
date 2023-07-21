#!/usr/bin/env python3
'''This is a module'''


from typing import Mapping, TypeVar, Any, Union

T = TypeVar('T')
Def = Union[T, None]
Ret = Union[Any, T]


def safely_get_value(dct: Mapping, key: Any, default: Def = None) -> Ret:
    '''A function'''
    if key in dct:
        return dct[key]
    else:
        return default
