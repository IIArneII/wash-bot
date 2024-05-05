from app.db.models.base import BaseModel
from sqlalchemy import Column, UUID, Boolean, String


class Chat(BaseModel):
    __tablename__ = 'chats'
    
    name = Column(String, nullable=False, server_default='', default='')
    organization_id = Column(UUID, nullable=True)
    for_system_managers = Column(Boolean, nullable=False, server_default='false', default=False)
