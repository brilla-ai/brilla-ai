from typing import List

from sqlalchemy import or_, and_

from sqlalchemy_orm.query import QueryAdapter

try:
    from dataclasses import dataclass

except ImportError:

    class FilterBase(QueryAdapter):
        # noinspection PyPep8Naming
        def __init__(self, or_: List["Filter"] = None, and_: List["Filter"] = None):
            self.or_ = or_
            self.and_ = and_

else:

    @dataclass
    class FilterBase(QueryAdapter):
        and_: List["Filter"] = None
        or_: List["Filter"] = None


class Filter(FilterBase):
    def apply(self, query, entities=None):
        return query.filter(*self.criterion(entities=entities))

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def criterion(self, entities=None):
        if self.or_ and self.and_:
            raise ValueError(
                "Filter applied with both logical operators 'OR' and 'AND'"
            )

        criterion = []

        if self.or_:
            criterion = [
                or_(
                    *[and_(*filter.criterion(entities=entities)) for filter in self.or_]
                )
            ]

        if self.and_:
            criterion = [
                and_(
                    *[
                        and_(*filter.criterion(entities=entities))
                        for filter in self.and_
                    ]
                )
            ]

        return criterion
