from fastapi import APIRouter
from schema import CampaignGenerationRequest, CampaignGenerationResponse
from services import generate_campaigns

campaigns_router = APIRouter(tags=["Campaign Generation"])

@campaigns_router.get("/health", status_code=200)
async def health_check():
    return {"status": "ok"}

@campaigns_router.post("/generate-campaigns", status_code=200, response_model=CampaignGenerationResponse)
async def generating_campaign(request: CampaignGenerationRequest):
    campaigns = await generate_campaigns(request.model_dump())
    return CampaignGenerationResponse(campaigns=campaigns)