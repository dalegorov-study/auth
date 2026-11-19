from dataclasses import dataclass

from models.profiles import (
    UserProfileCustomizationModel,
    UserProfileModel,
    UserProfilePersonDetailsModel,
)
from repositories.profiles import UserProfileRepository


@dataclass(frozen=True)
class UserProfileService:
    profile_repository: UserProfileRepository = UserProfileRepository()

    async def get(self, user_id: int) -> UserProfileModel:
        return await self.profile_repository.get(user_id)

    async def update(
        self,
        user_id: int,
        customization: UserProfileCustomizationModel,
        personDetails: UserProfilePersonDetailsModel,
    ) -> UserProfileModel:
        return await self.profile_repository.update(
            user_id=user_id,
            customization=customization,
            personDetails=personDetails,
        )

    async def delete(self, user_id: int) -> None:
        await self.profile_repository.delete(user_id)
