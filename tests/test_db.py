import sqlite3
import pytest
from db import init_db, upsert_users, upsert_posts, upsert_comments

USERS = [
    {
        "id": 1, "name": "Ivan", "username": "ivan", "email": "i@i.ru",
        "phone": "123", "website": "i.ru",
        "company": {"name": "Co"},
        "address": {"street": "Lenina 1", "city": "Moscow"},
    }
]
POSTS = [{"id": 1, "userId": 1, "title": "Title", "body": "Body"}]
COMMENTS = [{"id": 1, "postId": 1, "name": "Name", "email": "e@e.ru", "body": "Body"}]


@pytest.fixture
def conn():
    """In-memory SQLite — изолированная БД для каждого теста."""
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    init_db(connection)
    yield connection
    connection.close()


class TestUpsertUsers:
    def test_inserts_user(self, conn):
        upsert_users(conn, USERS)
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        assert count == 1

    def test_no_duplicates_on_repeat(self, conn):
        upsert_users(conn, USERS)
        upsert_users(conn, USERS)
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        assert count == 1

    def test_updates_on_conflict(self, conn):
        upsert_users(conn, USERS)
        updated = [{**USERS[0], "name": "Petr"}]
        upsert_users(conn, updated)
        name = conn.execute("SELECT name FROM users WHERE id=1").fetchone()[0]
        assert name == "Petr"


class TestUpsertPosts:
    def test_inserts_post(self, conn):
        upsert_users(conn, USERS)
        upsert_posts(conn, POSTS)
        count = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        assert count == 1

    def test_no_duplicates_on_repeat(self, conn):
        upsert_users(conn, USERS)
        upsert_posts(conn, POSTS)
        upsert_posts(conn, POSTS)
        count = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        assert count == 1


class TestUpsertComments:
    def test_inserts_comment(self, conn):
        upsert_users(conn, USERS)
        upsert_posts(conn, POSTS)
        upsert_comments(conn, COMMENTS)
        count = conn.execute("SELECT COUNT(*) FROM comments").fetchone()[0]
        assert count == 1

    def test_no_duplicates_on_repeat(self, conn):
        upsert_users(conn, USERS)
        upsert_posts(conn, POSTS)
        upsert_comments(conn, COMMENTS)
        upsert_comments(conn, COMMENTS)
        count = conn.execute("SELECT COUNT(*) FROM comments").fetchone()[0]
        assert count == 1
