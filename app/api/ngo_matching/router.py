from fastapi import APIRouter
from app.api.ngo_matching.schemas import NGOMatchRequest, NGOMatchResponse
from app.services.ngo_matcher import match_ngos_to_campaign

ngo_matching_router = APIRouter(tags=["NGO Matching"])


@ngo_matching_router.post(
    "/match-ngos",
    status_code=200,
    response_model=NGOMatchResponse,
)
async def match_ngos(request: NGOMatchRequest):
    matches = await match_ngos_to_campaign(
        campaign=request.campaign.model_dump(),
        top_n=request.top_n,
    )
    return NGOMatchResponse(matches=matches)