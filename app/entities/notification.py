from uuid import UUID

from app.entities.base import EntityBaseIdModel, BaseModel
from app.entities.organization import Organization
from app.entities.group import Group
from app.entities.wash import Wash


class Notification(EntityBaseIdModel):
    message: str
    service: str | None = None
    organization: Organization | None = None
    group: Group | None = None
    wash: Wash | None = None
    post_id: int | None = None


class NotificationCreate(BaseModel):
    message: str
    service: str | None = None
    organization_id: UUID | None = None
    group_id: UUID | None = None
    wash_id: UUID | None = None
    post_id: int | None = None
