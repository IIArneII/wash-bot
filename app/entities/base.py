from pydantic import BaseModel as PydanticBaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from humps import camelize


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        alias_generator=camelize,
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True
    )


class EntityBaseModel(BaseModel):
    created_at: datetime
    updated_at: datetime


class EntityBaseIdModel(EntityBaseModel):
    id: int


class EntityBaseUuidModel(EntityBaseModel):
    id: UUID
