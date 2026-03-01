import random
from typing import cast

from tortoise.functions import Max, Min

from bench.models import JournalSmall


LEVEL_CHOICE = [10, 20, 30, 40, 50]


async def prepare_test() -> tuple[int, int]:
    await JournalSmall.bulk_create([
        JournalSmall(
            level=random.choice(LEVEL_CHOICE),
            text=f"some journal {i}",
        )
        for i in range(500)
    ])

    return cast(
        tuple[int, int],
        await JournalSmall.all().annotate(min_id=Min("id"), max_id=Max("id")).first().values_list("min_id", "max_id")
    )
