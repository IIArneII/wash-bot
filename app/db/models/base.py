from app.db.db import Base

from sqlalchemy import Column, BigInteger, DateTime
from datetime import datetime, timezone


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class SoftDeletedBaseModel(BaseModel):
    __abstract__ = True

    deleted_at = Column(DateTime, nullable=True)
