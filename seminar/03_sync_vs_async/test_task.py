"""Все тесты задачи. Тестовый aiohttp-сервер создаётся через AioHTTPTestCase."""

import asyncio
import time
from functools import partial

import aiohttp
import requests
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from sync_vs_async import async_fetch, async_requests, sync_fetch, threaded_requests


class FetchingTestCase(AioHTTPTestCase):
    """Быстрый handler — проверяем корректность fetching (не скорость)."""

    async def get_application(self) -> web.Application:
        async def hello(request: web.Request) -> web.Response:
            return web.Response(text="Hello, asyncio!")

        app = web.Application()
        app.router.add_get("/", hello)
        return app

    @property
    def url(self) -> str:
        return f"http://{self.server.host}:{self.server.port}/"

    async def test_async_fetch_returns_body(self) -> None:
        async with aiohttp.ClientSession() as session:
            body = await async_fetch(session, self.url)
        assert body == "Hello, asyncio!"

    async def test_sync_fetch_returns_body(self) -> None:
        with requests.Session() as session:
            body = await asyncio.to_thread(partial(sync_fetch, session, self.url))
        assert body == "Hello, asyncio!"


class TimedTestCase(AioHTTPTestCase):
    """Медленный handler (1s) — проверяем что запросы реально параллелятся."""

    async def get_application(self) -> web.Application:
        async def sleepy(request: web.Request) -> web.Response:
            await asyncio.sleep(1)
            return web.Response(text="OK")

        app = web.Application()
        app.router.add_get("/", sleepy)
        return app

    @property
    def url(self) -> str:
        return f"http://{self.server.host}:{self.server.port}/"

    async def test_async_requests_run_in_parallel(self) -> None:
        """10 запросов по 1s — параллельно должны занять ~1s, не 10s."""
        start = time.perf_counter()
        responses = await async_requests([self.url] * 10)
        elapsed = time.perf_counter() - start
        assert responses == ["OK"] * 10
        assert elapsed <= 1.5, f"async должен быть параллельным, а занял {elapsed:.2f}s"

    async def test_threaded_requests_run_in_parallel(self) -> None:
        """То же, но через threads+requests."""
        start = time.perf_counter()
        responses = await asyncio.to_thread(partial(threaded_requests, [self.url] * 10))
        elapsed = time.perf_counter() - start
        assert responses == ["OK"] * 10
        assert elapsed <= 1.5, f"threaded должен быть параллельным, а занял {elapsed:.2f}s"
