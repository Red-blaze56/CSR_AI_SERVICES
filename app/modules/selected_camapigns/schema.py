from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Literal
from datetime import date


class BudgetBreakdown(BaseModel):
    infrastructure: int
    training:       int
    materials:      int
    monitoring:     int
    contingency:    int

    def total(self) -> int:
        return (
            self.infrastructure +
            self.training       +
            self.materials      +
            self.monitoring     +
            self.contingency
        )


class Impact(BaseModel):
    beneficiaries: int
    start_date:    date
    end_date:      date


class Milestone(BaseModel):
    title:            str
    description:      str
    target_date:      date
    duration_weeks:   int
    budget_allocated: int
    risk_level:       Literal["High", "Medium", "Low"]
    risk_reason:      str
    deliverables:     List[str]
    success_metric:   str


class SelectedCampaignIn(BaseModel):
    campaign:   dict          # raw campaign from generate step
    company_id: Optional[str] = None


class SelectedCampaignResponse(BaseModel):
    id:         str
    title:      str
    status:     str
    message:    str