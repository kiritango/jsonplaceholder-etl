import logging
import sqlite3
from config import config

log = logging.getLogger(__name__)

CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    username   TEXT NOT NULL,
    email      TEXT NOT NULL,
    phone      TEXT,
    website    TEXT,
    company    TEXT,
    address    TEXT
);

CREATE TABLE IF NOT EXISTS posts (
    id      INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title   TEXT NOT NULL,
    body    TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS comments (
    id       INTEGER PRIMARY KEY,
    post_id  INTEGER NOT NULL,
    name     TEXT,
    email    TEXT,
    body     TEXT,
    FOREIGN KEY (post_id) REFERENCES posts(id)
);
"""


def get_connection(db_path: str = None) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path or config.db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(CREATE_TABLES)


def _count(conn: sqlite3.Connection, table: str) -> int:
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def upsert_users(conn: sqlite3.Connection, users: list[dict]) -> None:
    before = _count(conn, "users")
    rows = [
        (
            u["id"],
            u["name"],
            u["username"],
            u["email"],
            u.get("phone"),
            u.get("website"),
            u["company"]["name"],
            f'{u["address"]["street"]}, {u["address"]["city"]}',
        )
        for u in users
    ]
    conn.executemany(
        """
        INSERT INTO users (id, name, username, email, phone, website, company, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name=excluded.name,
            username=excluded.username,
            email=excluded.email,
            phone=excluded.phone,
            website=excluded.website,
            company=excluded.company,
            address=excluded.address
        """,
        rows,
    )
    after = _count(conn, "users")
    log.info(f"users: fetched={len(users)}, before={before}, after={after}, new={after - before}")


def upsert_posts(conn: sqlite3.Connection, posts: list[dict]) -> None:
    before = _count(conn, "posts")
    rows = [(p["id"], p["userId"], p["title"], p["body"]) for p in posts]
    conn.executemany(
        """
        INSERT INTO posts (id, user_id, title, body)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            user_id=excluded.user_id,
            title=excluded.title,
            body=excluded.body
        """,
        rows,
    )
    after = _count(conn, "posts")
    log.info(f"posts: fetched={len(posts)}, before={before}, after={after}, new={after - before}")


def upsert_comments(conn: sqlite3.Connection, comments: list[dict]) -> None:
    before = _count(conn, "comments")
    rows = [(c["id"], c["postId"], c["name"], c["email"], c["body"]) for c in comments]
    conn.executemany(
        """
        INSERT INTO comments (id, post_id, name, email, body)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            post_id=excluded.post_id,
            name=excluded.name,
            email=excluded.email,
            body=excluded.body
        """,
        rows,
    )
    after = _count(conn, "comments")
    log.info(
        f"comments: fetched={len(comments)}, before={before}, after={after}, new={after - before}"
    )