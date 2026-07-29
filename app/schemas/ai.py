from enum import StrEnum

from pydantic import BaseModel, Field


class LeadPriority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class LeadAnalysis(BaseModel):
    summary: str = Field(description="Short summary of the lead.")

    priority: LeadPriority = Field(description="Lead priority.")

    budget: int | None = Field(
        default=None,
        description="Estimated budget in user's currency if mentioned.",
    )
