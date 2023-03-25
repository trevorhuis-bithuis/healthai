from src.db import redis_client


def get_user(email):
    user = redis_client.json().get(f"users:{email}")
    return user


def set_user(email, user_obj):
    redis_client.json().set(f"users:{email}", "$", user_obj)
    return user_obj


def delete_user(email):
    user = redis_client.delete(f"users:{email}")
    return user
