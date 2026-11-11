"""Скачать N URL-ов двумя способами: async + threads. См. README.md."""

import aiohttp
import asyncio

URLS = []

async def async_fetch(session, url) -> dict:
    async with session.post(url=url) as response:
        return await response.json()

async def f(i: int):
    await asyncio.sleep(i)
    return i


async def async_requests(session, urls):
    tasks = [async_fetch(session, url) for url in urls]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    return results


def sync_fetch(session, url):
    import requests

    return requests.post(session, url)


def threaded_requests(urls):
    ...


if __name__ == '__main__':
    async with aiohttp.ClientSession() as session:
        results = await async_requests(session, URLS)

    