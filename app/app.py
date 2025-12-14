from typing import Any, Optional

from sqlalchemy import engine, exc, inspect, orm

from .config import _engine, _session
from .encrypt import hash_password
from .models import Base, User


class CreateApp:

    def __init__(
        self,
        engin: engine.base.Engine = _engine,
        sess: orm.session.Session = _session,
    ) -> None:
        self.engine = engin
        self.session = sess

    table_name = inspect(_engine).get_table_names()
    if not table_name:
        Base.metadata.create_all(_engine)

    def created_user(self, data_user: dict) -> None:
        password = data_user.get("password")
        if not password:
            raise ValueError("Пароль должен быть не пустой")

        hash_p = hash_password(password)
        with self.session as session:
            try:
                new_user = User(
                    last_name=data_user.get("last_name"),
                    first_name=data_user.get("first_name"),
                    login=data_user.get("login"),
                    password=hash_p,
                )
                session.add(new_user)
                session.commit()
            except exc.IntegrityError:
                print(f"Пользователь с логином {data_user.get('login')} - Существует!")

    def read_user(self, login: str) -> Optional[User | Any]:
        with self.session as session:
            try:
                return session.query(User).filter(User.login == login).scalar()
            except AttributeError as err:
                raise
                print(err)


create_app = CreateApp()

if __name__ == "__main__":
    data = {
        "first_name": "",
        "last_name": "",
        "login": "chens",
        "password": "qwe123",
    }
    create_app.created_user(data)
    _user = create_app.read_user("chens")
    print(_user)
