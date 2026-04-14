# JSONPlaceholder ETL

Скрипт загружает данные из [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com)
(users, posts, comments) и сохраняет их в локальную БД SQLite.
Повторный запуск безопасен — данные обновляются, дубли не создаются.

## Требования

- Python 3.10+

## Установка

```bash
git clone https://github.com/kiritango/jsonplaceholder-etl.git
cd jsonplaceholder-etl
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

После запуска появится файл `data.db` с тремя таблицами: `users`, `posts`, `comments`.

## Проверка БД

```bash
sqlite3 data.db "SELECT COUNT(*) FROM users;"
sqlite3 data.db "SELECT COUNT(*) FROM posts;"
sqlite3 data.db "SELECT COUNT(*) FROM comments;"
```