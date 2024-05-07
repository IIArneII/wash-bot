from uuid import UUID

from app.entities.base import EntityBaseUuidModel, BaseModel


class Organization(EntityBaseUuidModel):
    name: str
    description: str
    display_name: str
    version: int


class OrganizationCreate(BaseModel):
    id: UUID
    name: str
    description: str
    display_name: str
    version: int


class OrganizationUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    display_name: str | None = None
    version: int | None = None
