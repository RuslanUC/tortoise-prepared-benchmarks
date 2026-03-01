#!/usr/bin/env python
import os
import sys

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
        pass
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

from .prepared_queries import test_a as pre_test_a
from .prepared_queries import test_b as pre_test_b

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


async def run_benchmarks_regular() -> None:
    print("Regular queries:")
    await reg_test_a.runtest(loopstr, total_iterations, concurrents)
    await reg_test_b.runtest(loopstr, total_iterations, concurrents)


async def run_benchmarks_prepared() -> None:
    print("Prepared queries:")
    await pre_test_a.runtest(loopstr, total_iterations, concurrents)
    await pre_test_b.runtest(loopstr, total_iterations, concurrents)


async def run_benchmarks():
    await create_db()
    await run_benchmarks_regular()
    await run_benchmarks_prepared()


def main() -> None:
    run_async(run_benchmarks())


if __name__ == "__main__":
    main()
