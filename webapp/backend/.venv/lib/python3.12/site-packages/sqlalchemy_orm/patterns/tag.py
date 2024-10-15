import uuid
from typing import Type

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, validates, object_session
from sqlalchemy.orm.decl_api import declared_attr

from sqlalchemy_orm.base.helper import Base
from sqlalchemy_orm.patterns.taggable import Taggable


class TagBase(Base):
    id: uuid.UUID = uuid.uuid4
    tag: str = ""

    __inheritance__ = False
    cached_mixin = None

    @classmethod
    def mixin(cls) -> Type[Taggable]:
        if cls.cached_mixin:
            return cls.cached_mixin
        tag_cls: Type[TagBase] = cls

        class Mixin(Taggable, Base):
            cached_tag_association_cls = None

            @classmethod
            def relations(cls, checked=None):
                super_relations = super().relations(checked=checked)
                return super_relations & {cls.tag_association_cls()}

            @classmethod
            def tag_association_cls(cls):
                if cls.cached_tag_association_cls:
                    return cls.cached_tag_association_cls

                class TagAssociation(tag_cls.declarative_base):
                    id: uuid.UUID = uuid.uuid4
                    tag: tag_cls
                    parent: cls = None

                    __tablename__ = cls.__tablename__ + "_tag"
                    __inheritance__ = False

                    @declared_attr
                    def tag_str(self):
                        return association_proxy("tag", "tag")

                    @validates("tag")
                    def _validate_tag(self, key, value):
                        session = object_session(self)
                        if session is not None:
                            v = value.value
                            with session.no_autoflush:
                                uvalue = session.query(tag_cls).filter_by(tag=v).first()
                                if uvalue:
                                    session.expunge(value)
                                    return uvalue
                        return value

                tag_name = TagAssociation.__name__
                tag_module = TagAssociation.__module__

                TagAssociation.__name__ = cls.__name__ + tag_name
                TagAssociation.__module__ = cls.__module__ + tag_module

                cls.cached_tag_association_cls = TagAssociation

                return TagAssociation

            @declared_attr
            def tag_associations(self):
                return relationship(
                    self.tag_association_cls(), cascade="all, delete, delete-orphan"
                )

            @validates("tag_associations")
            def _validate_tag_associations(self, key, value):
                session = object_session(self)
                if session is not None:
                    tag = value.tag
                    with session.no_autoflush:
                        existing_tag = session.query(tag_cls).filter_by(tag=tag).first()
                        if existing_tag:
                            session.expunge(existing_tag)
                            value.tag = existing_tag
                return value

            @declared_attr
            def tags(self):
                TagAssociation = self.tag_association_cls()
                Tag: Type[TagBase] = tag_cls

                def creator(_tag):
                    # from context_helper import ctx
                    return TagAssociation(tag=Tag(tag=_tag))

                return association_proxy("tag_associations", "tag_str", creator=creator)

        cls.cached_mixin = Mixin
        return Mixin
