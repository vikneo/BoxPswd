from typing import List

from sqlalchemy import event
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.mapper import Mapper

from .models import BoxPass


@event.listens_for(BoxPass, "before_insert")
def add_name_site(mapper: Mapper[BoxPass], connection: Engine, target: BoxPass):
    """
    Из ссылки на сайт выбирается домен,
    пример(
        http://domain.com,
        http://www.domain.com,
        https://domain.com,
        https://www.domain.com,
        );
    результат выборки как "domain.com" добавляется в поле "name_site" модели BoxPass
    и сохраняет в БД с заполненым полем.
    """
    site_name: List[str] = target.link.split("/")
    if target.link:
        name = site_name[2].split(".")
        target.name_site = ".".join(name[1:]) if len(name) > 2 else ".".join(name)
