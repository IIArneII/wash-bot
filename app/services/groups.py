from loguru import logger

from app.repositories import GroupsRepository
from app.entities import GroupCreate, Group, GroupUpdate


class GroupsService:
    def __init__(self, groups_repository: GroupsRepository) -> None:
        self._groups_repository = groups_repository
    
    async def create(self, group_create: GroupCreate) -> Group:
        group = self._groups_repository.get(group_create.id)

        if group and group.version >= group_create.version:
            return group

        if group and group.version < group_create.version:
            return self._groups_repository.update(group_create.id, GroupUpdate.model_validate(group_create))
        
        return self._groups_repository.create(group_create)
