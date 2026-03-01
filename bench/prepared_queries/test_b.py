from random import choice

from tortoise.parameter import Parameter

from bench.common.prepare_a import prepare_test, LEVEL_CHOICE
from bench.models import JournalSmall
from bench.utils import run_test


async def _runtest(ids: tuple[int, int], count: int):
    min_id, max_id = ids
    mid_id = min_id + (max_id - min_id) // 2
    for i in range(count):
        await JournalSmall.prepare_sql("prep_test_b").filter(
            id__gte=mid_id, level=Parameter("lvl"),
        ).prepared().execute(lvl=choice(LEVEL_CHOICE))


async def runtest(loopstr: str, total_iters: int, concurrent: int) -> None:
    await run_test(
        loopstr=loopstr,
        test_name="B",
        total_iters=total_iters,
        concurrent=concurrent,
        prepare_func=prepare_test,
        test_func=_runtest,
    )