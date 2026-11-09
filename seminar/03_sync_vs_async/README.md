# sync_vs_async — параллельные HTTP-запросы: aiohttp vs threads+requests

## Условие

Скачать список URL-ов двумя способами:

1. **Async** — через `aiohttp` + `asyncio.gather`:
   - `async_fetch(session, url) -> str` — один запрос.
   - `async_requests(urls) -> list[str]` — весь список через один
     `ClientSession`, параллельно.

2. **Threads+Sync** — через `requests` + `ThreadPoolExecutor`:
   - `sync_fetch(session, url) -> str` — один запрос.
   - `threaded_requests(urls) -> list[str]` — весь список через
     `ThreadPoolExecutor` (один `requests.Session`).

## Подсказки

- Для async — смотри в сторону `asyncio.gather` и `aiohttp`.
- Для sync — `concurrent.futures.ThreadPoolExecutor` и `requests`.

## Как проверить локально (из папки задачи)

```bash
pytest
ruff check .
mypy --strict .
```

Тестовый HTTP-сервер поднимается через `aiohttp.test_utils.AioHTTPTestCase`
— в реальный интернет не ходим.

## Материалы

- [aiohttp docs](https://docs.aiohttp.org/en/stable/)
- [asyncio.gather](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather)
- [concurrent.futures.ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html)
