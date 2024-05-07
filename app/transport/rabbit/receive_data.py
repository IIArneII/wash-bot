from aio_pika import IncomingMessage
from json import loads
from loguru import logger

from app.services import OrganizationsService, GroupsService, WashesService
from app.entities import RabbitMessageType, OrganizationCreate, GroupCreate, WashCreate


async def receive_data(container, message: IncomingMessage) -> None:
    match message.type:
        case RabbitMessageType.organization_data:
            msg: dict[str] = loads(message.body)
            organizations_service: OrganizationsService = container.organizations_service()
            await organizations_service.create(OrganizationCreate.model_validate(msg))

        case RabbitMessageType.group_data:
            msg: dict[str] = loads(message.body)
            groups_service: GroupsService = container.groups_service()
            await groups_service.create(GroupCreate.model_validate(msg))

        case RabbitMessageType.wash_data:
            msg: dict[str] = loads(message.body)
            washes_service: WashesService = container.washes_service()
            await washes_service.create(WashCreate.model_validate(msg))

        case _:
           await message.nack(requeue=False)
