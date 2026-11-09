from http import HTTPStatus
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app
from services.users import UserService


@pytest.mark.integration
@pytest.mark.parametrize('error_type', [Exception, ConnectionError])
def test_unexpected_error_returns_json(error_type):
    error = error_type('Internal database connection details')
    with patch.object(UserService, 'get_many', AsyncMock(side_effect=error)):
        with TestClient(app, raise_server_exceptions=False) as client:
            response = client.get('/users/')

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json() == {
        'detail': 'Внутренняя ошибка сервера. Попробуйте повторить запрос позже.',
    }
    assert str(error) not in response.text
