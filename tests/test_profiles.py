from http import HTTPStatus
from typing import Any, Mapping
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from errors import UserProfileNotFoundError
from models.users import UserModel
from repositories.profiles import UserProfileRepository
from services.users import UserService

pytestmark = pytest.mark.integration

RAW_PROFILE_DATA = {
    'customization': {
        'theme': 'dark',
        'language': 'ru',
    },
    'personDetails': {
        'biography': 'Изучаю backend-разработку',
        'interests': ['python', 'databases'],
        'contacts': {'telegram': 'https://t.me/example'},
    },
}


@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', ['qwerty'])
def test_update_user_profile(
    app_client: TestClient,
    some_user: Mapping[str, Any],
):
    cookies = {'x-user-id': str(some_user['id'])}
    expected_profile = {'user_id': some_user['id'], **RAW_PROFILE_DATA}

    response = app_client.get('/profile/details', cookies=cookies)
    assert response.status_code == HTTPStatus.NOT_FOUND

    response = app_client.put('/profile/details', json=RAW_PROFILE_DATA, cookies=cookies)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_profile

    response = app_client.get('/profile/details', cookies=cookies)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_profile

    updated_profile = {
        'customization': {
            'theme': 'light',
            'language': 'en',
        },
        'personDetails': {
            'biography': 'Обновлённая биография',
            'interests': [],
            'contacts': {},
        },
    }
    expected_profile = {'user_id': some_user['id'], **updated_profile}
    response = app_client.put('/profile/details', json=updated_profile, cookies=cookies)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_profile

    response = app_client.get('/profile/details', cookies=cookies)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_profile

    response = app_client.get(f'/users/{some_user["id"]}')
    assert response.json() == some_user


@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', ['qwerty'])
def test_profile_reads_current_user_once(app_client: TestClient, some_user: Mapping[str, Any]):
    headers = {'Cookie': f'x-user-id={some_user["id"]}'}
    response = app_client.put('/profile/details', json=RAW_PROFILE_DATA, headers=headers)
    assert response.status_code == HTTPStatus.OK

    current_user = UserModel(**some_user)
    with patch.object(UserService, 'get', AsyncMock(return_value=current_user)) as get_user:
        response = app_client.get('/profile/details', headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'user_id': current_user.id, **RAW_PROFILE_DATA}
    get_user.assert_awaited_once_with(current_user.id)


@pytest.mark.anyio
@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', ['qwerty'])
@pytest.mark.parametrize('method', ['GET', 'PUT'])
async def test_inactive_user_cannot_access_profile(
    app_client: TestClient,
    some_user: Mapping[str, Any],
    method: str,
):
    headers = {'Cookie': f'x-user-id={some_user["id"]}'}
    response = app_client.put('/profile/details', json=RAW_PROFILE_DATA, headers=headers)
    assert response.status_code == HTTPStatus.OK

    response = app_client.patch(f'/users/deactivate/{some_user["id"]}', headers=headers)
    assert response.status_code == HTTPStatus.OK

    profile_update = {**RAW_PROFILE_DATA, 'customization': {'theme': 'light', 'language': 'en'}}
    response = app_client.request(
        method, '/profile/details', json=profile_update, headers=headers,
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()['detail'] == 'Пользователь неактивен'

    profile = await UserProfileRepository().get(some_user['id'])
    assert profile.model_dump() == {'user_id': some_user['id'], **RAW_PROFILE_DATA}


@pytest.mark.anyio
@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', ['qwerty'])
async def test_inactive_user_cannot_create_profile(
    app_client: TestClient,
    some_user: Mapping[str, Any],
):
    headers = {'Cookie': f'x-user-id={some_user["id"]}'}
    response = app_client.patch(f'/users/deactivate/{some_user["id"]}', headers=headers)
    assert response.status_code == HTTPStatus.OK

    response = app_client.put('/profile/details', json=RAW_PROFILE_DATA, headers=headers)
    assert response.status_code == HTTPStatus.FORBIDDEN

    with pytest.raises(UserProfileNotFoundError):
        await UserProfileRepository().get(some_user['id'])


@pytest.mark.anyio
@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', ['qwerty'])
async def test_delete_user_removes_profile(
    app_client: TestClient,
    some_user: Mapping[str, Any],
):
    headers = {'Cookie': f'x-user-id={some_user["id"]}'}
    response = app_client.put('/profile/details', json=RAW_PROFILE_DATA, headers=headers)
    assert response.status_code == HTTPStatus.OK

    response = app_client.delete(f'/users/{some_user["id"]}', headers=headers)
    assert response.status_code == HTTPStatus.OK

    response = app_client.get(f'/users/{some_user["id"]}')
    assert response.status_code == HTTPStatus.NOT_FOUND

    with pytest.raises(UserProfileNotFoundError):
        await UserProfileRepository().get(some_user['id'])


@pytest.mark.parametrize('method', ['GET', 'PUT'])
def test_profile_requires_existing_user(
    app_client: TestClient,
    method: str,
):
    response = app_client.request(
        method,
        '/profile/details',
        json=RAW_PROFILE_DATA,
        headers={'Cookie': 'x-user-id=0'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Пользователь 0 не найден'


@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', ['qwerty'])
@pytest.mark.parametrize(('section', 'field'), [
    ('customization', 'theme'),
    ('customization', 'language'),
    ('personDetails', 'biography'),
    ('personDetails', 'interests'),
    ('personDetails', 'contacts'),
])
def test_profile_requires_all_fields(
    app_client: TestClient,
    some_user: Mapping[str, Any],
    section: str,
    field: str,
):
    profile = {
        **RAW_PROFILE_DATA,
        section: {key: value for key, value in RAW_PROFILE_DATA[section].items() if key != field},
    }
    response = app_client.put(
        '/profile/details',
        json=profile,
        headers={'Cookie': f'x-user-id={some_user["id"]}'},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', ['qwerty'])
@pytest.mark.parametrize('section', ['customization', 'personDetails'])
def test_profile_requires_both_sections(
    app_client: TestClient,
    some_user: Mapping[str, Any],
    section: str,
):
    profile = {key: value for key, value in RAW_PROFILE_DATA.items() if key != section}
    response = app_client.put(
        '/profile/details',
        json=profile,
        headers={'Cookie': f'x-user-id={some_user["id"]}'},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
