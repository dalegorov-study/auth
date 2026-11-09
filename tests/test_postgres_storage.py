from contextlib import suppress
from uuid import uuid4

import pytest

from errors import UserEmailAlreadyExistsError, UserNotFoundError
from repositories.users import UserPostgresStorage

pytestmark = [pytest.mark.integration, pytest.mark.anyio]


@pytest.fixture
def postgres_storage() -> UserPostgresStorage:
    return UserPostgresStorage()


@pytest.fixture
async def stored_user(postgres_storage: UserPostgresStorage, name: str, password: str):
    email = f'{uuid4().hex}@example.com'
    user = await postgres_storage.insert(name, password, email)
    yield user
    with suppress(UserNotFoundError):
        await postgres_storage.delete(user['id'])


@pytest.mark.parametrize('name,password', [
    ('Иванов И.И.', 'secret'),
    ('Петров П.П.', "p'assword"),
])
async def test_insert_and_select(postgres_storage, stored_user, name, password):
    assert type(stored_user['id']) is int
    assert stored_user['id'] > 0
    assert stored_user['name'] == name
    assert stored_user['password'] == password
    assert stored_user['is_active'] is True
    assert await postgres_storage.select(stored_user['id']) == stored_user


@pytest.mark.parametrize('name,password', [('Иванов И.И.', 'secret')])
@pytest.mark.parametrize('updates', [
    {'name': 'Петров П.П.'},
    {'password': "new'password"},
    {'email': f'{uuid4().hex}@example.com'},
    {'is_active': False},
    {'name': 'Петров П.П.', 'is_active': False},
])
async def test_update(postgres_storage, stored_user, updates):
    expected = {**stored_user, **updates}
    assert await postgres_storage.update(stored_user['id'], **updates) == expected
    assert await postgres_storage.select(stored_user['id']) == expected


@pytest.mark.parametrize('name,password', [('Иванов И.И.', 'secret')])
async def test_delete(postgres_storage, stored_user):
    assert await postgres_storage.delete(stored_user['id']) == stored_user
    with pytest.raises(UserNotFoundError):
        await postgres_storage.select(stored_user['id'])
