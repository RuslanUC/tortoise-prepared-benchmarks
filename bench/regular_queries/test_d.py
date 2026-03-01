from random import choice

from bench.common.prepare_d import prepare_test
from bench.models import JournalSmallFk
from bench.regular_queries import NAME
from bench.utils import run_test


async def _runtest(all_ids: list[int], count: int):
    for i in range(count):
        await JournalSmallFk.get(id=choice(all_ids)).select_related("parent")


async def runtest(loopstr: str, total_iters: int, concurrent: int) -> None:
    await run_test(
        loopstr=loopstr,
        tests_name=NAME,
        test_name="D",
        total_iters=total_iters,
        concurrent=concurrent,
        prepare_func=prepare_test,
        test_func=_runtest,
    )
