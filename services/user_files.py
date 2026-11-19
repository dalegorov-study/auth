import json
from dataclasses import dataclass

from pydantic import JsonValue

from errors import InvalidFileDataError
from repositories.user_files import UserFileRepository


@dataclass(frozen=True)
class UserFileService:
    file_repository: UserFileRepository = UserFileRepository()

    async def create(self, user_id: int, filename: str, data: JsonValue) -> str:
        try:
            body = json.dumps(data, allow_nan=False).encode('utf-8')
        except ValueError as exc:
            raise InvalidFileDataError() from exc
        return await self.file_repository.create(user_id, filename, body)

    async def delete(self, user_id: int, filename: str) -> None:
        await self.file_repository.delete(user_id, filename)

    async def list(self, user_id: int) -> list[str]:
        return await self.file_repository.list(user_id)
