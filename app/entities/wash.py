from uuid import UUID

from app.entities.base import EntityBaseUuidModel, BaseModel


class Wash(EntityBaseUuidModel):
    group_id: UUID
    name: str
    description: str
    version: int


class WashCreate(BaseModel):
    id: UUID
    group_id: UUID
    name: str
    description: str
    version: int


class WashUpdate(BaseModel):
    group_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    version: int | None = None
