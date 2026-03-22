from fastapi import APIRouter, HTTPException
from app.modules.selected_camapigns.schema import SelectedCampaignIn,SelectedCampaignResponse

from app.modules.selected_camapigns.service import selected_campaign_service

select_campaign_router = APIRouter(
    prefix="/selected-campaign",
    tags=["Selected Campaign"],
)

@select_campaign_router.post("/save_campaign", response_model=SelectedCampaignResponse)
async def select_campaign(req: SelectedCampaignIn) -> SelectedCampaignResponse:
    try:
        return await selected_campaign_service.select(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@select_campaign_router.get("/update_campaign/{company_id}")
async def update_campaign(company_id: str) -> SelectedCampaignResponse:
    try:
        return await selected_campaign_service.update(company_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))