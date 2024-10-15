from typing import Type

from sqlalchemy.orm.decl_api import declarative_base, DeclarativeMeta

from sqlalchemy_orm.base.helper import Base
from sqlalchemy_orm.typemapper import TypeMapper


class BaseDeclarativeMeta(DeclarativeMeta):
    def __init__(cls, classname, bases, dict_, **kw):
        dict_.update(cls.__dict__)
        super().__init__(classname, bases, dict_, **kw)


def base_factory(type_map: TypeMapper = None, base: Type = None) -> Type[Base]:
    if base:
        combined_base = type("Base", (base, Base), {})
    else:
        combined_base = Base

    if type_map:
        combined_base.type_mapper = type_map

    model: Type[Base] = declarative_base(
        cls=combined_base, name="Base", metaclass=BaseDeclarativeMeta
    )
    model.declarative_base = model

    return model


Model = base_factory

ModelBase = base_factory()
