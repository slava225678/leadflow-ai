from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.db.models import LeadStatus
from app.schemas.ai import LeadPriority


class LeadCreate(BaseModel):
    name: str
    phone: str
    email: str | None = None
    message: str


class LeadResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str | None
    message: str
    status: LeadStatus

    summary: str | None
    priority: LeadPriority | None
    budget: int | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
