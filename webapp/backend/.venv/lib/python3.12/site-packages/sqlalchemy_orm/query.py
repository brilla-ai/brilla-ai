from sqlalchemy.orm import Query as SQLAlchemyQuery


class QueryAdapter:
    def apply(self, query, entities=None):
        return query


class Query(SQLAlchemyQuery):
    def _apply_adapters(self, *criterion):
        query = self
        criterion = [criteria for criteria in criterion if criteria is not None]
        entities = [cd["type"] for cd in self.column_descriptions]
        for criteria in [*criterion]:
            if isinstance(criteria, QueryAdapter):
                criterion.remove(criteria)
                query = criteria.apply(query, entities)

        return criterion, query

    def filter(self, *criterion):
        criterion, query = self._apply_adapters(*criterion)
        return super(Query, query).filter(*criterion)

    def order_by(self, *criterion):
        criterion, query = self._apply_adapters(*criterion)
        return super(Query, query).order_by(*criterion)
