import json
import os

CACHE_DIR = "../cache"

def get_cached_result(key: str) -> dict | None:
    """
    Tries to retrieve a result from the cache.
    """
    filepath: str = os.path.join(CACHE_DIR, f"{key}.json")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    elif not os.path.exists(filepath):
        return None
    else:
        return None

def cache_result(key: str, result: dict) -> None:
    """
    Stores a result in the cache.
    """
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    filepath: str = os.path.join(CACHE_DIR, f"{key}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f)