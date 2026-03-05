from random import choice, choices, randint

from tortoise.expressions import Q
from tortoise.parameter import Parameter

from bench.common.prepare_e import prepare_test, LEVEL_CHOICE
from bench.models import JournalBig
from bench.compiled_queries import NAME
from bench.utils import run_test


async def _runtest(all_ids: list[int], count: int):
    for i in range(count):
        await JournalBig.filter(
            Q(level=Parameter("lvl"), id__in=Parameter("ids"))
            | Q(level__in=Parameter("lvls"), id__gt=all_ids[int(len(all_ids) * 0.9)])
            | Q(col_int3__gte=1000, col_int3__lte=10000)
        ).order_by("id").first().compile("prep_test_e").execute(
            lvl=choice(LEVEL_CHOICE),
            ids=choices(all_ids, k=randint(5, 15)),
            lvls=choices(LEVEL_CHOICE, k=2),
        )


async def runtest(loopstr: str, total_iters: int, concurrent: int) -> None:
    await run_test(
        loopstr=loopstr,
        tests_name=NAME,
        test_name="E",
        total_iters=total_iters,
        concurrent=concurrent,
        prepare_func=prepare_test,
        test_func=_runtest,
    )