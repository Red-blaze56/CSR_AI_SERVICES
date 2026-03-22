from fastapi import APIRouter, HTTPException
from app.modules.selected_camapigns.schema import SelectedCampaignIn,SelectedCampaignResponse
from app.modules.selected_camapigns.service import SelectedCampaignsService

selected_campaign_router = APIRouter(
    prefix="/selected-campaign",
    tags=["Selected Campaign"],
)
selected_campaign_service = SelectedCampaignsService()



@selected_campaign_router.post("/save_campaign", response_model=SelectedCampaignResponse)
async def select_campaign(req: SelectedCampaignIn) -> SelectedCampaignResponse:
    pass
    
@selected_campaign_router.get("/update_campaign/{company_id}")
async def update_campaign(company_id: str) -> SelectedCampaignResponse:
    pass