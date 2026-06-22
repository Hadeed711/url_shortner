import pytest
import fakeredis
from app import app as flask_app
import app as app_module

@pytest.fixture
def fake_redis():
    """
    A fresh fake Redis instance for each test.
    Resets automatically after each test — no leftover data.
    """
    return fakeredis.FakeRedis(decode_responses=True)


@pytest.fixture
def client(fake_redis):
    """
    A Flask test client wired to fake Redis.
    Lets us make HTTP requests without starting a real server.
    """
    # Swap the real Redis connection in app.py with our fake one
    app_module.r = fake_redis

    flask_app.config["TESTING"] = True

    with flask_app.test_client() as client:
        yield client