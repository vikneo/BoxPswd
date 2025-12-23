from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import session, sessionmaker

from .settings import Settings

dir_db = "database"
BASE_DIR = Path(__file__).parent.parent / dir_db
BASE_DIR.mkdir(exist_ok=True, parents=True)
BASE_URI = BASE_DIR / str(Settings.DB_NAME)

eng: Engine = create_engine(f"{Settings.DB_HOST}:///{BASE_URI}")

Session = sessionmaker(bind=eng)
ses: session.Session = Session()

navbar_list = ["Сайт", "Логин", "Пароль", "Телефон", "Пинкод"]
