import uuid
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm.decl_api import declared_attr

from sqlalchemy_orm.base.helper import Base
from sqlalchemy_orm.patterns.taggable import Taggable


class TagMixin(Taggable):
    cached_tag_class = None

    @classmethod
    def tag_cls(cls):
        if cls.cached_tag_class is not None:
            return cls.cached_tag_class

        if not issubclass(cls, Base):
            raise TypeError(f"TagMixin class {cls} must be a subclass of {Base}.")

        parent_table = cls.__tablename__
        primary_key = cls.primary_keys()[0].name

        class Tag(cls.declarative_base):
            id: uuid.UUID = uuid.uuid4
            tag: str
            parent_id = mapped_column(ForeignKey(f"{parent_table}.{primary_key}"))
            parent = relationship(cls)

            __tablename__ = cls.__tablename__ + "_tag"
            __inheritance__ = False
            __parent_cls__ = cls

        Tag.__name__ = cls.__name__ + Tag.__name__
        Tag.__qualname__ = Tag.__name__
        Tag.__module__ = cls.__module__ + Tag.__module__
        cls.cached_tag_class = Tag

        return Tag

    @declared_attr
    def tag_objects(self):
        tag_class = self.tag_cls()
        return relationship(
            tag_class,
            back_populates="parent",
            cascade="all, delete, delete-orphan",
            lazy="dynamic",
        )

    @declared_attr
    def tags(self) -> List[str]:
        return association_proxy(
            "tag_objects", "tag", creator=lambda tag: self.tag_cls()(tag=tag)
        )
