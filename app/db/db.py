from contextlib import contextmanager
from pydantic import BaseModel
from loguru import logger

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session

from alembic import command
from alembic.config import Config

Base: BaseModel = declarative_base()

from app.config import DBConfig
from app.db import models


class DataBase:
    def __init__(self, config: dict | DBConfig, ping: bool = True) -> None:
        logger.info(f'Init data base...')
        
        self._config = config if type(config) is DBConfig else DBConfig(config)
        self._engine = create_engine(self._config.dsn(), pool_pre_ping=True)
        self._session_factory = scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        ))

        Base.metadata.bind = self._engine

        if ping:
            self.ping()

        if self._config.APPLY_MIGRATIONS:
            self.apply_migrations()

    def apply_migrations(self) -> None:
        logger.info('Apply migrations...')
        
        alembic_cfg = Config(self._config.ALEMBIC_INI_PATH)
        alembic_cfg.set_section_option(alembic_cfg.config_ini_section, 'sqlalchemy.url', self._config.dsn())

        command.upgrade(alembic_cfg, "head")

    def ping(self):
        logger.info('Ping data base...')

        with self._engine.connect() as _: ...

    @contextmanager
    def get_session(self):
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.error('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()
            logger.debug('Session close')
