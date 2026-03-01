from random import choice

from tortoise.parameter import Parameter

from bench.common.prepare_c import prepare_test, LEVEL_CHOICE
from bench.models import JournalSmallFk
from bench.prepared_queries import NAME
from bench.utils import run_test


async def _runtest(_: list[int], count: int):
    for i in range(count):
        await JournalSmallFk.prepare_sql("prep_test_c").filter(
            level=Parameter("lvl"), parent_id__isnull=False,
        ).select_related("parent").prepared().execute(lvl=choice(LEVEL_CHOICE))


async def runtest(loopstr: str, total_iters: int, concurrent: int) -> None:
    await run_test(
        loopstr=loopstr,
        tests_name=NAME,
        test_name="C",
        total_iters=total_iters,
        concurrent=concurrent,
        prepare_func=prepare_test,
        test_func=_runtest,
    )