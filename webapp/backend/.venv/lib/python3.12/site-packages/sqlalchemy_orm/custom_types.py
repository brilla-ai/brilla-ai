import enum
import uuid
from typing import Type, Optional

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.type_api import TypeEngine
from sqlalchemy.types import TypeDecorator, CHAR

from sqlalchemy_orm.typemapper import TypeFactory


class UUIDType(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """

    impl = CHAR
    cache_ok = True

    @property
    def python_type(self):
        return uuid.UUID

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class EnumType(TypeFactory):
    def to_type(self, python_type: Type) -> Optional[Type[TypeEngine]]:
        if issubclass(python_type, enum.Enum):

            class Enum(SQLAlchemyEnum):
                _python_type = python_type

                def __init__(self, *enums, **kw):
                    super().__init__(Enum._python_type, *enums, **kw)

            return Enum
