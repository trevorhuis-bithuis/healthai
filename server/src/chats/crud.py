from src.db import redis_client
from src.users.crud import get_user, set_user


def get_chats_by_email(email):
    chat = redis_client.scan(f"chats:{email}:*")
    return chat


def get_chat(email, id):
    chat = redis_client.json().get(f"chats:{email}:{id}")
    return chat


def set_chat_by_email(email, chat_obj):
    redis_client.json().set(f"chats:{email}:{chat_obj['id']}", "$", chat_obj)
    return chat_obj


def add_chat_to_user(email, chat_id):
    user = get_user(email)
    user["chats"].append(chat_id)
    set_user(email, user)


def add_message_to_chat(email, chat_id, message):
    chat = get_chats_by_email(email, chat_id)
    chat["messages"].append(message)
    set_chat_by_email(email, chat)
