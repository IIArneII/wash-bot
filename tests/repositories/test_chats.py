from pytest import raises
from typing import Callable

from app.repositories import ChatsRepository, OrganizationsRepository
from app.entities import Chat, ChatCreate, ChatsFilter, OrganizationCreate, AlreadyExistsError


class TestCreate:
    def test_create(self, chats_repo: ChatsRepository, new_chat: Callable[..., ChatCreate], clean_db):
        new_cht = new_chat(1)

        chat = chats_repo.create(new_cht)
        assert type(chat) is Chat
        assert chat.id == new_cht.id
        assert chat.name == new_cht.name
        assert chat.for_system_managers == new_cht.for_system_managers
        assert chat.organization_id == new_cht.organization_id
    
    def test_already_exists_id(self, chats_repo: ChatsRepository, new_chat: Callable[..., ChatCreate], clean_db):
        new_cht1 = new_chat(1)
        new_cht2 = new_chat(1)

        chats_repo.create(new_cht1)

        with raises(AlreadyExistsError):
            chats_repo.create(new_cht2)


class TestGet:
    def test_get(self, chats_repo: ChatsRepository, new_chat: Callable[..., ChatCreate], clean_db):
        new_cht = new_chat(1)

        chat = chats_repo.create(new_cht)
        received_chat = chats_repo.get(chat.id)
        assert type(received_chat) is Chat
        assert received_chat.model_dump() == chat.model_dump()

    def test_not_found_by_id(self, chats_repo: ChatsRepository, clean_db):
        received_chat = chats_repo.get(1)
        assert received_chat is None


class TestList:
    def test_list(
            self,
            chats_repo: ChatsRepository,
            organizations_repo: OrganizationsRepository,
            new_chat: Callable[..., ChatCreate],
            new_organization: Callable[..., OrganizationCreate],
            clean_db
        ):
        org = organizations_repo.create(new_organization())

        chat1 = new_chat(1)
        chat2 = new_chat(2, org.id)
        chat3 = new_chat(3)
        chat3.for_system_managers = True

        chat1 = chats_repo.create(chat1)
        chat2 = chats_repo.create(chat2)
        chat3 = chats_repo.create(chat3)

        list = chats_repo.list(ChatsFilter())
        assert [i.model_dump() for i in list] == [i.model_dump() for i in [chat1, chat2, chat3]]

        list = chats_repo.list(ChatsFilter(for_system_managers=True))
        assert [i.model_dump() for i in list] == [i.model_dump() for i in [chat3]]

        list = chats_repo.list(ChatsFilter(for_system_managers=False))
        assert [i.model_dump() for i in list] == [i.model_dump() for i in [chat1, chat2]]

        list = chats_repo.list(ChatsFilter(organization_id=org.id))
        assert [i.model_dump() for i in list] == [i.model_dump() for i in [chat2]]

        list = chats_repo.list(ChatsFilter(organization_id=org.id, for_system_managers=True))
        assert list == []
