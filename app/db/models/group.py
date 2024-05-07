from sqlalchemy import Column, UUID, BigInteger, String, ForeignKey

from app.db.models.base import SoftDeletedBaseModel
from app.db.models.organization import Organization


class Group(SoftDeletedBaseModel):
    __tablename__ = 'groups'

    id = Column(UUID, primary_key=True)
    organization_id = Column(UUID, ForeignKey(Organization.id), nullable=False)
    name = Column(String, nullable=False, server_default='', default='')
    description = Column(String, nullable=False, server_default='', default='')
    version = Column(BigInteger, nullable=False, server_default='0', default=0)
