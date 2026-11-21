from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.location import LOCATION_TYPES


class LocationBase(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=128)
    type: str
    parent_id: int | None = None
    description: str | None = Field(default=None, max_length=2000)
    is_archived: bool = False

    @field_validator("type")
    @classmethod
    def type_must_be_known(cls, v: str) -> str:
        if v not in LOCATION_TYPES:
            raise ValueError(f"Unknown location type: {v}")
        return v

    @field_validator("code")
    @classmethod
    def normalize_code(cls, v: str) -> str:
        code = v.strip()
        if not code:
            raise ValueError("Code must not be blank")
        return code


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=64)
    name: str | None = Field(default=None, min_length=1, max_length=128)
    description: str | None = Field(default=None, max_length=2000)

    @field_validator("code")
    @classmethod
    def normalize_code(cls, v: str | None) -> str | None:
        if v is None:
            return v
        code = v.strip()
        if not code:
            raise ValueError("Code must not be blank")
        return code


class LocationOut(LocationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: str | None = None


class LocationSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    type: str
    is_archived: bool


class LocationTreeNode(LocationSummary):
    children: list["LocationTreeNode"] = []


class LocationList(BaseModel):
    items: list[LocationOut]
    total: int
