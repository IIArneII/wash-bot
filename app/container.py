from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton, Configuration, Resource
from aiogram import Bot, Dispatcher
from loguru import logger

from app.config import Config
from app.db.db import DataBase
from app.repositories import NotificationsRepository, ChatsRepository
from app.services import NotificationsService, ChatsService
from app.bot import init_bot, init_dispatcher
from app.transport.rabbit import RabbitClient
from app.infrastructure.telegram_client import TelegramClient


class Container(DeclarativeContainer):
    config: Config = Configuration()

    db: DataBase = Singleton(DataBase, config=config.db)

    notifications_repository: NotificationsRepository = Factory(NotificationsRepository, get_session=db.provided.get_session)
    chats_repository: ChatsRepository = Factory(ChatsRepository, get_session=db.provided.get_session)

    dispatcher: Dispatcher = Resource(init_dispatcher)
    bot: Bot = Resource(init_bot, config=config.bot)

    rabbit_client: RabbitClient = Singleton(RabbitClient, config=config.rabbit)

    telegram_client: TelegramClient = Singleton(TelegramClient, bot=bot)

    notifications_service: NotificationsService = Factory(
        NotificationsService,
        notifications_repository=notifications_repository,
        chats_repository=chats_repository,
        telegram_client=telegram_client,
    )

    chats_service: ChatsService = Factory(ChatsService, chats_repository=chats_repository)


container : Container | None = None


async def init_container(config: Config) -> Container:
    logger.info('Container initialization...')

    global container
    container = Container()
    container.config.from_dict(config.model_dump())

    container.dispatcher()
    await container.bot()
    container.db()
    container.telegram_client()
    container.rabbit_client()

    return container


def get_container() -> Container:
    global container
    return container
