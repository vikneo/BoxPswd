from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Хеширование пароля"""
    return hasher.hash(password)


def is_valid_hash(hash_pswd: str, password: str) -> bool:
    try:
        return hasher.verify(hash_pswd, password)
    except VerifyMismatchError as err:
        print(err)
        return False
