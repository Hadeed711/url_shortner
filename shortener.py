import hashlib


def generate_code(long_url: str) -> str:
    """Return a 6-char alphanumeric code for a given URL."""
    hash_bytes = hashlib.md5(long_url.encode()).hexdigest()
    return hash_bytes[:6]
