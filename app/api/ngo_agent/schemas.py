from pydantic import BaseModel, Field
from typing import Optional


class NGORequestInput(BaseModel):
    ngo_id:             int
    problem_statement:  str
    location:           str
    beneficiary_count:  int
    urgency:            str = Field(default="medium", pattern="^(low|medium|high)$")
    timeline:           Optional[str] = None
    additional_notes:   Optional[str] = None


class NGORequestConfirm(BaseModel):
    ngo_id:     int
    structured: dict


class NGORequestDraftResponse(BaseModel):
    status:      str
    structured:  Optional[dict] = None
    suggestions: Optional[list[str]] = None
    error:       Optional[str] = None


class NGORequestSavedResponse(BaseModel):
    status:     str
    request_id: Optional[int] = None
    message:    Optional[str] = None
    error:      Optional[str] = None