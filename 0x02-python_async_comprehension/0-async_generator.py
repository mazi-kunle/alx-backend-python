#!/usr/bin/env python3
'''This is a module'''

import asyncio
import random
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator[float, None]:
    '''A function'''
    for i in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
