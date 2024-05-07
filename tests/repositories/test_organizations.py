from pytest import raises
from uuid import uuid4
from typing import Callable

from app.repositories import OrganizationsRepository
from app.entities import Organization, OrganizationCreate, OrganizationUpdate, AlreadyExistsError


class TestCreate:
    def test_create(self, organizations_repo: OrganizationsRepository, new_organization: Callable[..., OrganizationCreate], clean_db):
        new_org = new_organization()

        org = organizations_repo.create(new_org)
        assert type(org) is Organization
        assert org.id == new_org.id
        assert org.name == new_org.name
        assert org.description == new_org.description
        assert org.display_name == new_org.display_name
        assert org.version == new_org.version
    
    def test_already_exists_id(self, organizations_repo: OrganizationsRepository, new_organization: Callable[..., OrganizationCreate], clean_db):
        new_org1 = new_organization()

        new_org2 = new_organization()
        new_org2.id = new_org1.id

        organizations_repo.create(new_org1)

        with raises(AlreadyExistsError):
            organizations_repo.create(new_org2)


class TestGet:
    def test_get(self, organizations_repo: OrganizationsRepository, new_organization: Callable[..., OrganizationCreate], clean_db):
        new_org = new_organization()

        org = organizations_repo.create(new_org)
        received_org = organizations_repo.get(org.id)
        assert type(received_org) is Organization
        assert received_org.model_dump() == org.model_dump()

    def test_not_found_by_id(self, organizations_repo: OrganizationsRepository, clean_db):
        received_org = organizations_repo.get(uuid4())
        assert received_org is None


class TestUpdate:
    def test_update(self, organizations_repo: OrganizationsRepository, new_organization: Callable[..., OrganizationCreate], clean_db):
        new_org = new_organization()

        org = organizations_repo.create(new_org)

        org_update = OrganizationUpdate(
            name='new org name',
            description='new org description',
            display_name='new org display name',
            version=1,
        )

        org.name = org_update.name
        org.description = org_update.description
        org.display_name = org_update.display_name
        org.version = org_update.version
        
        updated_org = organizations_repo.update(org.id, org_update)
        assert type(updated_org) is Organization
        assert updated_org.updated_at >= org.updated_at
        org.updated_at = updated_org.updated_at
        assert updated_org.model_dump() == org.model_dump()
    
    def test_update_and_get(self, organizations_repo: OrganizationsRepository, new_organization: Callable[..., OrganizationCreate], clean_db):
        new_org = new_organization()

        org = organizations_repo.create(new_org)

        org_update = OrganizationUpdate(
            name='new org name',
            description='new org description',
            display_name='new org display name',
            version=1,
        )

        org.name = org_update.name
        org.description = org_update.description
        org.display_name = org_update.display_name
        org.version = org_update.version
        
        organizations_repo.update(org.id, org_update)

        updated_org = organizations_repo.get(org.id)
        assert type(updated_org) is Organization
        assert updated_org.updated_at >= org.updated_at
        org.updated_at = updated_org.updated_at
        assert updated_org.model_dump() == org.model_dump()

    def test_not_found(self, organizations_repo: OrganizationsRepository, clean_db):
        updated_org = organizations_repo.update(uuid4(), OrganizationUpdate())
        assert updated_org is None

    def test_empty_update(self, organizations_repo: OrganizationsRepository, new_organization: Callable[..., OrganizationCreate], clean_db):
        new_org = new_organization()

        org = organizations_repo.create(new_org)

        updated_org = organizations_repo.update(org.id, OrganizationUpdate())
        assert type(updated_org) is Organization
        assert updated_org.updated_at >= org.updated_at
        org.updated_at = updated_org.updated_at
        assert updated_org.model_dump() == org.model_dump()

    def test_empty_same_values(self, organizations_repo: OrganizationsRepository, new_organization: Callable[..., OrganizationCreate], clean_db):
        new_org = new_organization()

        org = organizations_repo.create(new_org)

        org_update = OrganizationUpdate(
            name=org.name,
            description=org.description,
            display_name=org.display_name,
            version=org.version,
        )

        updated_org = organizations_repo.update(org.id, org_update)
        assert type(updated_org) is Organization
        assert updated_org.updated_at >= org.updated_at
        org.updated_at = updated_org.updated_at
        assert updated_org.model_dump() == org.model_dump()
