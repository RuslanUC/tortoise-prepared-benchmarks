import random

from bench.models import JournalBig1, JournalBig2, JournalBig3, JournalBig4, FkToJournalBigs

LEVEL_CHOICE = [10, 20, 30, 40, 50]


async def prepare_test() -> list[int]:
    await JournalBig1.bulk_create([
        JournalBig1(
            level=random.choice(LEVEL_CHOICE),
            text=f"some journal 1 {i}",
        )
        for i in range(100)
    ])
    await JournalBig2.bulk_create([
        JournalBig2(
            level=random.choice(LEVEL_CHOICE),
            text=f"some journal 2 {i}",
            col_int2=random.randint(100, 100000),
        )
        for i in range(100)
    ])
    await JournalBig3.bulk_create([
        JournalBig3(
            level=random.choice(LEVEL_CHOICE),
            text=f"some journal 3 {i}",
            col_int3=random.randint(100, 100000),
        )
        for i in range(100)
    ])
    await JournalBig4.bulk_create([
        JournalBig4(
            level=random.choice(LEVEL_CHOICE),
            text=f"some journal 4 {i}",
            col_int4=random.randint(100, 100000),
        )
        for i in range(100)
    ])

    all1 = await JournalBig1.all()
    all2 = await JournalBig2.all()
    all3 = await JournalBig3.all()
    all4 = await JournalBig4.all()

    await FkToJournalBigs.bulk_create([
        FkToJournalBigs(
            journal1=random.choice(all1),
            journal2=random.choice((random.choice(all2), None)),
            journal3=random.choice(all3),
            journal4=random.choice((random.choice(all4), None)),
        )
        for _ in range(500)
    ])

    all_ids = await FkToJournalBigs.all().values_list("id", flat=True)
    all_ids.sort()
    return all_ids
