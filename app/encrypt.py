from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Хеширование пароля перед сохранением в БД

    :param password: Вводимый пароль пользователем;
    :type password: str
    :return: Возвращает хешированный пароль для сохранения в БД
    :rtype: str
    """
    return hasher.hash(password)


def is_valid_hash(hash_pswd: str, password: str) -> bool:
    """
    Проверка на сравнение вводимого пароля и сохраненного в хеше

    :param hash_pswd: хешированный пароль в БД;
    :type hash_pswd: str
    :param password: Вводимы пароль пользователем;
    :type password: str
    :return: Возвращает True или False;
    :rtype: bool
    """
    try:
        return hasher.verify(hash_pswd, password)
    except VerifyMismatchError as err:
        print(err)
        return False
