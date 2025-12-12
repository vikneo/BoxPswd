from argon2 import PasswordHasher
from sqlalchemy import engine, exc, inspect, orm

from .config import _engine, session
from .models import Base, User

hasher = PasswordHasher()


class CreateApp:

    def __init__(
        self,
        engin: engine.base.Engine = _engine,
        _session: orm.session.Session = session,
        _hasher: PasswordHasher = hasher,
    ) -> None:
        self.engine = engin
        self.session = _session
        self.hasher = _hasher

    table_name = inspect(_engine).get_table_names()
    if not table_name:
        Base.metadata.create_all(_engine)

    def created_user(self, last_name: str, first_name: str, login: str, pswd: str):
        pswd_hash = self.hasher.hash(pswd)
        try:
            with self.session as _session:
                new_user = User(
                    last_name=last_name,
                    first_name=first_name,
                    login=login,
                    password=pswd_hash,
                )
                _session.add(new_user)
                _session.commit()
        except exc.IntegrityError:
            print(f"Пользователь с логином {login} - Существует!")

    def read_user(self):
        with self.session as _session:
            try:
                return _session.query(User).first()
            except AttributeError as err:
                print(err)


create_app = CreateApp()

if __name__ == "__main__":
    create_app.created_user("Виктор", "Мартынов", "chens", "qwerty123")
    _user = create_app.read_user()
    print(_user)
