from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

ApplicationStatus = Literal[
    "Applied",
    "Interview",
    "Assessment",
    "Offer",
    "Rejected",
]

WorkSetup = Literal["Remote", "Hybrid", "On-site"]


class ApplicationBase(BaseModel):
    company: str = Field(min_length=1, max_length=120)
    role: str = Field(min_length=1, max_length=160)
    location: str = Field(default="", max_length=160)
    work_setup: WorkSetup = "Remote"
    status: ApplicationStatus = "Applied"
    salary: str = Field(default="", max_length=100)
    job_url: HttpUrl | None = None
    notes: str = Field(default="", max_length=4000)
    applied_at: date = Field(default_factory=date.today)


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(ApplicationBase):
    pass


class ApplicationRead(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class StatsResponse(BaseModel):
    total: int
    applied: int
    interview: int
    assessment: int
    offer: int
    rejected: int
