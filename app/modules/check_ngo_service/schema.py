from pydantic import BaseModel, Field
from supabase_auth import datetime

class CheckNGOServicesRequest(BaseModel):
    budget: float = Field(..., gt=0)
    milestones: int = Field(..., gt=0)
    category: str
    timeline_start: str
    timeline_end: str
    location: str

class NGOMatch(BaseModel):
    ngo_id: str
    title: str
    description: str
    category: str
    location: str
    estimated_budget: float | None = None
    similarity: float


class CheckNGOServicesResponse(BaseModel):
    found: bool
    data: list[NGOMatch] | None = None
    message: str