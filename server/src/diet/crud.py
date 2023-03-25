from src.db import redis_client

from src.users.crud import get_user, set_user


def get_recipe(recipe_id):
    recipe = redis_client.json().get(f"recipes:{recipe_id}")
    return recipe


def set_recipe(recipe_obj):
    redis_client.json().set(f"recipes:{recipe_obj['id']}", "$", recipe_obj)
    return recipe_obj


def add_recipe_to_user(email, recipe_id):
    user = get_user(email)
    user["recipes"].append(recipe_id)
    set_user(email, user)
