from sqlalchemy.orm.session import Session
from typing import Callable

from app.db.models import Notification as NotificationDB
from app.entities import Notification, NotificationCreate


class NotificationsRepository:
    def __init__(self, get_session: Callable[..., Session]) -> None:
        self._get_session = get_session

    def get(self, id: int) -> Notification | None:
        with self._get_session() as session:
            notification = session.query(NotificationDB).where(NotificationDB.id == id).first()

            return Notification.model_validate(notification) if notification else None

    def create(self, model: NotificationCreate) -> Notification:
        with self._get_session() as session:
            user = NotificationDB(**model.model_dump())
            session.add(user)
            session.commit()
            session.refresh(user)
            
            return Notification.model_validate(user)
