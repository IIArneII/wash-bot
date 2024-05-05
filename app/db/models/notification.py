from app.db.models.base import BaseModel
from sqlalchemy import Column, UUID, Integer, String


class Notification(BaseModel):
    __tablename__ = 'notifications'

    message = Column(String, nullable=False, server_default='', default='')
    organization_id = Column(UUID, nullable=True)
    group_id = Column(UUID, nullable=True)
    wash_id = Column(UUID, nullable=True)
    post_id = Column(Integer, nullable=True)
