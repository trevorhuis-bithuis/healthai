import bcrypt

from src.users.crud import get_user


def verify_user(email, password):
    user = get_user(email)
    if user is None:
        return False
    stored_password_hash = user["password"]
    return bcrypt.checkpw(
        password.encode("utf-8"), stored_password_hash.encode("utf-8")
    )


def create_password_hash(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")
