#!/usr/bin/env python3
'''This is a module'''

import asyncio
from typing import List
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    '''A function'''
    s = time.perf_counter()
    await asyncio.gather(*[async_comprehension() for i in range(4)])
    elapsed = time.perf_counter() - s
    
    return elapsed
