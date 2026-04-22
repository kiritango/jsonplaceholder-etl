import logging
import sys
from config import config
from fetcher import fetch_all
from validator import validate_and_filter, validate_user, validate_post, validate_comment
from db import get_connection, init_db, upsert_users, upsert_posts, upsert_comments

logging.basicConfig(
    level=config.log_level,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
log = logging.getLogger(__name__)


def run_pipeline() -> None:
    log.info("Pipeline started")

    # 1. Загрузка данных из API
    log.info("Fetching data from API...")
    data = fetch_all()
    log.info(
        f"Fetched: {len(data['users'])} users, "
        f"{len(data['posts'])} posts, "
        f"{len(data['comments'])} comments"
    )

    # 2. Валидация
    users    = validate_and_filter(data["users"],    validate_user,    "users")
    posts    = validate_and_filter(data["posts"],    validate_post,    "posts")
    comments = validate_and_filter(data["comments"], validate_comment, "comments")

    # 3. Сохранение в БД — всё в одной транзакции
    conn = get_connection()
    try:
        init_db(conn)
        log.info("DB initialized")

        with conn:  # commit при успехе, rollback при исключении
            upsert_users(conn, users)
            upsert_posts(conn, posts)
            upsert_comments(conn, comments)

        log.info("Pipeline finished successfully")
    except Exception as e:
        log.error(f"Pipeline failed: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception:
        sys.exit(1)