from unittest import result

from app.shared.clients.supabase_client import supabase

class SelectedCampaignsService:
    def __init__(self):
        pass

    def get_selected_campaigns(self, ngo_id: str):
        pass

    def store_selected_campaign(self,campaign: dict, company_id: str | None) -> dict:

        result = supabase.table("campaigns").insert({
            "title":            campaign.get("title"),
            "description":      campaign.get("description"),
            "category":         campaign.get("category"),
            "location":         campaign.get("location"),
            "budget_inr":       campaign.get("estimated_budget"),
            "budget_breakdown": campaign.get("budgetBreakdown"),
            "schedule_vii":     campaign.get("scheduleVII"),
            "sdg_alignment":    campaign.get("sdgAlignment"),
            "impact_metrics":   campaign.get("impactMetrics"),
            "milestones":       campaign.get("milestones"),
            "start_date":       campaign.get("start_date"),
            "end_date":         campaign.get("end_date"),
            "company_id":       company_id,
        }).execute()
        print(result)
        print(result.data)
        return result.data[0]