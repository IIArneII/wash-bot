from aio_pika import IncomingMessage
from json import loads

from app.services import NotificationsService
from app.entities import NotificationCreate


async def receive_notifications(container, message: IncomingMessage) -> None:
    notifications_service: NotificationsService = await container.notifications_service()

    msg: dict[str] = loads(message.body)    

    await notifications_service.send(NotificationCreate.model_validate(msg))
