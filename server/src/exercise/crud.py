from src.db import redis_client

from src.users.crud import get_user, set_user


def get_workout(workout_id):
    workout = redis_client.json().get(f"workouts:{workout_id}")
    return workout


def set_workout(workout_obj):
    redis_client.json().set(f"workouts:{workout_obj['id']}", "$", workout_obj)
    return workout_obj


def add_workout_to_user(email, workout_id):
    user = get_user(email)
    user["workouts"].append(workout_id)
    set_user(email, user)


def get_user_workouts(workout_ids):
    workouts = []
    for workout_id in workout_ids:
        workout = get_workout(workout_id)
        workouts.append(workout)
    return workouts
