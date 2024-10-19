#  Database models
from datetime import datetime
from uuid import uuid4
from sqlalchemy import UUID, Column, DateTime


class DefaultData:
    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    created_at = Column(DateTime , default=datetime.utcnow())
    deleted_at = Column(DateTime, default=None, nullable=True)
    updated_at = Column(DateTime , default=datetime.utcnow())