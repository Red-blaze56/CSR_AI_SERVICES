from __future__ import annotations
from app.config.supabase_client import supabase
from app.ai.gemini_client import gemini_generate_response
from app.utils.json_parser import parse_json
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")

COST_LIBRARY = {
    "education_kit":  500,
    "meal_per_person": 30,
    "blanket":        300,
    "teacher_daily":  800,
    "water_filter":   1500,
    "medical_kit":    1200,
    "sanitation_unit": 5000,
    "volunteer_daily": 600,
}

LOCATION_MULTIPLIERS = {
    "urban":  1.20,
    "rural":  1.00,
    "remote": 1.30,
}

URGENCY_MULTIPLIERS = {
    "low":    1.00,
    "medium": 1.05,
    "high":   1.15,
}

KEYWORD_TO_REQUEST_TYPE = {
    "money":          "financial",
    "funding":        "financial",
    "fund":           "financial",
    "grant":          "financial",
    "kits":           "material",
    "food":           "material",
    "clothes":        "material",
    "blankets":       "material",
    "material":       "material",
    "supplies":       "material",
    "training":       "service",
    "teachers":       "service",
    "volunteers":     "service",
    "coaching":       "service",
    "build":          "infrastructure",
    "construction":   "infrastructure",
    "infrastructure": "infrastructure",
    "repair":         "infrastructure",
}

KEYWORD_TO_CATEGORY = {
    "school":      "Education",
    "education":   "Education",
    "children":    "Education",
    "students":    "Education",
    "hospital":    "Healthcare",
    "health":      "Healthcare",
    "medical":     "Healthcare",
    "camp":        "Healthcare",
    "water":       "Sanitation",
    "sanitation":  "Sanitation",
    "toilet":      "Sanitation",
    "women":       "Women Empowerment",
    "girl":        "Women Empowerment",
    "gender":      "Women Empowerment",
    "food":        "Hunger & Nutrition",
    "meal":        "Hunger & Nutrition",
    "hunger":      "Hunger & Nutrition",
    "environment": "Environment",
    "tree":        "Environment",
    "rural":       "Rural Development",
    "village":     "Rural Development",
    "skill":       "Skill Development",
    "vocational":  "Skill Development",
}

EVIDENCE_RULES = {
    "financial":      ["utilization certificate", "invoices"],
    "material":       ["photos", "distribution list"],
    "service":        ["attendance logs"],
    "infrastructure": ["progress photos", "completion proof"],
}


def _detect_request_type(text: str) -> str:
    text = text.lower()
    for keyword, request_type in KEYWORD_TO_REQUEST_TYPE.items():
        if keyword in text:
            return request_type
    return "service"


def _detect_category(text: str) -> str:
    text = text.lower()
    for keyword, category in KEYWORD_TO_CATEGORY.items():
        if keyword in text:
            return category
    return "General"


def _detect_location_type(location: str) -> str:
    location = location.lower()
    urban_keywords  = ["mumbai", "delhi", "bangalore", "chennai", "hyderabad", "kolkata", "pune"]
    remote_keywords = ["tribal", "remote", "forest", "hills", "northeast"]
    if any(k in location for k in urban_keywords):
        return "urban"
    if any(k in location for k in remote_keywords):
        return "remote"
    return "rural"


def _estimate_budget(
    request_type: str,
    beneficiary_count: int,
    location: str,
    urgency: str,
    problem_statement: str,
) -> float:
    text = problem_statement.lower()
    unit_cost = None

    for item, cost in COST_LIBRARY.items():
        if any(word in text for word in item.split("_")):
            unit_cost = cost
            break

    if unit_cost is None:
        defaults = {
            "financial":      500,
            "material":       400,
            "service":        600,
            "infrastructure": 2000,
        }
        unit_cost = defaults.get(request_type, 500)

    base_budget   = unit_cost * beneficiary_count
    location_type = _detect_location_type(location)
    location_mult = LOCATION_MULTIPLIERS.get(location_type, 1.0)
    urgency_mult  = URGENCY_MULTIPLIERS.get(urgency, 1.0)

    if request_type == "infrastructure":
        base_budget *= 1.30

    return round(base_budget * location_mult * urgency_mult, 2)


def _confidence_score(structured: dict) -> float:
    score = 0.0
    if structured.get("title"):              score += 0.20
    if structured.get("description"):        score += 0.15
    if structured.get("request_type"):       score += 0.15
    if structured.get("category"):           score += 0.15
    if structured.get("location"):           score += 0.10
    if structured.get("beneficiary_count"):  score += 0.10
    if structured.get("estimated_budget"):   score += 0.10
    if structured.get("impact_description"): score += 0.05
    return round(min(score, 1.0), 2)


def _validate(structured: dict) -> tuple[bool, str]:
    if not structured.get("beneficiary_count") or structured["beneficiary_count"] <= 0:
        return False, "Beneficiary count must be greater than 0."
    if not structured.get("location"):
        return False, "Location is required."
    if not structured.get("request_type"):
        return False, "Could not detect request type from input."
    if structured.get("request_type") == "financial" and not structured.get("estimated_budget"):
        return False, "Budget is required for financial requests."
    if structured.get("request_type") == "service" and not structured.get("requirements"):
        return False, "Skills required must be specified for service requests."
    if structured.get("request_type") == "infrastructure":
        structured["tags"] = structured.get("tags", []) + ["multi-phase"]
    return True, ""


