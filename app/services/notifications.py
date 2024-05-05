from loguru import logger

from app.repositories import NotificationsRepository, ChatsRepository
from app.infrastructure.telegram_client import TelegramClient
from app.entities import NotificationCreate, ChatsFilter


class NotificationsService:
    def __init__(
            self,
            notifications_repository: NotificationsRepository,
            chats_repository: ChatsRepository,
            telegram_client: TelegramClient
        ) -> None:
        self._notifications_repository = notifications_repository
        self._chats_repository = chats_repository
        self._telegram_client = telegram_client
    
    async def send(self, notification_create: NotificationCreate) -> None:
        logger.info(f'New notification: {notification_create.message}')

        notification = self._notifications_repository.create(notification_create)

        chats = self._chats_repository.list(ChatsFilter(for_system_managers=True))
        chats_ids = [c.id for c in chats]

        if notification.organization_id:
            org_chats = self._chats_repository.list(ChatsFilter(organization_id=notification.organization_id))
            chats_ids += [c.id for c in org_chats]

        for id in set(chats_ids):
            await self._telegram_client.send_notification(id, notification)
