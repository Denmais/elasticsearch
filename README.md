# Запуск

Из каталога проекта:

```bash
docker compose up --build
```

Приложение: http://127.0.0.1:8000

# Тесты

```bash
docker compose --profile test run --rm test
```

В выводе должно быть `1 passed`

# API

Приложение доступно по адресу `http://127.0.0.1:8000`.

| `POST http://127.0.0.1:8000/documents` | Создаёт документ в PostgreSQL и добавляет его в Elasticsearch. 

| `GET http://127.0.0.1:8000/documents?limit=20` | Возвращает последние документы из PostgreSQL. `limit` допускает значения от 1 до 100.


| `GET http://127.0.0.1:8000/documents/search?q=тест` | Ищет документы по тексту через Elasticsearch. Пустой запрос отклоняется


| `DELETE http://127.0.0.1:8000/documents/{doc_id}` | Удаляет документ из PostgreSQL и Elasticsearch; если ID не найден, возвращает 404. |
