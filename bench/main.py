#!/usr/bin/env python
import os
import random
import sys
from argparse import ArgumentParser
from typing import Literal

try:
    concurrents = int(os.environ.get("CONCURRENTS", "10"))
except ValueError:
    concurrents = 1

try:
    total_iterations = int(os.environ.get("ITERATIONS", "1000"))
except ValueError:
    total_iterations = 1

if concurrents != 10:
    loopstr = f" C{concurrents}"
else:
    loopstr = ""

if os.environ.get("UVLOOP", ""):
    import asyncio

    try:
        import uvloop
    except ImportError:
        uvloop = None
    else:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

if concurrents > 1 and sys.version_info < (3, 7):
    sys.exit()

dbtype = os.environ.get("DBTYPE", "")
if dbtype == "postgres":
    db_url = f"postgres://postgres:{os.environ.get('PASSWORD')}@127.0.0.1:{os.environ.get('PGPORT', '5432')}/tbench?minsize={concurrents}&maxsize={concurrents}"
elif dbtype == "mysql":
    db_url = f"mysql://root:{os.environ.get('PASSWORD')}@127.0.0.1:{os.environ.get('MYPORT', '3306')}/tbench?minsize={concurrents}&maxsize={concurrents}"
else:
    db_url = "sqlite:///tmp/db.sqlite3"

from .regular_queries import test_a as reg_test_a
from .regular_queries import test_b as reg_test_b
from .regular_queries import test_c as reg_test_c
from .regular_queries import test_d as reg_test_d
from .regular_queries import test_e as reg_test_e
from .regular_queries import test_f as reg_test_f
from .regular_queries import test_g as reg_test_g

from .prepared_queries import test_a as pre_test_a
from .prepared_queries import test_b as pre_test_b
from .prepared_queries import test_c as pre_test_c
from .prepared_queries import test_d as pre_test_d
from .prepared_queries import test_e as pre_test_e
from .prepared_queries import test_f as pre_test_f
from .prepared_queries import test_g as pre_test_g

from tortoise import Tortoise, run_async


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(db_url=db_url, modules={"models": ["bench.models"]})


async def create_db():
    # Generate the schema
    await init()
    await Tortoise.generate_schemas()


async def run_benchmarks_regular(random_state: tuple[int, ...] | None = None, print_header: bool = False) -> None:
    if random_state is not None:
        random.setstate(random_state)

    if print_header:
        print("Regular queries:")

    await reg_test_a.runtest(loopstr, total_iterations, concurrents)
    await reg_test_b.runtest(loopstr, total_iterations, concurrents)
    await reg_test_c.runtest(loopstr, total_iterations, concurrents)
    await reg_test_d.runtest(loopstr, total_iterations, concurrents)
    await reg_test_e.runtest(loopstr, total_iterations, concurrents)
    await reg_test_f.runtest(loopstr, total_iterations, concurrents)
    await reg_test_g.runtest(loopstr, total_iterations, concurrents)


async def run_benchmarks_prepared(random_state: tuple[int, ...] | None = None, print_header: bool = False) -> None:
    if random_state is not None:
        random.setstate(random_state)

    if print_header:
        print("Prepared queries:")

    await pre_test_a.runtest(loopstr, total_iterations, concurrents)
    await pre_test_b.runtest(loopstr, total_iterations, concurrents)
    await pre_test_c.runtest(loopstr, total_iterations, concurrents)
    await pre_test_d.runtest(loopstr, total_iterations, concurrents)
    await pre_test_e.runtest(loopstr, total_iterations, concurrents)
    await pre_test_f.runtest(loopstr, total_iterations, concurrents)
    await pre_test_g.runtest(loopstr, total_iterations, concurrents)


async def run_benchmarks(tests: list[Literal["regular", "prepared"]]):
    await create_db()

    random_state = random.getstate()
    if "regular" in tests:
        await run_benchmarks_regular(random_state, len(tests) > 1)
    if "prepared" in tests:
        await run_benchmarks_prepared(random_state, len(tests) > 1)


def main() -> None:
    available_tests = ("regular", "prepared")

    parser = ArgumentParser()
    parser.add_argument("tests", nargs="*", default=list(available_tests), choices=available_tests)
    args = parser.parse_args()

    run_async(run_benchmarks(args.tests))


if __name__ == "__main__":
    main()
