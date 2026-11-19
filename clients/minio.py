from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import AsyncGenerator

from aiobotocore.client import AioBaseClient
from aiobotocore.config import AioConfig
from aiobotocore.session import get_session
from botocore.exceptions import ClientError

import settings


@asynccontextmanager
async def get_minio_client() -> AsyncGenerator[AioBaseClient, None]:
    session = get_session()
    async with session.create_client(
        's3',
        endpoint_url=settings.MINIO_ENDPOINT_URL,
        region_name='us-east-1',
        aws_access_key_id=settings.MINIO_ROOT_USER,
        aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
        config=AioConfig(s3={'addressing_style': 'path'}),
    ) as client:
        yield client


async def ensure_minio_bucket() -> None:
    bucket = settings.MINIO_BUCKET
    async with get_minio_client() as client:
        try:
            await client.head_bucket(Bucket=bucket)
        except ClientError as exc:
            if exc.response['ResponseMetadata']['HTTPStatusCode'] != HTTPStatus.NOT_FOUND:
                raise

            try:
                await client.create_bucket(Bucket=bucket)
            except client.exceptions.BucketAlreadyOwnedByYou:
                pass
