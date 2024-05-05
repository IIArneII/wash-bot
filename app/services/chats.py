from loguru import logger

from app.repositories import ChatsRepository
from app.entities import ChatCreate


class ChatsService:
    def __init__(self, chats_repository: ChatsRepository) -> None:
        self._chats_repository = chats_repository
    
    async def new_chat(self, chat_create: ChatCreate) -> bool:
        chat = self._chats_repository.get(chat_create.id)

        if chat:
            logger.info(f'Trying to create an existing chat {chat_create.id}')
            return False
        
        self._chats_repository.create(chat_create)

        logger.info(f'New chat {chat_create.id} created')
        return True
