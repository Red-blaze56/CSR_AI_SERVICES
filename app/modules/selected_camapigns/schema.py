from pydantic import BaseModel, Field
from typing import Optional, List


class BudgetBreakdown(BaseModel):
    infrastructure: Optional[float] = Field(0, ge=0)
    training: Optional[float] = Field(0, ge=0)
    materials: Optional[float] = Field(0, ge=0)
    monitoring: Optional[float] = Field(0, ge=0)
    contingency: Optional[float] = Field(0, ge=0)


class ImpactMetrics(BaseModel):
    beneficiaries: int
    duration: str


class Milestone(BaseModel):
    title:            str
    description:      str
    duration_weeks:   int
    budget_allocated: float
    deliverables:     List[str]


class CampaignDraft(BaseModel):
    title:            str
    description:      str
    category:         str
    location:         str
    estimated_budget: int
    budgetBreakdown:  BudgetBreakdown
    scheduleVII:      str
    sdgAlignment:     List[int]
    start_date:       str
    end_date:         str
    impactMetrics:    ImpactMetrics
    milestones:       List[Milestone]


class UpdateImpactMetrics(BaseModel):
    beneficiaries: Optional[int] = None
    duration: Optional[str] = None


class UpdateMilestone(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_weeks: Optional[int] = None
    budget_allocated: Optional[float] = None
    deliverables: Optional[List[str]] = None


class UpdateCampaignDraft(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    estimated_budget: Optional[int] = None
    budgetBreakdown: Optional[BudgetBreakdown] = None
    scheduleVII: Optional[str] = None
    sdgAlignment: Optional[List[int]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    impactMetrics: Optional[UpdateImpactMetrics] = None
    milestones: Optional[List[UpdateMilestone]] = None


class SelectedCampaignIn(BaseModel):
    campaign:   CampaignDraft
    company_id: Optional[str] = None


class SelectedCampaignResponse(BaseModel):
    id:      str
    title:   str
    status:  str
    message: str

class UpdateSelectedCampaign(BaseModel):
    campaign: Optional[UpdateCampaignDraft] = None
    company_id: Optional[str] = None
