from typing import Any, Mapping, Generator
import pytest
from fastapi.testclient import TestClient
from main import app
from http import HTTPStatus

PASSWORD = 'qwerty'



@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', [PASSWORD])
def test_create_user(
    some_user: Mapping[str, Any],
    app_client: TestClient
):
    assert some_user['name'] == 'Иванов И.И.'
    assert type(some_user['id']) is int
    assert some_user['id'] > 0

    read_response = app_client.get(f'/users/{some_user["id"]}')
    read_user = read_response.json()

    assert read_response.status_code == HTTPStatus.OK
    assert read_user['id'] == some_user['id']
    assert read_user['name'] == some_user['name']


@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', [PASSWORD])
def test_deactivate_user(
    app_client: TestClient,
    some_user: Mapping[str, Any]
):
    update_response = app_client.patch(
        f'/users/deactivate/{some_user["id"]}',
        cookies={
            'x-user-id': str(some_user['id'])
        },
    )
    assert update_response.status_code == HTTPStatus.OK, update_response.json()

    updated_user = update_response.json()
    assert updated_user['id'] == some_user['id']
    assert not updated_user['is_active']


@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', [PASSWORD])
def test_delete_user(
    app_client: TestClient,
    some_user: Mapping[str, Any]
):
    delete_response = app_client.delete(
        f'/users/{some_user["id"]}',
        cookies={
            'x-user-id': str(some_user['id'])
        }
    )
    assert delete_response.status_code == HTTPStatus.OK, delete_response.json()

    deleted_user = delete_response.json()
    assert deleted_user['id'] == some_user['id']

    get_user = app_client.get(f'/users/{deleted_user["id"]}')
    assert get_user.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', [PASSWORD])
def test_get_many_users(
    app_client: TestClient,
    some_user: Mapping[str, Any]
):
    get_users_response = app_client.get(f'/users')
    assert get_users_response.status_code == HTTPStatus.OK

    users = get_users_response.json()
    assert len(users) == 1

    delete_response = app_client.delete(
        f'/users/{some_user["id"]}',
        cookies={
            'x-user-id': str(some_user['id'])
        },
    )
    assert delete_response.status_code == HTTPStatus.OK, delete_response.json()

    get_users_response = app_client.get(f'/users')
    assert get_users_response.status_code == HTTPStatus.OK

    users = get_users_response.json()
    assert len(users) == 0


@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', [PASSWORD])
def test_login_user(
    app_client: TestClient,
    some_user: Mapping[str, Any]
):
    login_response = app_client.post(f'/login', json=dict(
        name=some_user['name'],
        password=PASSWORD,
    ))
    assert login_response.status_code == HTTPStatus.OK
    assert login_response.cookies.get('x-user-id') == str(some_user['id'])

    logged_user = login_response.json()
    assert logged_user['id'] == some_user['id']

    current_response = app_client.get('/users/current/')
    assert current_response.status_code == HTTPStatus.OK
    assert current_response.json()['id'] == some_user['id']


@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', [PASSWORD])
def test_get_current_user(
    app_client: TestClient,
    some_user: Mapping[str, Any]
):
    get_response = app_client.get(f'/users/current/', cookies={
        'x-user-id': str(some_user['id']),
    })
    assert get_response.status_code == HTTPStatus.OK

    get_user = get_response.json()
    assert get_user['id'] == some_user['id']


def test_user_ids_are_not_reused_after_deletion(app_client: TestClient):
    user_ids = []

    def create_user(name: str) -> int:
        response = app_client.post('/users/', json={
            'name': name,
            'password': PASSWORD,
            'email': f'{name}@example.com',
        })
        assert response.status_code == HTTPStatus.CREATED
        user_id = response.json()['id']
        assert type(user_id) is int
        user_ids.append(user_id)
        return user_id

    try:
        first_id = create_user('first')
        second_id = create_user('second')
        assert second_id > first_id

        response = app_client.delete(
            f'/users/{second_id}',
            headers={'Cookie': f'x-user-id={second_id}'},
        )
        assert response.status_code == HTTPStatus.OK

        third_id = create_user('third')
        assert third_id > second_id
        response = app_client.get(f'/users/{first_id}')
        assert response.status_code == HTTPStatus.OK
        assert response.json()['name'] == 'first'

        users = app_client.get('/users/').json()
        assert {user['id'] for user in users} == {first_id, third_id}
    finally:
        for user_id in user_ids:
            app_client.delete(
                f'/users/{user_id}',
                headers={'Cookie': f'x-user-id={user_id}'},
            )


@pytest.mark.parametrize(('method', 'path'), [
    ('GET', '/users/not-an-integer'),
    ('PATCH', '/users/deactivate/not-an-integer'),
    ('DELETE', '/users/not-an-integer'),
])
def test_invalid_user_id_in_path(app_client: TestClient, method: str, path: str):
    response = app_client.request(method, path)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(('method', 'path'), [
    ('GET', '/users/current/'),
    ('PATCH', '/users/deactivate/1'),
    ('DELETE', '/users/1'),
])
@pytest.mark.parametrize('cookie', [None, '', 'not-an-integer'])
def test_invalid_user_id_in_cookie(
    app_client: TestClient, method: str, path: str, cookie: str | None,
):
    headers = {} if cookie is None else {'Cookie': f'x-user-id={cookie}'}
    response = app_client.request(method, path, headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize(('method', 'path'), [
    ('GET', '/users/0'),
    ('GET', '/users/current/'),
    ('PATCH', '/users/deactivate/0'),
    ('DELETE', '/users/0'),
])
def test_unknown_user_id(app_client: TestClient, method: str, path: str):
    response = app_client.request(method, path, headers={'Cookie': 'x-user-id=0'})
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize('name', ['Иванов И.И.'])
@pytest.mark.parametrize('password', [PASSWORD])
@pytest.mark.parametrize(('method', 'path'), [
    ('PATCH', '/users/deactivate/{user_id}'),
    ('DELETE', '/users/{user_id}'),
])
def test_user_id_must_match_cookie(
    app_client: TestClient, some_user: Mapping[str, Any], method: str, path: str,
):
    user_id = some_user['id']
    response = app_client.request(
        method,
        path.format(user_id=user_id + 1),
        headers={'Cookie': f'x-user-id={user_id}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN

    response = app_client.get(f'/users/{user_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['is_active'] is True
