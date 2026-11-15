from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from dependencies import (
    UserManagementServiceDepend,
    CurrentUserDepend,
)
from errors import UserInactiveError, UserProfileNotFoundError
from models.profiles import (
    UserProfileCustomizationModel,
    UserProfileModel,
    UserProfilePersonDetailsModel,
)
from models.users import UserModel


class UpdateUserProfileInDto(BaseModel):
    customization: UserProfileCustomizationModel
    personDetails: UserProfilePersonDetailsModel


router = APIRouter()


@router.get('/')
async def get_profile(current_user: CurrentUserDepend) -> UserModel:
    return current_user


@router.get('/details')
async def get_profile_details(
    current_user: CurrentUserDepend,
    user_management_service: UserManagementServiceDepend,
) -> UserProfileModel:
    try:
        return await user_management_service.get_profile(current_user)
    except UserProfileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Профиль пользователя не найден',
        )
    except UserInactiveError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Пользователь неактивен',
        )


@router.put('/details')
async def update_profile_details(
    data: UpdateUserProfileInDto,
    current_user: CurrentUserDepend,
    user_management_service: UserManagementServiceDepend,
) -> UserProfileModel:
    try:
        return await user_management_service.update_profile(
            user=current_user,
            customization=data.customization,
            personDetails=data.personDetails,
        )
    except UserInactiveError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Пользователь неактивен',
        )
