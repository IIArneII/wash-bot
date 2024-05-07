from sqlalchemy import Column, UUID, Boolean, String, BigInteger, ForeignKey

from app.db.models.base import BaseModel
from app.db.models.organization import Organization


class Chat(BaseModel):
    __tablename__ = 'chats'
    
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False, server_default='', default='')
    organization_id = Column(UUID, ForeignKey(Organization.id), nullable=True)
    for_system_managers = Column(Boolean, nullable=False, server_default='false', default=False)
