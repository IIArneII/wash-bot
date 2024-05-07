from pytest import raises
from uuid import uuid4
from typing import Callable

from app.repositories import OrganizationsRepository, GroupsRepository, WashesRepository
from app.entities import Wash, Group, OrganizationCreate, WashUpdate, GroupCreate, WashCreate, AlreadyExistsError


class TestCreate:
    def test_create(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            washes_repo: WashesRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            new_wash: Callable[..., WashCreate],
            clean_db,
        ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))
        new_wsh = new_wash(group_id=group.id)

        wash = washes_repo.create(new_wsh)
        assert type(wash) is Wash
        assert wash.id == new_wsh.id
        assert wash.name == new_wsh.name
        assert wash.description == new_wsh.description
        assert wash.group_id == new_wsh.group_id
        assert wash.version == new_wsh.version
    
    def test_already_exists_id(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            washes_repo: WashesRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            new_wash: Callable[..., WashCreate],
            clean_db,
        ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))

        new_wsh1 = new_wash(group_id=group.id)
        new_wsh2 = new_wash(group_id=group.id)
        new_wsh2.id = new_wsh1.id

        washes_repo.create(new_wsh1)

        with raises(AlreadyExistsError):
            washes_repo.create(new_wsh2)


class TestGet:
    def test_get(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            washes_repo: WashesRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            new_wash: Callable[..., WashCreate],
            clean_db
        ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))
        wash = washes_repo.create(new_wash(group_id=group.id))

        received_wash = washes_repo.get(wash.id)
        assert type(received_wash) is Wash
        assert received_wash.model_dump() == wash.model_dump()

    def test_not_found_by_id(self, washes_repo: WashesRepository, clean_db):
        received_group = washes_repo.get(uuid4())
        assert received_group is None


class TestUpdate:
    def test_update(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            washes_repo: WashesRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            new_wash: Callable[..., WashCreate],
            clean_db,
        ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))
        wash = washes_repo.create(new_wash(group_id=group.id))

        wash_update = WashUpdate(
            name='new wash name',
            description='new wash description',
            version=1,
        )

        wash.name = wash_update.name
        wash.description = wash_update.description
        wash.version = wash_update.version
        
        updated_wash = washes_repo.update(wash.id, wash_update)
        assert type(updated_wash) is Wash
        assert updated_wash.updated_at >= wash.updated_at
        wash.updated_at = updated_wash.updated_at
        assert updated_wash.model_dump() == wash.model_dump()
    
    def test_update_and_get(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            washes_repo: WashesRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            new_wash: Callable[..., WashCreate],
            clean_db
        ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))
        wash = washes_repo.create(new_wash(group_id=group.id))

        wash_update = WashUpdate(
            name='new wash name',
            description='new wash description',
            version=1,
        )

        wash.name = wash_update.name
        wash.description = wash_update.description
        wash.version = wash_update.version
        
        washes_repo.update(wash.id, wash_update)

        updated_wash = washes_repo.get(wash.id)
        assert type(updated_wash) is Wash
        assert updated_wash.updated_at >= wash.updated_at
        wash.updated_at = updated_wash.updated_at
        assert updated_wash.model_dump() == wash.model_dump()

    def test_not_found(self, washes_repo: WashesRepository, clean_db):
        updated_group = washes_repo.update(uuid4(), WashUpdate())
        assert updated_group is None

    def test_empty_update(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            washes_repo: WashesRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            new_wash: Callable[..., WashCreate],
            clean_db
        ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))
        wash = washes_repo.create(new_wash(group_id=group.id))

        updated_wash = washes_repo.update(wash.id, WashUpdate())
        assert type(updated_wash) is Wash
        assert updated_wash.updated_at >= wash.updated_at
        wash.updated_at = updated_wash.updated_at
        assert updated_wash.model_dump() == wash.model_dump()

    def test_empty_same_values(
            self,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            washes_repo: WashesRepository,
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            new_wash: Callable[..., WashCreate],
            clean_db
        ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))
        wash = washes_repo.create(new_wash(group_id=group.id))

        wash_update = WashUpdate(
            name=wash.name,
            description=wash.description,
            group_id=wash.group_id,
            version=wash.version,
        )

        updated_wash = washes_repo.update(wash.id, wash_update)
        assert type(updated_wash) is Wash
        assert updated_wash.updated_at >= wash.updated_at
        wash.updated_at = updated_wash.updated_at
        assert updated_wash.model_dump() == wash.model_dump()
