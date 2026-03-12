from fastapi import APIRouter
from schemas import CSRAgentRequest, CSRAgentResponse
from app.agents.csr_agent import CSRAgent

router = APIRouter(
    prefix = "/csr",
    tags = ["CSR Services Navadrishti API"],  
)

@router.post("/chat", status_code=200, response_model=CSRAgentResponse)
async def chat(request: CSRAgentRequest):
    # Placeholder for the actual implementation
    return CSRAgentResponse(
        response_text="This is a placeholder response.",
        next_step="collect_budget"
    )

