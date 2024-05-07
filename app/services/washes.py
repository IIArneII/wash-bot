from loguru import logger

from app.repositories import WashesRepository
from app.entities import WashCreate, Wash, WashUpdate


class WashesService:
    def __init__(self, washes_repository: WashesRepository) -> None:
        self._washes_repository = washes_repository
    
    async def create(self, wash_create: WashCreate) -> Wash:
        wash = self._washes_repository.get(wash_create.id)

        if wash and wash.version >= wash_create.version:
            return wash

        if wash and wash.version < wash_create.version:
            return self._washes_repository.update(wash_create.id, WashUpdate.model_validate(wash_create))
        
        return self._washes_repository.create(wash_create)
