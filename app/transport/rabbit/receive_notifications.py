from aio_pika import IncomingMessage
from json import loads
from loguru import logger

from app.services import NotificationsService
from app.entities import NotificationCreate


async def receive_notifications(container, message: IncomingMessage) -> None:
    if not message.body:
        await message.nack(requeue=False)
        return

    try:
        msg: dict[str] = loads(message.body)
        model = NotificationCreate.model_validate(msg)
    except Exception as e:
        logger.info(f'failed to parse the body {message.body}, error: {e}')
        await message.nack(requeue=False)
        return

    notifications_service: NotificationsService = await container.notifications_service() 
    await notifications_service.send(model)

    await message.ack()
