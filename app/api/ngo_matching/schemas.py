from pydantic import BaseModel, Field
from typing import Optional


class CampaignInput(BaseModel):
    """
    Matches the output shape of /generate-campaigns.
    The TypeScript backend passes one selected campaign here.
    """
    title:           Optional[str]       = None
    cause:           Optional[str]       = None
    region:          Optional[str]       = None
    schedule_vii:    Optional[str]       = None
    sdg_alignment:   Optional[list[int]] = None
    impact_metrics:  Optional[dict]      = None
    budget_breakdown: Optional[dict]     = None


class NGOMatchRequest(BaseModel):
    campaign: CampaignInput
    top_n:    int = Field(default=5, ge=1, le=10)


class SignalBreakdown(BaseModel):
    cause_alignment:    float
    geography:          float
    impact_score:       float
    expertise_match:    float
    verification_score: float


class NGOMatch(BaseModel):
    ngo_id:              int
    ngo_name:            str
    city:                Optional[str]       = None
    state_province:      Optional[str]       = None
    cause_tags:          Optional[list[str]] = None
    expertise:           Optional[list[str]] = None
    registration_type:   Optional[str]       = None
    fcra_verified:       bool
    verification_status: str
    composite_score:     float
    signal_breakdown:    SignalBreakdown
    match_reason:        str


class NGOMatchResponse(BaseModel):
    matches: list[NGOMatch]