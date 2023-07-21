#!/usr/bin/env python3
'''This is a module'''


from typing import Any, Union, Sequence


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    '''A function'''
    if lst:
        return lst[0]
    else:
        return None
