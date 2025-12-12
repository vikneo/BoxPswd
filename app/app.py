from argon2 import PasswordHasher

import sqlalchemy as sa

from .models import Base, User
from .config import engine, session

hasher = PasswordHasher()

class Create_app():

    def __init__(
        self,
        engin: sa.engine.base.Engine=engine,
        session: sa.orm.session.Session=session,
        hasher: PasswordHasher = hasher,
    ) -> None:
        self.engine = engin
        self.session = session
        self.hasher = hasher

    table_name = sa.inspect(engine).get_table_names()
    if not table_name:
        Base.metadata.create_all(engine)

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
        except sa.exc.IntegrityError:
            print(f"Пользователь с логином {login} - Существует!")
    
    def read_user(self):
        with self.session as _session:
            try:
                user = _session.query(User).first()
                return user
            except AttributeError as err:
                print(err)

create_app = Create_app()


if __name__ == "__main__":
    create_app.created_user("Виктор", "Мартынов", "chens", "qwerty123")
    _user = create_app.read_user()
    print(_user)