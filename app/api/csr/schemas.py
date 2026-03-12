from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class CSRAgentRequest(BaseModel):
    session_id: str
    message: str
    context: Optional[Dict[str, Any]] = None
class CSRAgentResponse(BaseModel):
    pass
