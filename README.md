# virtual_goods

## Основные фичи

- Использование атомарных транзакций
- Header с Idempotency-Key для поддержания идемпотентности
- Кэширование (Redis, TTL)
- Фоновые задачи (Celery)
- Кастомные ошибки

## Как запустить
### Клонируем репозиторий и устанавливаем зависимости
```
git clone https://github.com/darkgooddack/virtual_goods.git
cd virtual-shop
pip install -r requirements.txt
```
### Создаём файл окружения
```
cp .env.example .env
```
> **Примечание:** не забудьте заполнить `.env` перед запуском

### Запуск
```
docker-compose up --build
```
### Доступ к API
- FastAPI: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

## Технологии

- FastAPI, Python 3.11+
- PostgreSQL + SQLAlchemy / Alembic (миграции)
- Redis (кэш + брокер для Celery)
- Pydantic v2 для валидации
- Celery для фоновых задач
- Async/await для асинхронных операций

## Архитектура
- Разделение на слои: repository, service, API
- Использование Dependency Injection для сервисов и репозиториев
- Atomic transactions для финансовых операций

## TODO
- [ ] Event Sourcing: history_transactions
- [ ] Rate limiting