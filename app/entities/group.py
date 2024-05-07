from uuid import UUID

from app.entities.base import EntityBaseUuidModel, BaseModel


class Group(EntityBaseUuidModel):
    organization_id: UUID
    name: str
    description: str
    version: int


class GroupCreate(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    description: str
    version: int


class GroupUpdate(BaseModel):
    organization_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    version: int | None = None
