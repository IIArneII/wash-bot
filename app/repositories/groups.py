from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from typing import Callable
from datetime import datetime, timezone
from uuid import UUID

from app.db.models import Group as GroupDB
from app.entities import Group, GroupCreate, GroupUpdate, ALREADY_EXISTS


class GroupsRepository:
    def __init__(self, get_session: Callable[..., Session]) -> None:
        self._get_session = get_session

    def get(self, id: int) -> Group | None:
        with self._get_session() as session:
            group = session.query(GroupDB).where(GroupDB.id == id).first()

            return Group.model_validate(group) if group else None

    def create(self, model: GroupCreate) -> Group:
        try:
            with self._get_session() as session:
                group = GroupDB(**model.model_dump())
                session.add(group)
                session.commit()
                session.refresh(group)
                
                return Group.model_validate(group)
        except IntegrityError:
            raise ALREADY_EXISTS
    
    def update(self, id: UUID, model: GroupUpdate) -> Group | None:
        with self._get_session() as session:
            group = session.query(GroupDB).where(GroupDB.id == id).first()

            if group is None:
                return None

            if isinstance(model.name, str):
                group.name = model.name

            if isinstance(model.description, str):
                group.description = model.description
            
            if isinstance(model.version, int):
                group.version = model.version
            
            if isinstance(model.organization_id, UUID):
                group.organization_id = model.organization_id

            group.updated_at = datetime.now(timezone.utc)

            session.commit()

            return Group.model_validate(group)
