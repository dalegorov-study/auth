from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Protocol, TypedDict, cast

from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection

import settings


class UserProfileCustomization(TypedDict):
    theme: str
    language: str


class UserProfilePersonDetails(TypedDict):
    biography: str
    interests: list[str]
    contacts: dict[str, str]


class UserProfileDocument(TypedDict):
    _id: int
    customization: UserProfileCustomization
    personDetails: UserProfilePersonDetails


class MongoDatabase(Protocol):
    user_profiles: AsyncCollection[UserProfileDocument]


@asynccontextmanager
async def get_mongo_database() -> AsyncGenerator[MongoDatabase, None]:
    client: AsyncMongoClient[dict[str, Any]] = AsyncMongoClient(
        host=settings.MONGO_HOST,
        port=settings.MONGO_PORT,
        username=settings.MONGO_USER,
        password=settings.MONGO_PASSWORD,
        authSource=settings.MONGO_AUTH_DATABASE,
    )

    try:
        # PyMongo предоставляет коллекции динамически, протокол описывает их типы.
        yield cast(MongoDatabase, client[settings.MONGO_DATABASE])
    finally:
        await client.close()
