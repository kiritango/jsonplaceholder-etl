import sqlite3

DB_PATH = "data.db"

CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY,
    name       TEXT,
    username   TEXT,
    email      TEXT,
    phone      TEXT,
    website    TEXT,
    company    TEXT,
    address    TEXT
);

CREATE TABLE IF NOT EXISTS posts (
    id      INTEGER PRIMARY KEY,
    user_id INTEGER,
    title   TEXT,
    body    TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS comments (
    id       INTEGER PRIMARY KEY,
    post_id  INTEGER,
    name     TEXT,
    email    TEXT,
    body     TEXT,
    FOREIGN KEY (post_id) REFERENCES posts(id)
);
"""

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(conn):
    conn.executescript(CREATE_TABLES)
    conn.commit()

def upsert_users(conn, users: list[dict]):
    rows = [
        (
            u["id"],
            u["name"],
            u["username"],
            u["email"],
            u["phone"],
            u["website"],
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
            name=excluded.name, username=excluded.username,
            email=excluded.email, phone=excluded.phone,
            website=excluded.website, company=excluded.company,
            address=excluded.address
        """,
        rows,
    )
    conn.commit()

def upsert_posts(conn, posts: list[dict]):
    rows = [(p["id"], p["userId"], p["title"], p["body"]) for p in posts]
    conn.executemany(
        """
        INSERT INTO posts (id, user_id, title, body)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            user_id=excluded.user_id, title=excluded.title, body=excluded.body
        """,
        rows,
    )
    conn.commit()

def upsert_comments(conn, comments: list[dict]):
    rows = [(c["id"], c["postId"], c["name"], c["email"], c["body"]) for c in comments]
    conn.executemany(
        """
        INSERT INTO comments (id, post_id, name, email, body)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            post_id=excluded.post_id, name=excluded.name,
            email=excluded.email, body=excluded.body
        """,
        rows,
    )
    conn.commit()