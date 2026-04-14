import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def fetch(endpoint: str) -> list[dict]:
    response = requests.get(f"{BASE_URL}/{endpoint}", timeout=10)
    response.raise_for_status()
    return response.json()

def fetch_all() -> dict:
    return {
        "users":    fetch("users"),
        "posts":    fetch("posts"),
        "comments": fetch("comments"),
    }