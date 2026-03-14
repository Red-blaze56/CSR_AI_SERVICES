from pydantic import BaseModel, Field
from typing import Optional

class CampaignGenerationRequest(BaseModel):
    industry: Optional[str] = None
    company_size: Optional[str] = None
    budget: Optional[float] = None
    cause: Optional[str] = None
    region: Optional[str] = None
    timeline: Optional[str] = None
    employee_engagement: Optional[bool] = None

class CampaignGenerationResponse(BaseModel):
    campaigns: list