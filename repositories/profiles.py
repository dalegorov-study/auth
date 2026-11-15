from dataclasses import dataclass
from typing import Any, Mapping

from pymongo import ReturnDocument

from clients.mongo import (
    UserProfileCustomization,
    UserProfileDocument,
    UserProfilePersonDetails,
    get_mongo_database,
)
from errors import UserProfileNotFoundError
from models.profiles import (
    UserProfileCustomizationModel,
    UserProfileModel,
    UserProfilePersonDetailsModel,
)


@dataclass(frozen=True)
class UserProfileMongoStorage:
    async def select(self, user_id: int) -> Mapping[str, Any]:
        async with get_mongo_database() as database:
            profile = await database.user_profiles.find_one(
                filter={'_id': user_id},
            )

        if profile is None:
            raise UserProfileNotFoundError()

        return self._build_profile_data(profile)

    async def update(
        self,
        user_id: int,
        customization: UserProfileCustomizationModel,
        personDetails: UserProfilePersonDetailsModel,
    ) -> Mapping[str, Any]:
        profile = UserProfileDocument(
            _id=user_id,
            customization=UserProfileCustomization(
                theme=customization.theme,
                language=customization.language,
            ),
            personDetails=UserProfilePersonDetails(
                biography=personDetails.biography,
                interests=personDetails.interests,
                contacts=personDetails.contacts,
            ),
        )

        async with get_mongo_database() as database:
            # ID пользователя служит уникальным ключом его профиля.
            updated_profile = await database.user_profiles.find_one_and_replace(
                filter={'_id': user_id},
                replacement=profile,
                return_document=ReturnDocument.AFTER,

                # создаст новую запись, если ее не было
                upsert=True,
            )

        assert updated_profile is not None
        return self._build_profile_data(updated_profile)

    async def delete(self, user_id: int) -> None:
        async with get_mongo_database() as database:
            await database.user_profiles.delete_one(filter={'_id': user_id})

    def _build_profile_data(self, document: UserProfileDocument) -> Mapping[str, Any]:
        return {
            'user_id': document['_id'],
            'customization': document['customization'],
            'personDetails': document['personDetails'],
        }


@dataclass(frozen=True)
class UserProfileRepository:
    profile_storage: UserProfileMongoStorage = UserProfileMongoStorage()

    async def get(self, user_id: int) -> UserProfileModel:
        profile_data = await self.profile_storage.select(user_id)
        return UserProfileModel(**profile_data)

    async def update(
        self,
        user_id: int,
        customization: UserProfileCustomizationModel,
        personDetails: UserProfilePersonDetailsModel,
    ) -> UserProfileModel:
        profile_data = await self.profile_storage.update(
            user_id=user_id,
            customization=customization,
            personDetails=personDetails,
        )
        return UserProfileModel(**profile_data)

    async def delete(self, user_id: int) -> None:
        await self.profile_storage.delete(user_id)
