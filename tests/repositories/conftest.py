from pytest import fixture
from sqlalchemy import text
from uuid import uuid4, UUID
from typing import Callable

from app.db.db import DataBase
from app.repositories import (
    ChatsRepository,
    NotificationsRepository,
    OrganizationsRepository,
    GroupsRepository,
    WashesRepository,
)
from app.entities import (
    NotificationCreate,
    OrganizationCreate,
    GroupCreate,
    WashCreate,
    ChatCreate,
)


@fixture(scope='package')
def chats_repo(db: DataBase) -> ChatsRepository:
    return ChatsRepository(db.get_session)


@fixture(scope='package')
def notifications_repo(db: DataBase) -> NotificationsRepository:
    return NotificationsRepository(db.get_session)


@fixture(scope='package')
def organizations_repo(db: DataBase) -> OrganizationsRepository:
    return OrganizationsRepository(db.get_session)


@fixture(scope='package')
def groups_repo(db: DataBase) -> GroupsRepository:
    return GroupsRepository(db.get_session)


@fixture(scope='package')
def washes_repo(db: DataBase) -> WashesRepository:
    return WashesRepository(db.get_session)


@fixture(scope='package')
def new_notification() -> Callable[..., NotificationCreate]:
    def f(
        org_id: UUID | None = None,
        group_id: UUID | None = None,
        wash_id: UUID | None = None,
        post_id: int | None = None
    ) -> NotificationCreate:
        return NotificationCreate(
            message='notification message',
            organization_id=org_id,
            group_id=group_id,
            wash_id=wash_id,
            post_id=post_id,
        )

    return f


@fixture(scope='package')
def new_organization() -> Callable[..., OrganizationCreate]:
    def f() -> OrganizationCreate:
        return OrganizationCreate(
            id=uuid4(),
            name='org name',
            description='org description',
            display_name='org display name',
            version=0,
        )

    return f


@fixture(scope='package')
def new_group() -> Callable[..., GroupCreate]:
    def f(org_id: UUID) -> GroupCreate:
        return GroupCreate(
            id=uuid4(),
            name='group name',
            description='group description',
            organization_id=org_id,
            version=0,
        )

    return f


@fixture(scope='package')
def new_wash() -> Callable[..., WashCreate]:
    def f(group_id: UUID) -> WashCreate:
        return WashCreate(
            id=uuid4(),
            name='wash name',
            description='wash description',
            group_id=group_id,
            version=0,
        )

    return f


@fixture(scope='package')
def new_chat() -> Callable[..., ChatCreate]:
    def f(id: int, org_id: UUID | None = None, for_system_managers: bool = False) -> ChatCreate:
        return ChatCreate(
            id=id,
            name='chat name',
            for_system_managers=for_system_managers,
            organization_id=org_id,
        )

    return f


@fixture(scope='function')
def clean_db(db: DataBase):
    with db.get_session() as session:
        session.execute(text('''
            do $$
            DECLARE
                seq_name text; 
                statements CURSOR FOR
                    SELECT tablename FROM pg_tables
                    WHERE schemaname = 'public';
            BEGIN
                FOR stmt IN statements LOOP
                    EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) || ' CASCADE;';
                END LOOP;

                FOR seq_name IN (SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema = 'public') LOOP 
                EXECUTE 'SELECT setval(' || quote_literal(seq_name) || ', 1, false)'; 
                END LOOP;

            END $$ LANGUAGE plpgsql;
        '''))
        session.commit()
