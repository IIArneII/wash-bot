from aiogram import Bot
from loguru import logger

from app.entities import Notification


class TelegramClient:
    def __init__(self, bot: Bot) -> None:
        logger.info('Telegram client initialization...')

        self._bot = bot
    
    async def send_notification(self, chat_id: int, notification: Notification) -> None:
        await self._bot.send_message(chat_id, TelegramClient._notification_msg(notification), parse_mode='MarkdownV2')
    
    @staticmethod
    def _notification_msg(notification: Notification) -> str:
        org = f'Организация: `{notification.organization.name}`\n' if notification.organization else ''
        grp = f'Группа: `{notification.group.name}`\n' if notification.group else ''
        wsh = f'Мойка: `{notification.wash.name}`\n' if notification.wash else ''
        pst = f'Пост: `{notification.post_id}`\n' if notification.post_id else ''
        svc = f'Сервис: `{notification.service}`\n' if notification.service else ''

        return f'''
***Новое уведомление***

{org}{grp}{wsh}{pst}{svc}
`{notification.message}`
'''
