from sqlalchemy import Column, UUID, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.db.models.base import BaseModel
from app.db.models.organization import Organization
from app.db.models.group import Group
from app.db.models.wash import Wash


class Notification(BaseModel):
    __tablename__ = 'notifications'

    id = Column(BigInteger, primary_key=True)
    message = Column(String, nullable=False, server_default='', default='')
    service = Column(String, nullable=True)
    organization_id = Column(UUID, ForeignKey(Organization.id), nullable=True)
    group_id = Column(UUID, ForeignKey(Group.id), nullable=True)
    wash_id = Column(UUID, ForeignKey(Wash.id), nullable=True)
    post_id = Column(Integer, nullable=True)

    organization = relationship(Organization, lazy='joined')
    group = relationship(Group, lazy='joined')
    wash = relationship(Wash, lazy='joined')
