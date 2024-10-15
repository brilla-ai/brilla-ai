from datetime import datetime, date, time, timedelta
from decimal import Decimal
from typing import Type, Optional, List
from uuid import UUID

from sqlalchemy import (
    String,
    Date,
    DateTime,
    Time,
    Integer,
    Numeric,
    Float,
    LargeBinary,
    Boolean,
    JSON,
    Uuid,
)
from sqlalchemy.sql.type_api import TypeEngine

from sqlalchemy_orm.utils import get_all_subclasses


class TypeFactory:
    def __init__(self, type_map=None):
        pass

    def to_type(self, python_type: Type) -> Optional[Type[TypeEngine]]:
        pass


class TypeMapper:
    def __init__(self, type_map=None, types=None):
        if not types:
            types = []

        overriding_types = [*types]

        if not type_map:
            type_map = {}

        self.type_map = {
            str: String(),
            datetime: DateTime(),
            date: Date(),
            time: Time(),
            timedelta: DateTime(),
            int: Integer(),
            Decimal: Numeric(),
            float: Float(),
            bytes: LargeBinary(),
            bool: Boolean(),
            dict: JSON(),
            list: JSON(),
            UUID: Uuid(),
            **type_map,
        }
        self.type_factories: List[TypeFactory] = []
        _types = types + get_all_subclasses(TypeEngine)

        for type_ in _types:
            origin = type_
            if issubclass(type_, TypeFactory):
                self.type_factories.append(type_(type_map=self))
                continue

            try:
                if callable(type_):
                    type_obj = type_()
                else:
                    type_obj = type_

                if not hasattr(type_obj, "__visit_name__"):
                    continue

                python_type = type_obj.python_type

            except (NotImplementedError, AssertionError, TypeError):
                if type_ in types:
                    raise TypeError(
                        f"Custom type '{type}' did not specify a Python type"
                    )
            except Exception:
                pass
            else:
                if (
                    python_type not in self.type_map.keys()
                    or issubclass(self.type_map[python_type].__class__, type_)
                ) or type_ in overriding_types:
                    type_obj.origin = origin
                    self.type_map[python_type] = type_obj
                elif type_obj in self.type_map.values():
                    raise TypeError(
                        f"Types must be consistently mapped in both "
                        f"directions, '{type}' already mapped."
                    )

        self.type_map.update(type_map)

    def to_type(self, python_type: Type) -> Optional[Type[TypeEngine]]:
        column_type = self.type_map.get(python_type)

        if column_type is not None:
            return column_type

        for type_factory in self.type_factories:
            column_type = type_factory.to_type(python_type=python_type)
            if column_type:
                self.type_map[python_type] = column_type
                return column_type


default_type_mapper = TypeMapper()
