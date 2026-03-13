from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class Action(str, Enum):
    budget = "collect_budget"
    cause = "collect_cause"
    region = "collect_region"
    timeline = "timeline"
    employee_engagement = "employee_engagement"
    generate_ideas = "generate_ideas"
    complete = "complete"

class UserProfile(BaseModel):
    company_id: int
    company_name: str
    industry: Optional[str] = None
    company_size: Optional[str] = None

class CSRContext(BaseModel):
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    current_step: str = Field(default="welcome")
    preferences_collected: Dict[str, Any] = Field(default_factory=dict)
    user_profile: UserProfile

class CSRAgentRequest(BaseModel):
    session_id: int
    message: str
    context: CSRContext

class CSRAgentResponse(BaseModel):
    response_text: str
    next_step: str
    action: Optional[Action] = None
    extracted_data: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None
    confidence: Optional[float] = None

    
'''
interface CSRAgentRequest {
  session_id: number;
  message: string;
  context: {
    conversation_history: Message[];
    current_step: string;
    preferences_collected: Record<string, any>;
    user_profile: {
      company_id: number;
      company_name: string;
      industry?: string;
      company_size?: string;
    };
  };
}

interface CSRAgentResponse {
  response_text: string;
  next_step: string;
  action?: 
    | 'collect_budget'
    | 'collect_cause'
    | 'collect_region'
    | 'generate_ideas'
    | 'timeline'
    | 'employee_engagement'
    | 'complete';

  extracted_data?: Record<string, any>;
  suggestions?: string[];
  confidence?: number;
}
'''

