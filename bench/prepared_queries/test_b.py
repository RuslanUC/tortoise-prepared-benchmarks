import asyncio
import time
from random import randint, choice

from tortoise.parameter import Parameter

from bench.common.prepare_a import prepare_test, LEVEL_CHOICE
from bench.models import JournalSmall
from bench.utils import atomic_rollback


async def _runtest(min_id: int, max_id: int, count: int):
    mid_id = min_id + (max_id - min_id) // 2
    for i in range(count):
        await JournalSmall.prepare_sql("prep_test_b").filter(
            id__gte=mid_id, level=Parameter("lvl"),
        ).prepared().execute(lvl=choice(LEVEL_CHOICE))


@atomic_rollback()
async def runtest(loopstr: str, total_iters: int, concurrent: int) -> None:
    min_id, max_id = await prepare_test()

    start = time.time()

    await asyncio.gather(*[_runtest(min_id, max_id, total_iters // concurrent) for _ in range(concurrent)])

    now = time.time()

    print(f"Tortoise ORM{loopstr}, B: Rows/sec: {total_iters / (now - start): 10.2f}")
