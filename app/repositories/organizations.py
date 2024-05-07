from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from typing import Callable
from datetime import datetime, timezone
from uuid import UUID

from app.db.models import Organization as OrganizationDB
from app.entities import Organization, OrganizationCreate, OrganizationUpdate, ALREADY_EXISTS


class OrganizationsRepository:
    def __init__(self, get_session: Callable[..., Session]) -> None:
        self._get_session = get_session

    def get(self, id: int) -> Organization | None:
        with self._get_session() as session:
            org = session.query(OrganizationDB).where(OrganizationDB.id == id).first()

            return Organization.model_validate(org) if org else None

    def create(self, model: OrganizationCreate) -> Organization:
        try:
            with self._get_session() as session:
                org = OrganizationDB(**model.model_dump())
                session.add(org)
                session.commit()
                session.refresh(org)
                
                return Organization.model_validate(org)
        
        except IntegrityError:
            raise ALREADY_EXISTS
    
    def update(self, id: UUID, model: OrganizationUpdate) -> Organization | None:
        with self._get_session() as session:
            org = session.query(OrganizationDB).where(OrganizationDB.id == id).first()

            if org is None:
                return None

            if isinstance(model.name, str):
                org.name = model.name

            if isinstance(model.description, str):
                org.description = model.description
            
            if isinstance(model.display_name, str):
                org.display_name = model.display_name
            
            if isinstance(model.version, int):
                org.version = model.version

            org.updated_at = datetime.now(timezone.utc)

            session.commit()

            return Organization.model_validate(org)
