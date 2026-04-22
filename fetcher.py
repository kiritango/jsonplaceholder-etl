import logging
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
from config import config

log = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(config.max_retries),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    before_sleep=before_sleep_log(log, logging.WARNING),
)
def fetch(endpoint: str) -> list[dict]:
    """Загружает данные из API с автоматическим retry при ошибке."""
    url = f"{config.base_url}/{endpoint}"
    log.debug(f"GET {url}")
    response = requests.get(url, timeout=config.timeout)
    response.raise_for_status()
    return response.json()


def fetch_all() -> dict:
    """Загружает все сущности из API."""
    return {
        "users":    fetch("users"),
        "posts":    fetch("posts"),
        "comments": fetch("comments"),
    }