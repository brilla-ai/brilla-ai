from sqlalchemy.orm import Session as SQLAlchemySession


class Session(SQLAlchemySession):
    def create(self, *instances):
        self.add_all(instances)

    def delete(self, *instances):
        for instance in instances:
            super().delete(instance)
