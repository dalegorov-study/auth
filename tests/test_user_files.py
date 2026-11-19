from asyncio import gather
from http import HTTPStatus
from typing import Any, Mapping

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from main import app


pytestmark = [
    pytest.mark.integration,
    pytest.mark.parametrize('name', ['Иванов И.И.']),
    pytest.mark.parametrize('password', ['qwerty']),
]


def test_create_list_and_delete_user_file(
    app_client: TestClient, some_user: Mapping[str, Any],
):
    headers = {'Cookie': f'x-user-id={some_user["id"]}'}
    filename = 'settings.json'
    files_url = '/profile/files'

    response = app_client.post(
        files_url, json={'filename': filename, 'data': {'theme': 'dark'}}, headers=headers,
    )
    assert response.status_code == HTTPStatus.CREATED

    response = app_client.get(files_url, headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert filename in response.json()

    response = app_client.delete(f'{files_url}/{filename}', headers=headers)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = app_client.get(files_url, headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert filename not in response.json()
