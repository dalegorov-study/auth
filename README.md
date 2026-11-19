# auth
Семинарский сервис для модуля Backend-разработка

Нужны Python 3.12 и запущенный Docker с Docker Compose. Все команды выполняются из корня проекта.

## Локальное окружение

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

## Настройки

Параметры локального окружения находятся в `.env` в корне проекта.

В `.env` хранятся параметры PostgreSQL (`PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`),
MongoDB (`MONGO_HOST`, `MONGO_PORT`, `MONGO_DATABASE`, `MONGO_USER`, `MONGO_PASSWORD`, `MONGO_AUTH_DATABASE`)
и его веб-интерфейса (`MONGO_EXPRESS_PORT`, `MONGO_EXPRESS_USER`, `MONGO_EXPRESS_PASSWORD`).
Настройки MinIO используют переменные `MINIO_HOST`, `MINIO_PORT`, `MINIO_ROOT_USER`,
`MINIO_ROOT_PASSWORD`, `MINIO_BUCKET` и `MINIO_UI_PORT`.
Имена `PG*` стандартны для PostgreSQL, поэтому те же значения используются в миграциях.

Compose автоматически читает `.env`, Python-клиенты загружают его через `settings.py`.
Переменные, уже заданные в окружении, имеют приоритет.

## База данных

Запустить PostgreSQL 16 и дождаться готовности:

```sh
docker compose up -d --wait postgres
```

Параметры подключения сервиса и миграций берутся из переменных `PG*` в `.env`.
Внутри контейнера PostgreSQL слушает порт `5432`. Данные сохраняются в Docker volume `pg_data`.

## MongoDB и веб-интерфейс

Запустить MongoDB 7.0 и mongo-express:

```sh
docker compose up -d --wait mongo mongo-express
```

Веб-интерфейс доступен по адресу `http://localhost:<MONGO_EXPRESS_PORT>`. Логин и пароль заданы в `MONGO_EXPRESS_USER` и `MONGO_EXPRESS_PASSWORD`.
Для подключения к MongoDB с компьютера используйте параметры `MONGO_*` из `.env`.
Внутри сети Compose адрес MongoDB — `mongo:27017`.
Порты MongoDB и веб-интерфейса доступны только на локальном компьютере. Данные сохраняются в Docker volume `mongo_data`.
Учётные записи баз создаются при первом запуске с пустыми volumes; изменение пароля в `.env` не меняет пароль в существующей БД.

Python-сервис запускается локально, как описано ниже. Клиент MongoDB использует базу из `MONGO_DATABASE`, профили хранятся в коллекции `user_profiles`.
Доступные коллекции описаны протоколом `MongoDatabase` в `clients/mongo.py`.
Коллекция `user_profiles` имеет тип `AsyncCollection[UserProfileDocument]`; поля документа описаны через `TypedDict` рядом с протоколом в `clients/mongo.py`.

