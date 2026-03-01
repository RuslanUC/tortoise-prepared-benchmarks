import random

from bench.models import JournalBig

LEVEL_CHOICE = [10, 20, 30, 40, 50]


async def prepare_test() -> list[int]:
    await JournalBig.bulk_create([
        JournalBig(
            level=random.choice(LEVEL_CHOICE),
            text=f"some journal {i}",
            col_int3=random.randint(100, 100000),
        )
        for i in range(500)
    ])

    all_ids = await JournalBig.all().values_list("id", flat=True)
    all_ids.sort()
    return all_ids
