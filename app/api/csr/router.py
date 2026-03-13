from fastapi import APIRouter
from app.agents.csr_agent.agent import process_csr_chat
from app.api.csr.schemas import CSRAgentRequest, CSRAgentResponse

csr_router = APIRouter(
    prefix = "/csr",
    tags = ["CSR Services Navadrishti API"],  
)

@csr_router.post("/chat", status_code=200, response_model=CSRAgentResponse)
async def chat(request: CSRAgentRequest):
    return await process_csr_chat(request)

