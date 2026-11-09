"""Скачать N URL-ов двумя способами: async + threads. См. README.md."""


async def async_fetch(session, url):
    ...


async def async_requests(urls):
    ...


def sync_fetch(session, url):
    ...


def threaded_requests(urls):
    ...
