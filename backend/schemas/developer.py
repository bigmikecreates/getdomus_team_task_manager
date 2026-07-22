from datetime import datetime, time

from pydantic import BaseModel, EmailStr


class DeveloperCreate(BaseModel):
    name: str
    email: EmailStr
    timezone: str = "UTC"
    working_hours_start: time | None = None
    working_hours_end: time | None = None


class DeveloperUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    timezone: str | None = None
    working_hours_start: time | None = None
    working_hours_end: time | None = None


class DeveloperResponse(BaseModel):
    id: str
    name: str
    email: str
    timezone: str
    working_hours_start: time | None = None
    working_hours_end: time | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DeveloperAvailability(BaseModel):
    is_online: bool
    is_within_working_hours: bool
    local_time: str


class DeveloperWithAvailability(BaseModel):
    id: str
    name: str
    email: str
    timezone: str
    working_hours_start: time | None = None
    working_hours_end: time | None = None
    created_at: datetime
    updated_at: datetime
    is_online: bool = False
    is_within_working_hours: bool = False
    local_time: str = ""

    model_config = {"from_attributes": True}
