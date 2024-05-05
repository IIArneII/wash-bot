from sqlalchemy.orm.session import Session
from typing import Callable

from app.db.models import Chat as ChatDB
from app.entities import Chat, ChatCreate, ChatsFilter


class ChatsRepository:
    def __init__(self, get_session: Callable[..., Session]) -> None:
        self._get_session = get_session

    def get(self, id: int) -> Chat | None:
        with self._get_session() as session:
            chat = session.query(ChatDB).where(ChatDB.id == id).first()

            return Chat.model_validate(chat) if chat else None
    
    def list(self, filter: ChatsFilter) -> list[Chat]:
        with self._get_session() as session:
            q = session.query(ChatDB)

            if filter.organization_id:
                q = q.where(ChatDB.organization_id == filter.organization_id)
            
            if filter.for_system_managers:
                q = q.filter(ChatDB.for_system_managers == filter.for_system_managers)
            
            items = q.all()

            return [Chat.model_validate(e) for e in items]

    def create(self, model: ChatCreate) -> Chat:
        with self._get_session() as session:
            chat = ChatDB(**model.model_dump())
            session.add(chat)
            session.commit()
            session.refresh(chat)
            
            return Chat.model_validate(chat)
