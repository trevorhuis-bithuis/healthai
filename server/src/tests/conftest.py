from datetime import datetime
import pytest
import shortuuid

from src.app import create_app
from src.db import redis_client


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def test_redis():
    yield redis_client
    redis_client.flushall()


@pytest.fixture(scope="function")
def add_user():
    def _add_user(email):
        user = {
            "id": shortuuid.uuid(),
            "email": email,
            "created_date": datetime.utcnow().isoformat(),
            "chats": [],
        }
        redis_client.json().set(f"users:{email}", "$", user)
        return user

    return _add_user
