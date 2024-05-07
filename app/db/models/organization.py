from app.db.models.base import SoftDeletedBaseModel
from sqlalchemy import Column, UUID, BigInteger, String


class Organization(SoftDeletedBaseModel):
    __tablename__ = 'organizations'

    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False, server_default='', default='')
    description = Column(String, nullable=False, server_default='', default='')
    display_name = Column(String, nullable=False, server_default='', default='')
    version = Column(BigInteger, nullable=False, server_default='0', default=0)
