#!/usr/bin/env python3
'''This is a module'''


from typing import List
import asyncio
task_wait_random = __import__('3-tasks').wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    ''' A function'''
    lst = []
    for i in range(n):
        num = await task_wait_random(max_delay)
        lst.append(num)
    return sorted(lst)
