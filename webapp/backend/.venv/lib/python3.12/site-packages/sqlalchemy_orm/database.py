from typing import Iterable

from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.orm import sessionmaker, RelationshipProperty
from sqlalchemy.orm.clsregistry import _ModuleMarker

from sqlalchemy_orm.base.helper import Base
from sqlalchemy_orm.query import Query
from sqlalchemy_orm.session import Session
from sqlalchemy_orm.utils import find_subclasses


class DatabaseException(BaseException):
    pass


class Database:
    def __init__(self, url, session_cls=Session, query_cls=Query):
        self.url = url
        self.engine = create_engine(url)
        self.session_maker = sessionmaker(
            class_=session_cls, bind=self.engine, query_cls=query_cls
        )
        self.declarative_base = None

    def entity_relationship_diagram(self, embed_html=True) -> str:
        """
        ERD in dot format
        """

        from sqlalchemy_orm.eralchemy.main import (
            _intermediary_to_dot,
            all_to_intermediary,
        )

        tables, relationships = all_to_intermediary(
            self.declarative_base.metadata, schema="Schema"
        )
        output = _intermediary_to_dot(tables, relationships)

        if embed_html:
            # flake8: noqa
            output = (
                """
            <!DOCTYPE html><meta charset="utf-8"><body>
            <script src="https://d3js.org/d3.v5.min.js"></script>
            <script src="https://unpkg.com/@hpcc-js/wasm@0.3.11/dist/index.min.js"></script>
            <script src="https://unpkg.com/d3-graphviz@3.0.5/build/d3-graphviz.js"></script>
            <div id="graph" style="text-align: center;"></div>
            <script>d3.select("#graph").graphviz().renderDot('DOT');</script>
            """.replace(
                    "DOT", output
                )
                .replace("\n", "")
                .replace("\r", "")
            )

        return output

    def session(self) -> Session:
        return self.session_maker()

    def create_all(self, base):
        base.metadata.create_all(bind=self.engine, checkfirst=True)
        self.declarative_base = base

    def create(self, *models, create_relations=True, create_polymorphic_parents=True):
        if create_relations:
            models_with_relations = {*models}

            for model in models:
                if issubclass(model, Base):
                    models_with_relations.update(model.relations())
                    self.declarative_base = model.declarative_base

            models = models_with_relations

        if create_polymorphic_parents:
            parents = set()

            for model in models:
                if issubclass(model, Base):
                    parents.update(model.parents())

            models.update(parents)

        get_metadata(models).create_all(
            bind=self.engine,
            tables=[model.__table__ for model in models],
            checkfirst=True,
        )

    def delete(self, *models):
        get_metadata(models).drop_all(
            bind=self.engine,
            tables=[model.__table__ for model in models],
            checkfirst=True,
        )

    def wipe(self):
        meta = MetaData()
        meta.reflect(bind=self.engine)
        meta.drop_all(bind=self.engine, tables=meta.sorted_tables, checkfirst=True)

        if not self.is_empty():
            raise DatabaseException(f"Database '{self}' was not empty after wipe.")

    def is_empty(self):
        table_names = inspect(self.engine).get_table_names()
        return not table_names

    def validate(self, base, logger=None):
        """Check whether the current db matches the models

        Check that all tables exist with all columns

        What is not checked:

        * Column types are not verified
        * Relationships are not verified

        :return: True if all declared Models and
        Attributes have corresponding tables and columns.
        """

        iengine = inspect(self.engine)

        errors = False

        tables = iengine.get_table_names()

        # Go through all Model subclasses
        for model_class in find_subclasses(base):
            module_marker = isinstance(model_class, _ModuleMarker)

            is_abstract = model_class.__dict__.get("__abstract__", False)

            if module_marker or is_abstract:
                continue

            table = model_class.__tablename__
            if table in tables:
                # Check all columns are found

                columns = [c["name"] for c in iengine.get_columns(table)]
                mapper = inspect(model_class)

                for column_prop in mapper.attrs:
                    if isinstance(column_prop, RelationshipProperty):
                        # TODO: Add checks for relations
                        pass
                    else:
                        for column in column_prop.columns:
                            # Assume normal flat column
                            if column.key not in columns:
                                if logger:
                                    logger.info(
                                        f"Column '{table}.{column.key}' does"
                                        f" not exist in db '{self.engine}'"
                                    )
                                errors = True
            else:
                if logger:
                    logger.info("Table '{table}' does not exist in db '{self.engine}'")

                errors = True

        return not errors

    def __contains__(self, model):
        connect_ = self.engine.connect()
        return self.engine.dialect.has_table(connect_, model.__tablename__)

    def __repr__(self):
        return f"<Database url='{self.url}'>"


def get_metadata(models: Iterable[object]):
    if not models:
        raise ValueError("Metadata must have at least one model specified")

    metadata = None

    for model in models:
        if hasattr(model, "metadata"):
            if metadata is None:
                metadata = model.metadata

            if model.metadata != metadata:
                raise ValueError("Metadata mismatch within list of models")
        else:
            raise ValueError("All models must specify a 'metadata' attribute")

    return metadata
