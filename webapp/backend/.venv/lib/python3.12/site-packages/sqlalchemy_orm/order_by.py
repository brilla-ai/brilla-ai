import enum

from sqlalchemy_orm.query import QueryAdapter


class OrderByDirection(enum.Enum):
    asc = "asc"
    desc = "desc"


class OrderByMultipleEntitiesException(BaseException):
    pass


try:
    from dataclasses import dataclass

except ImportError:

    class OrderByBase(QueryAdapter):
        def __init__(
            self, key: str, direction: OrderByDirection = OrderByDirection.asc
        ):
            """
            The `OrderBy` ObjectType describes an
            order_by clause for a collection.
            """
            self.key = key
            self.direction = direction

else:

    @dataclass
    class OrderByBase(QueryAdapter):
        key: str
        direction: OrderByDirection = OrderByDirection.asc


class OrderBy(OrderByBase):
    def apply(self, query, entities=None):
        if len(entities) != 1:
            raise OrderByMultipleEntitiesException(
                f"Cannot use a OrderBy when querying" f" multiple models: '{entities}'"
            )

        model = entities[0]

        sort_attr = getattr(model, self.key)

        if self.direction == OrderByDirection.asc:
            criterion = sort_attr.asc()
        else:
            criterion = sort_attr.desc()

        return query.order_by(criterion)
