from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict

class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
    )

class BotConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='BOT_')

    TOKEN: str = '0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'


class DBConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='DB_')

    ALEMBIC_INI_PATH: str = 'alembic.ini'
    PORT: int = 5432
    HOST: str = 'wash_bot_postgres'
    NAME: str = 'wash_bot'
    USER: str = 'admin'
    PASSWORD: str = 'password'
    APPLY_MIGRATIONS: bool = True

    def dsn(self):
        if self.PASSWORD:
            return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"
        return f"postgresql://{self.USER}@{self.HOST}:{self.PORT}/{self.NAME}"


class RabbitConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='RABBIT_')

    HOST: str = 'localhost'
    PORT: int = 5672
    PASSWORD: str = 'password'
    USER: str = 'admin'
    SECURE: bool = True


class LogConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='LOG_', use_enum_values=True)

    class LogLevel(str, Enum):
        debug = 'debug'
        info = 'info'
        error = 'error'

    LEVEL: LogLevel = LogLevel.info
    DIR: str = ''
    RETENTION: int = 5
    ROTATION: int = 100


class Config(BaseSettings):
    bot: BotConfig = BotConfig()
    db:  DBConfig  = DBConfig()
    log: LogConfig = LogConfig()
    rabbit: RabbitConfig = RabbitConfig()
