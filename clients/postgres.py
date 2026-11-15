import asyncpg
from typing import AsyncGenerator
from contextlib import asynccontextmanager

import settings


@asynccontextmanager
async def get_pg_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    # TODO: 1. При каждом обращении к БД создается новое соединение
    # TODO: 2. Не учитывается работа в транзакции

    connection: asyncpg.Connection = await asyncpg.connect(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DATABASE,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
    )

    try:
        yield connection
    finally:
        await connection.close()
