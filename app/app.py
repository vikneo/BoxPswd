from sqlalchemy import engine, exc, inspect, orm

from .config import _engine, _session
from .encrypt import hash_password
from .models import Base, BoxPass, User


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

    def created_password(self, data_password: dict) -> None:
        with self.session as session:
            try:
                boxpswd = BoxPass(
                    link=data_password.get("link"),
                    login=data_password.get("login"),
                    password=data_password.get("password"),
                    phone=data_password.get("phone"),
                    pincode=data_password.get("pincode"),
                    user_id=data_password.get("user_id"),
                )
                session.add(boxpswd)
                session.commit()
            except exc.IntegrityError as err:
                print(err)

    def get_user(self, login: str):
        with self.session as session:
            try:
                return session.query(User).filter(User.login == login).scalar()
            except AttributeError as err:
                print(err)

    def get_items(self, login: str):
        with self.session as session:
            try:
                user = session.query(User).filter(User.login == login).first()
                if user:
                    return user.boxpasses
            except AttributeError as err:
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
    _user = create_app.get_user("chens")
    print(_user)
