from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.rack import MAX_RACK_U, MIN_RACK_U, RACK_STATUSES


class RackBase(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=128)
    location_id: int
    height_u: int = Field(ge=MIN_RACK_U, le=MAX_RACK_U)
    status: str = "active"
    description: str | None = Field(default=None, max_length=2000)
    is_archived: bool = False

    @field_validator("status")
    @classmethod
    def status_must_be_known(cls, v: str) -> str:
        if v not in RACK_STATUSES:
            raise ValueError(f"Unknown rack status: {v}")
        return v

    @field_validator("code")
    @classmethod
    def normalize_code(cls, v: str) -> str:
        code = v.strip()
        if not code:
            raise ValueError("Code must not be blank")
        return code


class RackCreate(RackBase):
    pass


class RackUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=64)
    name: str | None = Field(default=None, min_length=1, max_length=128)
    location_id: int | None = None
    height_u: int | None = Field(default=None, ge=MIN_RACK_U, le=MAX_RACK_U)
    status: str | None = None
    description: str | None = Field(default=None, max_length=2000)

    @field_validator("status")
    @classmethod
    def status_must_be_known(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if v not in RACK_STATUSES:
            raise ValueError(f"Unknown rack status: {v}")
        return v

    @field_validator("code")
    @classmethod
    def normalize_code(cls, v: str | None) -> str | None:
        if v is None:
            return v
        code = v.strip()
        if not code:
            raise ValueError("Code must not be blank")
        return code


class RackLocationRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    type: str


class RackOut(RackBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    location: RackLocationRef
    created_at: str | None = None


class RackList(BaseModel):
    items: list[RackOut]
    total: int
