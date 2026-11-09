# Тема: Тестирование async: `pytest-asyncio`
# Запуск из папки lecture: pytest 3_asyncio/18_test_async.py -v
# Нужен pytest-asyncio: pip install pytest-asyncio

import asyncio
import pytest

async def fetch_delayed(x: int, delay: float) -> int:
    await asyncio.sleep(delay)
    return x * 2

@pytest.mark.asyncio
async def test_fetch() -> None:
    result = await fetch_delayed(21, 0.01)
    assert result == 42

@pytest.mark.asyncio
async def test_gather() -> None:
    results = await asyncio.gather(
        fetch_delayed(1, 0.01),
        fetch_delayed(2, 0.01),
        fetch_delayed(3, 0.01),
    )
    assert results == [2, 4, 6]
