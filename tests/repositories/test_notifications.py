from typing import Callable

from app.repositories import NotificationsRepository, OrganizationsRepository, GroupsRepository, WashesRepository
from app.entities import Notification, NotificationCreate, Organization, Group, Wash, OrganizationCreate, GroupCreate, WashCreate


class TestCreate:
    def test_create(self, notifications_repo: NotificationsRepository, new_notification: Callable[..., NotificationCreate], clean_db):
        new_ntf = new_notification()

        ntf = notifications_repo.create(new_ntf)
        assert type(ntf) is Notification
        assert ntf.message == new_ntf.message
        assert ntf.organization is None
        assert ntf.group is None
        assert ntf.wash is None
        assert ntf.post_id is None
    
    def test_create_with_attachments(
            self,
            notifications_repo: NotificationsRepository,
            organizations_repo: OrganizationsRepository,
            groups_repo: GroupsRepository,
            washes_repo: WashesRepository,
            new_notification: Callable[..., NotificationCreate],
            new_organization: Callable[..., OrganizationCreate],
            new_group: Callable[..., GroupCreate],
            new_wash: Callable[..., WashCreate],
            clean_db
        ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))
        wash = washes_repo.create(new_wash(group_id=group.id))

        new_ntf = new_notification(org_id=org.id, group_id=group.id, wash_id=wash.id, post_id=1)

        ntf = notifications_repo.create(new_ntf)
        assert type(ntf.organization) is Organization
        assert type(ntf.group) is Group
        assert type(ntf.wash) is Wash
        assert ntf.organization.model_dump() == org.model_dump()
        assert ntf.group.model_dump() == group.model_dump()
        assert ntf.wash.model_dump() == wash.model_dump()


class TestGet:
    def test_get(self, notifications_repo: NotificationsRepository, new_notification: Callable[..., NotificationCreate], clean_db):
        new_ntf = new_notification()

        ntf = notifications_repo.create(new_ntf)
        received_ntf = notifications_repo.get(ntf.id)
        assert type(received_ntf) is Notification
        assert received_ntf.model_dump() == ntf.model_dump()

    def test_not_found_by_id(self, notifications_repo: NotificationsRepository, clean_db):
        received_ntf = notifications_repo.get(1)
        assert received_ntf is None
    
    def test_get_with_attachments(
        self,
        notifications_repo: NotificationsRepository,
        organizations_repo: OrganizationsRepository,
        groups_repo: GroupsRepository,
        washes_repo: WashesRepository,
        new_notification: Callable[..., NotificationCreate],
        new_organization: Callable[..., OrganizationCreate],
        new_group: Callable[..., GroupCreate],
        new_wash: Callable[..., WashCreate],
        clean_db
    ):
        org = organizations_repo.create(new_organization())
        group = groups_repo.create(new_group(org_id=org.id))
        wash = washes_repo.create(new_wash(group_id=group.id))

        new_ntf = new_notification(org_id=org.id, group_id=group.id, wash_id=wash.id, post_id=1)
        ntf = notifications_repo.create(new_ntf)
        received_ntf = notifications_repo.get(ntf.id)
        assert type(received_ntf) is Notification
        assert ntf.model_dump() == received_ntf.model_dump()
