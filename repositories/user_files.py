from dataclasses import dataclass
from http import HTTPStatus

from botocore.exceptions import ClientError

import settings
from clients.minio import get_minio_client
from errors import FileAlreadyExistsError


@dataclass(frozen=True)
class UserFileMinioStorage:
    async def insert(self, user_id: int, filename: str, body: bytes) -> str:
        object_key = f'{self._user_prefix(user_id)}{filename}'
        async with get_minio_client() as client:
            try:
                await client.put_object(
                    Bucket=settings.MINIO_BUCKET,
                    Key=object_key,
                    Body=body,
                    ContentType='application/json',
                    IfNoneMatch='*',
                )
            except ClientError as exc:
                if exc.response['ResponseMetadata']['HTTPStatusCode'] == HTTPStatus.PRECONDITION_FAILED:
                    raise FileAlreadyExistsError(filename) from None
                raise
        return object_key

    async def delete(self, user_id: int, filename: str) -> None:
        async with get_minio_client() as client:
            await client.delete_object(
                Bucket=settings.MINIO_BUCKET,
                Key=f'{self._user_prefix(user_id)}{filename}',
            )

    async def select_many(self, user_id: int) -> list[str]:
        prefix = self._user_prefix(user_id)
        filenames = []
        async with get_minio_client() as client:
            paginator = client.get_paginator('list_objects_v2')
            async for page in paginator.paginate(Bucket=settings.MINIO_BUCKET, Prefix=prefix, Delimiter='/'):
                filenames.extend(item['Key'].removeprefix(prefix) for item in page.get('Contents', ()))
        return filenames

    @staticmethod
    def _user_prefix(user_id: int) -> str:
        return f'user/{user_id}/'


@dataclass(frozen=True)
class UserFileRepository:
    file_storage: UserFileMinioStorage = UserFileMinioStorage()

    async def create(self, user_id: int, filename: str, body: bytes) -> str:
        return await self.file_storage.insert(user_id, filename, body)

    async def delete(self, user_id: int, filename: str) -> None:
        await self.file_storage.delete(user_id, filename)

    async def list(self, user_id: int) -> list[str]:
        return await self.file_storage.select_many(user_id)
