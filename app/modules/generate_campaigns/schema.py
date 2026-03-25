from pydantic import BaseModel, Field

class MilestoneInput(BaseModel):
    title: str
    budget_allocated: float = Field(gt=0)

class CampaignGenerationRequest(BaseModel):
    company_id: str
    budget: float = Field(..., gt=0)
    milestones: int = Field(ge=1, le=10)
    category: str
    timeline_start: str
    timeline_end: str
    location: str
    milestone_inputs: list[MilestoneInput] = Field(default_factory=list)


class CampaignGenerationResponse(BaseModel):
    campaigns: list