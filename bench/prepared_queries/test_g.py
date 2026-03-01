from random import choices, randint

from tortoise.parameter import Parameter

from bench.common.prepare_c import prepare_test
from bench.models import JournalSmallFk
from bench.prepared_queries import NAME
from bench.utils import run_test


async def _runtest(all_ids: list[int], count: int):
    for i in range(count):
        await JournalSmallFk.prepare_sql("prep_test_g").filter(
            level__in=Parameter("ids"),
        ).select_related("parent").prepared().execute(
            ids=choices(all_ids, k=randint(1, len(all_ids))),
        )


async def runtest(loopstr: str, total_iters: int, concurrent: int) -> None:
    await run_test(
        loopstr=loopstr,
        tests_name=NAME,
        test_name="G",
        total_iters=total_iters,
        concurrent=concurrent,
        prepare_func=prepare_test,
        test_func=_runtest,
    )