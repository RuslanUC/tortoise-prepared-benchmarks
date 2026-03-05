from random import randint

from tortoise.parameter import Parameter

from bench.common.prepare_a import prepare_test
from bench.models import JournalSmall
from bench.compiled_queries import NAME
from bench.utils import run_test


async def _runtest(ids: tuple[int, int], count: int):
    min_id, max_id = ids
    for i in range(count):
        await JournalSmall.get_or_none(
            id=Parameter("search_id"),
        ).compile("prep_test_a").execute(search_id=randint(min_id, max_id))


async def runtest(loopstr: str, total_iters: int, concurrent: int) -> None:
    await run_test(
        loopstr=loopstr,
        tests_name=NAME,
        test_name="A",
        total_iters=total_iters,
        concurrent=concurrent,
        prepare_func=prepare_test,
        test_func=_runtest,
    )