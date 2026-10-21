from typing import Annotated

from fastapi import Depends

from services.users import UserService


def user_service() -> UserService:
    return UserService()


UserServiceDepend = Annotated[UserService, Depends(user_service)]
