from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, JsonValue

from dependencies import (
    UserManagementServiceDepend,
    CurrentUserDepend,
)
from errors import (
    FileAlreadyExistsError,
    InvalidFileDataError,
    UserInactiveError,
    UserProfileNotFoundError,
)
from models.profiles import (
    UserProfileCustomizationModel,
    UserProfileModel,
    UserProfilePersonDetailsModel,
)
from models.users import UserModel


class UpdateUserProfileInDto(BaseModel):
    customization: UserProfileCustomizationModel
    personDetails: UserProfilePersonDetailsModel


class CreateUserFileInDto(BaseModel):
    filename: str
    data: JsonValue


class UserFileModel(BaseModel):
    filename: str
    object_key: str


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


@router.post('/files', status_code=status.HTTP_201_CREATED)
async def create_file(
    data: CreateUserFileInDto,
    current_user: CurrentUserDepend,
    user_management_service: UserManagementServiceDepend,
) -> UserFileModel:
    try:
        object_key = await user_management_service.create_file(current_user, data.filename, data.data)
    except InvalidFileDataError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Передайте корректное значение JSON',
        ) from None
    except UserInactiveError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Пользователь неактивен',
        )
    except FileAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Файл с таким именем уже существует',
        )
    return UserFileModel(filename=data.filename, object_key=object_key)


@router.delete('/files/{filename}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    filename: str,
    current_user: CurrentUserDepend,
    user_management_service: UserManagementServiceDepend,
) -> None:
    try:
        await user_management_service.delete_file(current_user, filename)
    except UserInactiveError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Пользователь неактивен',
        )


@router.get('/files')
async def list_files(
    current_user: CurrentUserDepend,
    user_management_service: UserManagementServiceDepend,
) -> list[str]:
    try:
        return await user_management_service.list_files(current_user)
    except UserInactiveError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Пользователь неактивен',
        )
