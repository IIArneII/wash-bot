from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from typing import Callable
from datetime import datetime, timezone
from uuid import UUID

from app.db.models import Wash as WashDB
from app.entities import Wash, WashCreate, WashUpdate, ALREADY_EXISTS


class WashesRepository:
    def __init__(self, get_session: Callable[..., Session]) -> None:
        self._get_session = get_session

    def get(self, id: int) -> Wash | None:
        with self._get_session() as session:
            wash = session.query(WashDB).where(WashDB.id == id).first()

            return Wash.model_validate(wash) if wash else None

    def create(self, model: WashCreate) -> Wash:
        try:
            with self._get_session() as session:
                wash = WashDB(**model.model_dump())
                session.add(wash)
                session.commit()
                session.refresh(wash)
                
                return Wash.model_validate(wash)
        except IntegrityError:
            raise ALREADY_EXISTS

    def update(self, id: UUID, model: WashUpdate) -> Wash | None:
        with self._get_session() as session:
            wash = session.query(WashDB).where(WashDB.id == id).first()

            if wash is None:
                return None

            if isinstance(model.name, str):
                wash.name = model.name

            if isinstance(model.description, str):
                wash.description = model.description
            
            if isinstance(model.version, int):
                wash.version = model.version
            
            if isinstance(model.group_id, UUID):
                wash.group_id = model.group_id

            wash.updated_at = datetime.now(timezone.utc)

            session.commit()

            return Wash.model_validate(wash)
