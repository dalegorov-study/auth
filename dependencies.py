from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from errors import UserNotFoundError
from helpers import get_user_id_from_cookie
from models.users import UserModel
from services.users import UserService
from services.user_management import UserManagementService


def user_service() -> UserService:
    return UserService()


def user_management_service() -> UserManagementService:
    return UserManagementService()




UserServiceDepend = Annotated[UserService, Depends(user_service)]
UserManagementServiceDepend = Annotated[UserManagementService, Depends(user_management_service)]


async def get_current_user(request: Request, user_service: UserServiceDepend) -> UserModel:
    user_id = get_user_id_from_cookie(request)

    try:
        return await user_service.get(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пользователь {user_id} не найден',
        )


CurrentUserDepend = Annotated[UserModel, Depends(get_current_user)]
