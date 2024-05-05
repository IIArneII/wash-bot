from uuid import UUID

from app.entities.base import EntityBaseModel, BaseModel


class Notification(EntityBaseModel):
    message: str
    organization_id: UUID | None = None
    group_id: UUID | None = None
    wash_id: UUID | None = None
    post_id: int | None = None


class NotificationCreate(BaseModel):
    message: str
    organization_id: UUID | None = None
    group_id: UUID | None = None
    wash_id: UUID | None = None
    post_id: int | None = None
