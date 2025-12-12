import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:

    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG")
    templates = Path(__file__).parent.parent.parent / "templates"
    static = Path(__file__).parent.parent.parent / "static"

    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_PORT")
