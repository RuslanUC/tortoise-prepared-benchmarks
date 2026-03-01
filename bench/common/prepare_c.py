import random

from bench.models import JournalSmallFk

LEVEL_CHOICE = [10, 20, 30, 40, 50]


async def prepare_test() -> list[int]:
    await JournalSmallFk.bulk_create([
        JournalSmallFk(
            level=random.choice(LEVEL_CHOICE),
            text=f"some journal {i}",
            parent=None,
        )
        for i in range(100)
    ])

    parents = await JournalSmallFk.all()

    await JournalSmallFk.bulk_create([
        JournalSmallFk(
            level=random.choice(LEVEL_CHOICE),
            text=f"some journal {i}",
            parent=random.choice(parents),
        )
        for i in range(500)
    ])

    return await JournalSmallFk.all().values_list("id", flat=True)