Для локального окружения используется MongoDB 7.0: MongoDB 8.0 отказывается запускаться с ядром текущей Docker VM `7.0.0-22-generic`
из-за [известной несовместимости TCMalloc с ядрами Linux 6.19–7.0.13](https://jira.mongodb.org/browse/SERVER-121912).

## MinIO и веб-интерфейс

Запустите MinIO и S3 Manager:

```sh
docker compose up -d --wait minio minio-ui
```

При первом запуске Docker собирает MinIO `RELEASE.2025-10-15T17-29-55Z` из исходников по `docker/minio/Dockerfile`.
Сборка скачивает зависимости Go и может занять несколько минут. Для повторной сборки используйте `docker compose build minio`.

S3 API доступен локально на `http://localhost:9000`, S3 Manager — на `http://localhost:9001`.
В сети Compose веб-интерфейс подключается к `minio:9000` с учебной парой `admin` / `admin123` из `.env`.
Приложение при старте проверяет бакет из `MINIO_BUCKET` и создаёт его при необходимости. Значение по умолчанию — `profile-files`.
Данные MinIO сохраняются в Docker volume `minio_data`.

Для запуска всех сервисов используйте `docker compose up -d --wait`.

## Миграции

После запуска БД применить все миграции:

```sh
dotenv run --no-override -- pgmigrate -d db -t latest migrate
```

Команда загружает переменные из `.env` и читает SQL-файлы из `db/migrations/`.
В `db/migrations.yml` строка подключения оставлена пустой: PostgreSQL использует переменные `PG*` из окружения.
Имена файлов должны иметь формат `V<версия>__<описание>.sql` с двумя подчёркиваниями, например `V001__initial.sql`.
Уже применённые миграции повторно не выполняются.

Проверить состояние миграций:

```sh
dotenv run --no-override -- pgmigrate -d db info
```

## Тесты

При активированном `.venv`, запущенных PostgreSQL, MongoDB и MinIO и применённых миграциях:

```sh
python -m pytest
```


Запустить интеграционные тесты:

```sh
python -m pytest -m integration
```

Тесты хранилища (`tests/test_postgres_storage.py`) учитывают существующих пользователей в БД.
Фикстура `stored_user` создаёт пользователя с уникальным email и удаляет его после теста, в том числе при его падении.
HTTP-тесты (`tests/test_users.py`) пока ожидают пустую таблицу `account`; запускайте их до ручного создания пользователей.
Тестовые пользователи HTTP-тестов удаляются при завершении тестов.
Отдельно запускать HTTP-сервис для тестов не нужно.
Тесты профиля (`tests/test_profiles.py`) проверяют создание, чтение, полную замену полей, удаление вместе с аккаунтом и ошибки HTTP-ручек с настоящими PostgreSQL и MongoDB.
Тесты файлов (`tests/test_user_files.py`) проверяют сохранение JSON в MinIO, обработку дубликатов, список файлов пользователя и удаление.
Тест в `tests/test_errors.py` проверяет, что ошибка удаления профиля не приводит к удалению аккаунта.

## Расширенный профиль пользователя

Аккаунты хранятся в PostgreSQL, расширенные профили — в MongoDB.
Поле `_id` документа профиля равно ID пользователя, поэтому у аккаунта может быть только один профиль.
В ответах API этот идентификатор называется `user_id`. Сторадж возвращает данные с `user_id` вместо MongoDB `_id`.
В теле `PUT` идентификатор передавать не нужно: он определяется по текущему пользователю.
При удалении аккаунта удаляется и его профиль.
Поля профиля разделены на `customization` (тема и язык) и `personDetails` (биография, интересы и контакты).
Оба раздела сохраняются в MongoDB в том же виде. Сторадж формирует MongoDB-документы для записи и возвращает обычные данные профиля.
Репозиторий создаёт из этих данных `UserProfileModel`, включая вложенные модели разделов.
MongoDB-типы используются только внутри стораджа и клиента. Сервисы и обработчики работают с моделями приложения.

Логика разделена между тремя сервисами:

- `UserService` работает только с аккаунтами через `UserRepository`.
- `UserProfileService` работает только с профилями через `UserProfileRepository`.
- `UserManagementService` вызывает оба сервиса: проверяет `is_active` перед чтением и сохранением профиля, а также управляет совместным удалением.

Зависимость `CurrentUserDepend` читает ID из cookie и получает пользователя через `UserService`.
Обработчики получают готовый `UserModel` и передают его в менеджер, поэтому повторное чтение аккаунта не требуется.
Отсутствующая или некорректная cookie даёт `401`, неизвестный пользователь — `404`.

При удалении `UserManagementService` сначала удаляет профиль и после этого аккаунт.
Отсутствие профиля не мешает удалению. Если удалить профиль не удалось, аккаунт сохраняется.
Операции в двух базах не объединены в транзакцию: если удаление аккаунта завершится ошибкой, пользователь останется без профиля, а удаление можно повторить.

Обработчики профиля находятся в отдельном роутере `routers/profile.py`, подключённом с префиксом `/profile`.

Ручки используют cookie `x-user-id`, которую устанавливает `/login`:

- `GET /profile/` — получить данные текущего аккаунта.
- `GET /profile/details` — получить расширенный профиль. Если пользователь или профиль не найден, возвращается `404`.
- `PUT /profile/details` — создать или полностью заменить расширенный профиль. Оба раздела и все пять полей внутри них обязательны:

```json
{
  "customization": {
    "theme": "dark",
    "language": "ru"
  },
  "personDetails": {
    "biography": "Изучаю backend-разработку",
    "interests": ["python", "databases"],
    "contacts": {
      "telegram": "https://t.me/example"
    }
  }
}
```

Биографию можно очистить пустой строкой, интересы — пустым массивом, контакты — пустым объектом.
Без корректной cookie ручки возвращают `401`, без обязательного поля в `PUT` — `422`.
Для неактивного пользователя (`is_active=False`) чтение и сохранение расширенного профиля возвращают `403` с сообщением «Пользователь неактивен».

## JSON-файлы пользователя

`POST /profile/files` принимает имя `filename` и значение JSON `data`. В MinIO записывается значение `data` с типом `application/json`.
Успешное создание возвращает `201` с `filename` и `object_key`. Если имя уже занято, возвращается `409`.
`GET /profile/files` возвращает массив имён файлов текущего пользователя.
`DELETE /profile/files/{filename}` возвращает `204`, в том числе если файла уже нет.
Передавайте имя файла без пути. Для неактивного аккаунта все три операции возвращают `403`.

Подставьте ID своего активного пользователя вместо `123`:

```sh
curl -X POST --cookie 'x-user-id=123' \
  -H 'Content-Type: application/json' \
  --data '{"filename":"settings.json","data":{"theme":"dark"}}' \
  http://localhost:8003/profile/files

curl --cookie 'x-user-id=123' http://localhost:8003/profile/files

curl -X DELETE --cookie 'x-user-id=123' http://localhost:8003/profile/files/settings.json
```

В S3 Manager откройте бакет `profile-files` и папку `user/123`. Ключ объекта имеет вид `user/{user_id}/{filename}`.
MinIO проверяет условие `If-None-Match: *` при записи. При конфликте сторадж поднимает `FileAlreadyExistsError`.

## Сервис

При активированном `.venv`, запущенных базах и MinIO и применённых миграциях запустить сервис на http://localhost:8003:

```sh
python main.py
```

## Остановка контейнеров

```sh
docker compose down
```

Данные PostgreSQL, MongoDB и MinIO в volumes сохраняются и будут доступны после следующего `docker compose up -d --wait`.
