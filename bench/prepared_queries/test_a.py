import asyncio
import time
from random import randint

from tortoise.parameter import Parameter

from bench.common.prepare_a import prepare_test
from bench.models import JournalSmall
from bench.utils import atomic_rollback


async def _runtest(min_id: int, max_id: int, count: int):
    for i in range(count):
        await JournalSmall.prepare_sql("prep_test_a").get_or_none(
            id=Parameter("search_id"),
        ).prepared().execute(search_id=randint(min_id, max_id))


@atomic_rollback()
async def runtest(loopstr: str, total_iters: int, concurrent: int) -> None:
    min_id, max_id = await prepare_test()

    start = time.time()

    await asyncio.gather(*[_runtest(min_id, max_id, total_iters // concurrent) for _ in range(concurrent)])

    now = time.time()

    print(f"Tortoise ORM{loopstr}, A: Rows/sec: {total_iters / (now - start): 10.2f}")
