import asyncio
import time
from functools import wraps
from typing import Callable, cast, ParamSpec, TypeVar, Awaitable

from tortoise.backends.base.client import TransactionalDBClient
from tortoise.transactions import in_transaction

P = ParamSpec("P")
T = TypeVar("T")
FuncType = Callable[P, T]
F = TypeVar("F", bound=FuncType)


def atomic_rollback(connection_name: str | None = None) -> Callable[[F], F]:
    def wrapper(func: F) -> F:
        @wraps(func)
        async def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            tconn: TransactionalDBClient

            async with in_transaction(connection_name) as tconn:
                result = await func(*args, **kwargs)
                await tconn.rollback()
                return result

        return wrapped

    return wrapper


@atomic_rollback()
async def run_test(
        loopstr: str, tests_name: str, test_name: str, total_iters: int, concurrent: int,
        prepare_func: Callable[..., Awaitable[T]], test_func: Callable[[T, int], Awaitable[...]],
) -> None:
    data = await prepare_func()

    start = time.time()

    await asyncio.gather(*[test_func(data, total_iters // concurrent) for _ in range(concurrent)])

    now = time.time()

    print(f"{tests_name}{loopstr}, {test_name}: Rows/sec: {total_iters / (now - start): 10.2f}")