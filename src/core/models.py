from typing import Any
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr


class OptionChoice(Enum):
    SOCIAL_GROUPS = 1
    AD_COMPANY = 2


class TrackableMixin:
    created_at = sa.Column(sa.DateTime, default=func.now())
    # updated_at = sa.Column(sa.DateTime, default=func.now())


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__.lower()
        if name.endswith('y'):
            return name[:-1] + 'ies'

        return name + 's'
