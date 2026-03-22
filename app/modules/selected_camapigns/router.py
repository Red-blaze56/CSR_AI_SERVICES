from fastapi import APIRouter, HTTPException
from app.modules.selected_camapigns.schema import SelectedCampaignIn, SelectedCampaignResponse, UpdateSelectedCampaign
from app.modules.selected_camapigns.service import SelectedCampaignsService

selected_campaign_router = APIRouter(
    prefix="/selected-campaign",
    tags=["Selected Campaign"],
)

scs=SelectedCampaignsService()

@selected_campaign_router.post("/save_campaign", response_model=SelectedCampaignResponse)
async def select_campaign(req: SelectedCampaignIn) -> SelectedCampaignResponse:
    inserted = scs.store_selected_campaign(
        campaign=req.campaign.model_dump(),
        company_id=req.company_id
    )
    return SelectedCampaignResponse(
        id=inserted["id"],
        title=inserted["title"],
        status=inserted["status"],
        message="Campaign saved successfully"
    )


@selected_campaign_router.put("/update_campaign/{campaign_id}")
async def update_campaign(campaign_id: str, req: UpdateSelectedCampaign) -> SelectedCampaignResponse:
    updates = {}
    if req.campaign is not None:
        updates = req.campaign.model_dump(exclude_none=True, exclude_unset=True)

    updated = scs.update_selected_campaign(
        campaign_id=campaign_id,
        updates=updates,
        company_id=req.company_id
    )
    return SelectedCampaignResponse(
        id=updated["id"],
        title=updated["title"],
        status=updated["status"],
        message="Campaign updated successfully"
    )