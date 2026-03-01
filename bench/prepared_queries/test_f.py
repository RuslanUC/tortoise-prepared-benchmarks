from random import choice, choices, randint

from tortoise.expressions import Q
from tortoise.parameter import Parameter

from bench.common.prepare_e import prepare_test, LEVEL_CHOICE
from bench.models import FkToJournalBigs
from bench.utils import run_test


async def _runtest(all_ids: list[int], count: int):
    for i in range(count):
        await FkToJournalBigs.prepare_sql("prep_test_e").filter(
            Q(journal1__level=Parameter("lvl"), id__in=Parameter("ids"))
            | Q(journal2__level__in=Parameter("lvls"), id__gt=all_ids[int(len(all_ids) * 0.9)])
            | Q(journal3__col_int3__gte=1000, journal4__col_int4__lte=10000)
        ).order_by("id").select_related(
            "journal1", "journal2", "journal3", "journal4"
        ).order_by("id").first().prepared().execute(
            lvl=choice(LEVEL_CHOICE),
            ids=choices(all_ids, k=randint(5, 15)),
            lvls=choices(LEVEL_CHOICE, k=2),
        )


async def runtest(loopstr: str, total_iters: int, concurrent: int) -> None:
    await run_test(
        loopstr=loopstr,
        test_name="F",
        total_iters=total_iters,
        concurrent=concurrent,
        prepare_func=prepare_test,
        test_func=_runtest,
    )