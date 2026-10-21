"""Проверка ручек сервиса: .venv/bin/python check_api.py"""

import json
from uuid import uuid4

import requests


BASE_URL = 'http://localhost:8000'
TIMEOUT = 5


def check_response(response: requests.Response, expected_status: int):
    print(f'{response.request.method} {response.url} → {response.status_code}')
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    if response.status_code != expected_status:
        raise RuntimeError(
            f'Ожидался HTTP {expected_status}, получен HTTP {response.status_code}'
        )
    return response.json()


def main():
    base_url = BASE_URL.rstrip('/')

    # Уникальное имя позволяет запускать сценарий несколько раз.
    name = f'student-{uuid4().hex[:8]}'
    password = 'study-password'

    # Session автоматически сохраняет cookie после входа.
    with requests.Session() as session:
        print('\n=== 1. HEALTH: проверка доступности сервиса ===')
        check_response(session.get(f'{base_url}/', timeout=TIMEOUT), 200)

        print('\n=== 2. CREATE: регистрация пользователя ===')
        user = check_response(session.post(
            f'{base_url}/users/',
            json={'name': name, 'password': password, 'email': f'{name}@example.com'},
            timeout=TIMEOUT,
        ), 201)
        user_id = user['id']
        if type(user_id) is not int or user_id <= 0:
            raise RuntimeError('ID пользователя должен быть положительным целым числом')

        print('\n=== 3. LIST: получение списка пользователей ===')
        check_response(session.get(f'{base_url}/users/', timeout=TIMEOUT), 200)

        print('\n=== 4. READ: получение пользователя по ID ===')
        check_response(session.get(f'{base_url}/users/{user_id}', timeout=TIMEOUT), 200)

        print('\n=== 5. LOGIN: вход и сохранение cookie ===')
        check_response(session.post(
            f'{base_url}/login',
            json={'name': name, 'password': password},
            timeout=TIMEOUT,
        ), 200)
        if session.cookies.get('x-user-id') != str(user_id):
            raise RuntimeError('После входа не получена ожидаемая cookie x-user-id')

        print('\n=== 6. READ: получение текущего пользователя по cookie ===')
        current_user = check_response(
            session.get(f'{base_url}/users/current/', timeout=TIMEOUT), 200,
        )
        if current_user['id'] != user_id:
            raise RuntimeError('Сервис вернул другого текущего пользователя')

        print('\n=== 7. UPDATE: деактивация пользователя ===')
        deactivated_user = check_response(session.patch(
            f'{base_url}/users/deactivate/{user_id}', timeout=TIMEOUT,
        ), 200)
        if deactivated_user['is_active'] is not False:
            raise RuntimeError('Пользователь остался активным после деактивации')

        print('\n=== 8. DELETE: удаление пользователя ===')
        check_response(session.delete(
            f'{base_url}/users/{user_id}', timeout=TIMEOUT,
        ), 200)

        print('\n=== 9. READ: поиск удалённого пользователя, ожидаем 404 ===')
        check_response(session.get(f'{base_url}/users/{user_id}', timeout=TIMEOUT), 404)

        print('\n=== 10. VALIDATION: некорректный ID в URL, ожидаем 422 ===')
        check_response(session.get(f'{base_url}/users/not-an-integer', timeout=TIMEOUT), 422)

        print('\n=== 11. AUTH: некорректная cookie, ожидаем 401 ===')
        session.cookies.clear()
        session.cookies.set('x-user-id', 'not-an-integer')
        check_response(session.get(f'{base_url}/users/current/', timeout=TIMEOUT), 401)

    print('\nВсе 11 запросов выполнены с ожидаемыми статусами.')


if __name__ == '__main__':
    try:
        main()
    except requests.RequestException as error:
        raise SystemExit(
            f'Не удалось выполнить HTTP-запрос: {error}\n'
            'Убедитесь, что сервис запущен: .venv/bin/python main.py'
        )
    except RuntimeError as error:
        raise SystemExit(f'Проверка не пройдена: {error}')
