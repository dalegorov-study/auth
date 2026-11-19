from dataclasses import dataclass

from pydantic import JsonValue

from errors import UserInactiveError
from models.profiles import (
    UserProfileCustomizationModel,
    UserProfileModel,
    UserProfilePersonDetailsModel,
)
from models.users import UserModel
from services.profiles import UserProfileService
from services.user_files import UserFileService
from services.users import UserService


@dataclass(frozen=True)
class UserManagementService:
    user_service: UserService = UserService()
    user_profile_service: UserProfileService = UserProfileService()
    user_file_service: UserFileService = UserFileService()

    async def get_profile(self, user: UserModel) -> UserProfileModel:
        self._check_user_is_active(user)
        return await self.user_profile_service.get(user.id)

    async def update_profile(
        self,
        user: UserModel,
        customization: UserProfileCustomizationModel,
        personDetails: UserProfilePersonDetailsModel,
    ) -> UserProfileModel:
        self._check_user_is_active(user)
        return await self.user_profile_service.update(
            user_id=user.id,
            customization=customization,
            personDetails=personDetails,
        )

    async def create_file(self, user: UserModel, filename: str, data: JsonValue) -> str:
        self._check_user_is_active(user)
        return await self.user_file_service.create(user.id, filename, data)

    async def delete_file(self, user: UserModel, filename: str) -> None:
        self._check_user_is_active(user)
        await self.user_file_service.delete(user.id, filename)

    async def list_files(self, user: UserModel) -> list[str]:
        self._check_user_is_active(user)
        return await self.user_file_service.list(user.id)

    async def delete(self, user: UserModel) -> UserModel:
        await self.user_profile_service.delete(user.id)
        return await self.user_service.delete(user.id)

    def _check_user_is_active(self, user: UserModel) -> None:
        if not user.is_active:
            raise UserInactiveError()
