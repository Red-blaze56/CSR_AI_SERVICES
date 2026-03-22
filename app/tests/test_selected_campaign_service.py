import uuid
from app.modules.selected_camapigns.service import SelectedCampaignsService
from app.shared.clients.supabase_client import supabase

scs = SelectedCampaignsService()

def test_store_selected_campaign_inserts_data():

    company_id = 1

    campaign = {
        "title": "TEST_CAMPAIGN",
        "description": "Testing DB insert",
        "category": "education",
        "location": "Delhi",
        "estimated_budget": 100000,
        "budgetBreakdown": {
            "infrastructure": 20000,
            "training": 20000,
            "materials": 20000,
            "monitoring": 20000,
            "contingency": 20000
        },
        "scheduleVII": "Education",
        "sdgAlignment": [4],
        "impactMetrics": {
            "beneficiaries": 100
        },
        "milestones": [],
        "start_date": "2026-01-01",
        "end_date": "2026-03-01",
    }

    #call function
    inserted = scs.store_selected_campaign(campaign, company_id)

    #basic checks
    assert inserted is not None
    assert inserted["title"] == "TEST_CAMPAIGN"
    assert inserted["company_id"] == company_id

    # fetch from DB (real verification)
    db_response = supabase.table("campaigns") \
        .select("*") \
        .eq("id", inserted["id"]) \
        .execute()

    assert len(db_response.data) == 1

    row = db_response.data[0]

    # field-level checks
    assert row["title"] == campaign["title"]
    assert row["category"] == campaign["category"]
    assert row["location"] == campaign["location"]
    assert row["budget_inr"] == campaign["estimated_budget"]
    assert row["company_id"] == company_id

    # cleanup (important)
    supabase.table("campaigns") \
        .delete() \
        .eq("id", inserted["id"]) \
        .execute()