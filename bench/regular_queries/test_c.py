from random import choice

from bench.common.prepare_c import prepare_test, LEVEL_CHOICE
from bench.models import JournalSmallFk
from bench.utils import run_test


async def _runtest(_: list[int], count: int):
    for i in range(count):
        await JournalSmallFk.filter(level=choice(LEVEL_CHOICE), parent_id__isnull=False).select_related("parent")


async def runtest(loopstr: str, total_iters: int, concurrent: int) -> None:
    await run_test(
        loopstr=loopstr,
        test_name="C",
        total_iters=total_iters,
        concurrent=concurrent,
        prepare_func=prepare_test,
        test_func=_runtest,
    )
