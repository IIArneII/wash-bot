from loguru import logger

from app.repositories import OrganizationsRepository
from app.entities import OrganizationCreate, Organization, OrganizationUpdate


class OrganizationsService:
    def __init__(self, organizations_repository: OrganizationsRepository) -> None:
        self._organizations_repository = organizations_repository
    
    async def create(self, org_create: OrganizationCreate) -> Organization:
        org = self._organizations_repository.get(org_create.id)

        if org and org.version >= org_create.version:
            return org

        if org and org.version < org_create.version:
            return self._organizations_repository.update(org_create.id, OrganizationUpdate.model_validate(org_create))
        
        return self._organizations_repository.create(org_create)
