from fastapi import APIRouter, HTTPException, status, Response, Request
from typing import Sequence
from pydantic import BaseModel
from models.users import UserModel
from dependencies import UserServiceDepend
from errors import UserNotFoundError


class CreateUserInDto(BaseModel):
    name: str
    password: str
    email: str


class LoginUserInDto(BaseModel):
    name: str
    password: str



router = APIRouter()
root_router = APIRouter()

def _get_user_id_from_cookie(request: Request) -> int:
    try:
        return int(request.cookies.get('x-user-id', ''))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized',
        )


@router.get('/', status_code=status.HTTP_200_OK)
async def get_many(user_service: UserServiceDepend) -> Sequence[UserModel]:
    return await user_service.get_many()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def register(data: CreateUserInDto, user_service: UserServiceDepend) -> UserModel:
    return await user_service.register(dict(data))


@router.get('/{user_id}')
async def get(user_id: int, user_service: UserServiceDepend) -> UserModel:
    try:
        return await user_service.get(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пользователь {user_id} не найден',
        )

@router.get('/current/')
async def get_current(request: Request, user_service: UserServiceDepend) -> UserModel:
    user_id = _get_user_id_from_cookie(request)

    try:
        return await user_service.get(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пользователь {user_id} не найден',
        )


@router.patch('/deactivate/{user_id}')
async def deactivate(user_id: int, request: Request, user_service: UserServiceDepend) -> UserModel:
    if user_id != _get_user_id_from_cookie(request):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Можно изменять только своего пользователя',
        )

    try:
        return await user_service.deactivate(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пользователь {user_id} не найден',
        )


@router.delete('/{user_id}')
async def delete(user_id: int, request: Request, user_service: UserServiceDepend) -> UserModel:
    if user_id != _get_user_id_from_cookie(request):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Можно удалять только своего пользователя',
        )

    try:
        return await user_service.delete(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пользователь {user_id} не найден',
        )


@root_router.post('/login')
async def login(
    dto: LoginUserInDto,
    response: Response,
    user_service: UserServiceDepend,
) -> UserModel:
    try:
        user = await user_service.login(dto.name, dto.password)

        response.set_cookie(
            key="x-user-id",
            value=str(user.id),
        )

        return user
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Логин или пароль не верны',
        )
