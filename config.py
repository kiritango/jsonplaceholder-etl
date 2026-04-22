import os
from dataclasses import dataclass


@dataclass
class Config:
    db_path: str = os.getenv("DB_PATH", "data.db")
    base_url: str = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
    timeout: int = int(os.getenv("REQUEST_TIMEOUT", "10"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    max_retries: int = int(os.getenv("MAX_RETRIES", "3"))


config = Config()