def _build_embed_text(structured: dict) -> str:
    return (
        f"{structured.get('title', '')}. "
        f"{structured.get('description', '')}. "
        f"Category: {structured.get('category', '')}. "
        f"Location: {structured.get('location', '')}. "
        f"Type: {structured.get('request_type', '')}. "
        f"Impact: {structured.get('impact_description', '')}."
    )


def _embed(text: str) -> list[float]:
    return _model.encode(text, convert_to_numpy=True).tolist()


async def _extract_with_gemini(input_data: dict) -> dict:
    problem  = input_data.get("problem_statement", "")
    location = input_data.get("location", "")
    count    = input_data.get("beneficiary_count", 0)
    urgency  = input_data.get("urgency", "medium")
    timeline = input_data.get("timeline", "")
    notes    = input_data.get("additional_notes", "")

    request_type = _detect_request_type(problem)
    category     = _detect_category(problem)
    budget       = _estimate_budget(request_type, count, location, urgency, problem)
    impact       = f"Directly benefits {count} people in {location} under {category}."
    evidence     = EVIDENCE_RULES.get(request_type, [])

    prompt = f"""You are structuring an NGO service request. Extract a clean title and description.

Problem statement: {problem}
Location: {location}
Beneficiaries: {count}
Urgency: {urgency}
Timeline: {timeline}
Notes: {notes}

Return ONLY this JSON:
{{
  "title": "concise request title",
  "description": "2-3 sentence description of what is needed and why"
}}"""

    try:
        raw    = await gemini_generate_response(prompt)
        parsed = parse_json(raw)
    except Exception:
        parsed = {
            "title":       f"{category} support for {count} beneficiaries in {location}",
            "description": problem,
        }

    return {
        "title":              parsed.get("title", ""),
        "description":        parsed.get("description", ""),
        "request_type":       request_type,
        "category":           category,
        "location":           location,
        "beneficiary_count":  count,
        "estimated_budget":   budget,
        "budget_currency":    "INR",
        "impact_description": impact,
        "urgency_level":      urgency,
        "required_by_date":   timeline or None,
        "evidence_required":  evidence,
        "requirements":       {},
        "tags":               [],
        "timeline":           timeline,
    }


async def _generate_suggestions(structured: dict) -> list[str]:
    suggestions = []
    if not structured.get("timeline"):
        suggestions.append("Add a timeline for better campaign matching.")
    if structured.get("estimated_budget", 0) < 10000:
        suggestions.append("Budget seems low for this scope — consider reviewing.")
    if structured.get("beneficiary_count", 0) > 500 and structured.get("urgency_level") == "low":
        suggestions.append("Large beneficiary count — consider raising urgency level.")
    if not structured.get("requirements"):
        suggestions.append("Add specific skill or resource requirements for better matching.")
    return suggestions


def _save_to_db(ngo_id: int, structured: dict) -> int:
    embed_text = _build_embed_text(structured)
    embedding  = _embed(embed_text)

    response = (
        supabase
        .table("service_requests")
        .insert({
            "ngo_id":             ngo_id,
            "title":              structured.get("title"),
            "description":        structured.get("description"),
            "category":           structured.get("category"),
            "location":           structured.get("location"),
            "request_type":       structured.get("request_type"),
            "estimated_budget":   structured.get("estimated_budget"),
            "budget_currency":    structured.get("budget_currency", "INR"),
            "beneficiary_count":  structured.get("beneficiary_count"),
            "impact_description": structured.get("impact_description"),
            "urgency_level":      structured.get("urgency_level"),
            "deadline":           structured.get("required_by_date"),
            "timeline":           structured.get("timeline"),
            "requirements":       structured.get("requirements", {}),
            "tags":               structured.get("tags", []),
            "status":             "open",
        })
        .execute()
    )

    request_id = response.data[0]["id"]

    # Stored in campaign_embeddings with source tag until dedicated table is created
    # location and estimated_budget included for pre-filtering before vector search
    supabase.table("campaign_embeddings").insert({
        "campaign_id": None,
        "embedding":   embedding,
        "metadata": {
            "source":           "ngo_request",
            "request_id":       request_id,
            "title":            structured.get("title"),
            "category":         structured.get("category"),
            "location":         structured.get("location"),
            "request_type":     structured.get("request_type"),
            "estimated_budget": structured.get("estimated_budget"),
            "budget_currency":  structured.get("budget_currency", "INR"),
        },
        "version": 1,
    }).execute()

    return request_id


async def process_ngo_request(ngo_id: int, input_data: dict) -> dict:
    if not input_data.get("problem_statement"):
        return {"error": "Problem statement is required."}
    if not input_data.get("location"):
        return {"error": "Location is required."}
    if not input_data.get("beneficiary_count") or input_data["beneficiary_count"] <= 0:
        return {"error": "Valid beneficiary count is required."}

    structured = await _extract_with_gemini(input_data)

    is_valid, error_msg = _validate(structured)
    if not is_valid:
        return {"error": error_msg}

    structured["confidence_score"] = _confidence_score(structured)
    suggestions = await _generate_suggestions(structured)

    return {
        "status":      "draft",
        "structured":  structured,
        "suggestions": suggestions,
    }


async def confirm_ngo_request(ngo_id: int, structured: dict) -> dict:
    request_id = _save_to_db(ngo_id, structured)
    return {
        "status":     "saved",
        "request_id": request_id,
        "message":    "Request saved and embedded into RAG successfully.",
    }