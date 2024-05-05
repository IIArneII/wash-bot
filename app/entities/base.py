from pydantic import BaseModel as PydanticBaseModel, Field, ConfigDict
from datetime import datetime
from humps import camelize


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        alias_generator=camelize,
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True
    )


class EntityBaseModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
