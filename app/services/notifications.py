from loguru import logger

from app.repositories import NotificationsRepository, ChatsRepository, OrganizationsRepository, GroupsRepository, WashesRepository
from app.infrastructure.telegram_client import TelegramClient
from app.entities import NotificationCreate, ChatsFilter


class NotificationsService:
    def __init__(
            self,
            notifications_repository: NotificationsRepository,
            chats_repository: ChatsRepository,
            organizations_repository: OrganizationsRepository,
            groups_repository: GroupsRepository,
            washes_repository: WashesRepository,
            telegram_client: TelegramClient
        ) -> None:
        self._notifications_repository = notifications_repository
        self._organizations_repository = organizations_repository
        self._groups_repository = groups_repository
        self._washes_repository = washes_repository
        self._chats_repository = chats_repository
        self._telegram_client = telegram_client
    
    async def send(self, notification_create: NotificationCreate) -> None:
        logger.info(f'New notification: {notification_create.message}')

        # If we receive non-existent connections, we cut them off in order to send a notification anyway
        # If we haven’t received some entities, then we try to restore them based on known ones

        if notification_create.wash_id:
            wash = self._washes_repository.get(notification_create.wash_id)
            if not wash:
                logger.warning(f'Unknown wash {notification_create.wash_id} will be cut')
                notification_create.wash_id = None
            
            elif not notification_create.group_id:
                notification_create.group_id = wash.group_id

        if notification_create.group_id:
            group = self._groups_repository.get(notification_create.group_id)
            if not group:
                logger.warning(f'Unknown group {notification_create.group_id} will be cut')
                notification_create.group_id = None
            
            elif not notification_create.organization_id:
                notification_create.organization_id = group.organization_id

        if notification_create.organization_id:
            org = self._organizations_repository.get(notification_create.organization_id)
            if not org:
                logger.warning(f'Unknown organization {notification_create.organization_id} will be cut')
                notification_create.organization_id = None

        notification = self._notifications_repository.create(notification_create)

        chats = self._chats_repository.list(ChatsFilter(for_system_managers=True))
        chats_ids = [c.id for c in chats]

        if notification.organization:
            org_chats = self._chats_repository.list(ChatsFilter(organization_id=notification.organization.id))
            chats_ids += [c.id for c in org_chats]

        for id in set(chats_ids):
            await self._telegram_client.send_notification(id, notification)
