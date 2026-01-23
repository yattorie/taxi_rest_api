# Taxi REST API

REST API для сервиса заказа такси, разработанный на Django и Django REST Framework.
Проект реализует регистрацию и аутентификацию пользователей, подтверждение email,
управление профилями и работу с заказами.

---

## Содержание

- Технологии
- Начало работы
- Запуск проекта
- Структура проекта
- Использование
- Документация API
- Тестирование
- Автор

---

## Технологии

- Python 3.12
- Django
- Django REST Framework
- Djoser
- Simple JWT
- PostgreSQL
- Docker
- Docker Compose
- drf-spectacular
- pytest

---

## Начало работы

### Предварительные требования

Для установки и запуска проекта необходимы:

- Docker
- Docker Compose

---

## Запуск проекта

1. Клонируйте репозиторий и перейдите в его директорию:

git clone https://github.com/yattorie/taxi_rest_api.git  
cd taxi_rest_api

2. Создайте файл окружения:

cp .env.example .env

3. При необходимости отредактируйте файл .env, указав свои значения переменных окружения.

4. Соберите и запустите контейнеры:

docker compose up --build

После успешного запуска приложение будет доступно по адресу:

http://localhost:8000

---

## Структура проекта

taxi_rest_api/  
├── apps/  
│   ├── accounts/          # Аутентификация и пользователи  
│   └── orders/            # Работа с заказами такси  
├── taxi_project/          # Основные настройки Django-проекта  
├── .env.example           # Пример переменных окружения  
├── docker-compose.yml     # Docker Compose конфигурация  
├── Dockerfile             # Docker образ приложения  
├── manage.py  
├── conftest.py
├── requirements.txt  
└── pytest.ini             # Конфигурация тестов  

---

## Использование

Все эндпоинты аутентификации доступны по префиксу:

/api/v1/auth/

### Основные эндпоинты

POST /api/v1/auth/register/  
Регистрация нового пользователя

POST /api/v1/auth/login/  
Получение JWT токенов (access / refresh)

POST /api/v1/auth/verify-email/  
Подтверждение email адреса по коду

POST /api/v1/auth/token/refresh/  
Обновление access токена

POST /api/v1/auth/token/verify/  
Проверка валидности токена

GET /api/v1/auth/users/me/  
Получение профиля текущего пользователя

!Пользователь не может авторизоваться без подтверждения по почте!

Активация аккаунта происходит после подтверждения email.

---

## Документация API

После запуска проекта документация доступна по адресам:

Swagger UI:  
http://localhost:8000/api/docs/swagger/

ReDoc:  
http://localhost:8000/api/docs/redoc/

OpenAPI Schema:  
http://localhost:8000/api/schema/

---

## Тестирование

Проект покрыт тестами с использованием pytest.

Для запуска тестов выполните команду:

pytest

---

## Автор

Andrew (yattorie) — Backend Developer  
GitHub: https://github.com/yattorie
