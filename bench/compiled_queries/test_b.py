from random import choice

from tortoise.parameter import Parameter

from bench.common.prepare_b import prepare_test, LEVEL_CHOICE
from bench.models import JournalSmall
from bench.compiled_queries import NAME
from bench.utils import run_test


async def _runtest(ids: tuple[int, int], count: int):
    min_id, max_id = ids
    mid_id = min_id + (max_id - min_id) // 2
    for i in range(count):
        await JournalSmall.filter(
            id__gte=mid_id, level=Parameter("lvl"),
        ).compile("prep_test_b").execute(lvl=choice(LEVEL_CHOICE))


async def runtest(loopstr: str, total_iters: int, concurrent: int) -> None:
    await run_test(
        loopstr=loopstr,
        tests_name=NAME,
        test_name="B",
        total_iters=total_iters,
        concurrent=concurrent,
        prepare_func=prepare_test,
        test_func=_runtest,
    )