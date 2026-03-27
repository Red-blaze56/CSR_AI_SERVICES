from fastapi import APIRouter
from app.api.ngo_agent.schemas import (
    NGORequestInput,
    NGORequestConfirm,
    NGORequestDraftResponse,
    NGORequestSavedResponse,
)
from app.services.ngo_agent import process_ngo_request, confirm_ngo_request

ngo_agent_router = APIRouter(tags=["NGO Agent"])


@ngo_agent_router.post(
    "/ngo-agent/structure",
    status_code=200,
    response_model=NGORequestDraftResponse,
)
async def structure_request(request: NGORequestInput):
    result = await process_ngo_request(
        ngo_id=request.ngo_id,
        input_data=request.model_dump(),
    )
    return NGORequestDraftResponse(**result)


@ngo_agent_router.post(
    "/ngo-agent/confirm",
    status_code=200,
    response_model=NGORequestSavedResponse,
)
async def confirm_request(request: NGORequestConfirm):
    result = await confirm_ngo_request(
        ngo_id=request.ngo_id,
        structured=request.structured,
    )
    return NGORequestSavedResponse(**result)