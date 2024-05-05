from aiogram import Router
from aiogram.types import ChatMemberUpdated, ChatMemberMember
from aiogram.enums import ChatMemberStatus
from loguru import logger

from app.container import get_container
from app.services import ChatsService
from app.entities import ChatCreate


base_router = Router()


@base_router.my_chat_member()
async def start(updated: ChatMemberUpdated):
    try:
        if isinstance(updated.new_chat_member, ChatMemberMember) \
            and updated.new_chat_member.status == ChatMemberStatus.MEMBER \
            and updated.new_chat_member.user.is_bot \
            and updated.new_chat_member.user.id == updated.bot.id:
        
            chats_service: ChatsService = get_container().chats_service()
            await chats_service.new_chat(ChatCreate(
                id=updated.chat.id,
                name=updated.chat.full_name
            ))

    except Exception as e:
        logger.exception(e)
