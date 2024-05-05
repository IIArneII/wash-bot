from aiogram import Bot
from loguru import logger

from app.entities import Notification


class TelegramClient:
    def __init__(self, bot: Bot) -> None:
        logger.info('Telegram client initialization...')

        self._bot = bot
    
    async def send_notification(self, chat_id: int, notification: Notification) -> None:
        await self._bot.send_message(chat_id, TelegramClient._notification_msg(notification))
    
    @staticmethod
    def _notification_msg(notification: Notification) -> str:
        return f'''
Новое уведомление

Организация: {notification.organization_id}
Группа: {notification.group_id}
Мойка: {notification.wash_id}
Пост: {notification.post_id}

{notification.message}
'''
