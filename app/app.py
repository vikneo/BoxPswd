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

    def created_user(self, last_name: str, first_name: str, login: str, pswd: str):
        hash_p = hash_password(pswd)
        with self.session as session:
            try:
                new_user = User(
                    last_name=last_name,
                    first_name=first_name,
                    login=login,
                    password=hash_p,
                )
                session.add(new_user)
                session.commit()
            except exc.IntegrityError:
                print(f"Пользователь с логином {login} - Существует!")

    def read_user(self):
        with self.session as session:
            try:
                return session.query(User).first()
            except AttributeError as err:
                print(err)


create_app = CreateApp()

if __name__ == "__main__":
    create_app.created_user("Виктор", "Мартынов", "chens", "qwerty123")
    _user = create_app.read_user()
    print(_user)
