import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
URL_EXPIRY = int(os.getenv("URL_EXPIRY", 86400))  # seconds — 86400 = 1 day
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
