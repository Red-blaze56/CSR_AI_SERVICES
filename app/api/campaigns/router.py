from fastapi import APIRouter
from app.api.campaigns.schemas import CampaignGenerationRequest, CampaignGenerationResponse
from app.api.campaigns.campaigns_service import generate_campaigns

campaigns_router = APIRouter(tags=["Campaign Generation"])

@campaigns_router.post("/generate-campaigns", status_code=200, response_model=CampaignGenerationResponse)
async def generating_campaign(request: CampaignGenerationRequest):
    campaigns = await generate_campaigns(request.model_dump())
    return CampaignGenerationResponse(campaigns=campaigns)