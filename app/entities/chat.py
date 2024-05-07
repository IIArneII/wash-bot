from uuid import UUID

from app.entities.base import EntityBaseIdModel, BaseModel


class Chat(EntityBaseIdModel):
    name: str
    for_system_managers: bool = False
    organization_id: UUID | None = None


class ChatCreate(BaseModel):
    id: int
    name: str
    for_system_managers: bool = False
    organization_id: UUID | None = None


class ChatsFilter(BaseModel):
    for_system_managers: bool | None = None
    organization_id: UUID | None = None
