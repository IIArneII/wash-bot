from sqlalchemy import Column, UUID, BigInteger, String, ForeignKey

from app.db.models.base import SoftDeletedBaseModel
from app.db.models.group import Group


class Wash(SoftDeletedBaseModel):
    __tablename__ = 'washes'

    id = Column(UUID, primary_key=True)
    group_id = Column(UUID, ForeignKey(Group.id), nullable=False)
    name = Column(String, nullable=False, server_default='', default='')
    description = Column(String, nullable=False, server_default='', default='')
    version = Column(BigInteger, nullable=False, server_default='0', default=0)
