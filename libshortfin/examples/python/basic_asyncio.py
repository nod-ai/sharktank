#!/usr/bin/env python
# Copyright 2024 Advanced Micro Devices, Inc
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import asyncio
import threading
import time

from _shortfin import asyncio_bridge
from _shortfin import lib as sfl

lsys = sfl.local.host.CPUSystemBuilder().create_system()
worker = lsys.create_worker("main")
print("Worker:", worker)


async def do_something(delay):
    print(f"FROM ASYNC do_something (tid={threading.get_ident()})", delay)
    print("Time:", asyncio.get_running_loop().time(), "Delay:", delay)
    await asyncio.sleep(delay)
    print(f"DONE", delay)
    return delay


import random

fs = []
total_delay = 0.0
max_delay = 0.0
for i in range(5):
    delay = random.random() * 2
    total_delay += delay
    max_delay = max(max_delay, delay)
    print("SCHEDULE", i)
    fs.append(asyncio.run_coroutine_threadsafe(do_something(delay), worker.loop))

for f in fs:
    print(f.result())

print("TOTAL DELAY:", total_delay, "MAX:", max_delay)
