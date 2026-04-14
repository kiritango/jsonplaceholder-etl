import logging
from fetcher import fetch_all
from db import get_connection, init_db, upsert_users, upsert_posts, upsert_comments

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

def main():
    log.info("Fetching data from API...")
    data = fetch_all()
    log.info(f"Fetched: {len(data['users'])} users, {len(data['posts'])} posts, {len(data['comments'])} comments")

    conn = get_connection()
    try:
        init_db(conn)
        log.info("DB initialized")

        upsert_users(conn, data["users"])
        log.info("Users saved")

        upsert_posts(conn, data["posts"])
        log.info("Posts saved")

        upsert_comments(conn, data["comments"])
        log.info("Comments saved")

        log.info("Done!")
    finally:
        conn.close()

if __name__ == "__main__":
    main()