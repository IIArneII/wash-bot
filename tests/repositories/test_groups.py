from pytest import raises
from uuid import uuid4
from typing import Callable

from app.repositories import OrganizationsRepository, GroupsRepository
from app.entities import Organization, Group, OrganizationCreate, GroupUpdate, GroupCreate, AlreadyExistsError


class TestCreate:
    def test_create(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            clean_db,
        ):
        org = organizations_repo.create(new_organization())

        new_grp = new_group(org_id=org.id)

        group = groups_repo.create(new_grp)
        assert type(group) is Group
        assert group.id == new_grp.id
        assert group.name == new_grp.name
        assert group.description == new_grp.description
        assert group.organization_id == new_grp.organization_id
        assert group.version == new_grp.version
    
    def test_already_exists_id(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            clean_db,
        ):
        org = organizations_repo.create(new_organization())

        new_grp1 = new_group(org_id=org.id)
        new_grp2 = new_group(org_id=org.id)
        new_grp2.id = new_grp1.id

        groups_repo.create(new_grp1)

        with raises(AlreadyExistsError):
            groups_repo.create(new_grp2)


class TestGet:
    def test_get(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            clean_db
        ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))

        received_group = groups_repo.get(group.id)
        assert type(received_group) is Group
        assert received_group.model_dump() == group.model_dump()

    def test_not_found_by_id(self, groups_repo: GroupsRepository, clean_db):
        received_group = groups_repo.get(uuid4())
        assert received_group is None


class TestUpdate:
    def test_update(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            clean_db,
        ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))

        group_update = GroupUpdate(
            name='new group name',
            description='new group description',
            version=1,
        )

        group.name = group_update.name
        group.description = group_update.description
        group.version = group_update.version
        
        updated_group = groups_repo.update(group.id, group_update)
        assert type(updated_group) is Group
        assert updated_group.updated_at >= group.updated_at
        group.updated_at = updated_group.updated_at
        assert updated_group.model_dump() == group.model_dump()
    
    def test_update_and_get(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            clean_db
        ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))

        group_update = GroupUpdate(
            name='new group name',
            description='new group description',
            version=1,
        )

        group.name = group_update.name
        group.description = group_update.description
        group.version = group_update.version
        
        groups_repo.update(group.id, group_update)

        updated_group = groups_repo.get(group.id)
        assert type(updated_group) is Group
        assert updated_group.updated_at >= group.updated_at
        group.updated_at = updated_group.updated_at
        assert updated_group.model_dump() == group.model_dump()

    def test_not_found(self, groups_repo: GroupsRepository, clean_db):
        updated_group = groups_repo.update(uuid4(), GroupUpdate())
        assert updated_group is None

    def test_empty_update(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            clean_db
        ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))

        updated_group = groups_repo.update(group.id, GroupUpdate())
        assert type(updated_group) is Group
        assert updated_group.updated_at >= group.updated_at
        group.updated_at = updated_group.updated_at
        assert updated_group.model_dump() == group.model_dump()

    def test_empty_same_values(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            clean_db
        ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))

        group_update = GroupUpdate(
            name=group.name,
            description=group.description,
            organization_id=group.organization_id,
            version=group.version,
        )

        updated_group = groups_repo.update(group.id, group_update)
        assert type(updated_group) is Group
        assert updated_group.updated_at >= group.updated_at
        group.updated_at = updated_group.updated_at
        assert updated_group.model_dump() == group.model_dump()
