from __future__ import annotations
from app.config.supabase_client import supabase
from app.ai.groq_client import groq_generate_response


# Dummy profiles — remove when sector/expertise fields are populated in DB
DUMMY_NGO_PROFILES: dict[str, dict] = {
    "Hope Foundation NGO": {
        "cause_tags":          ["Education", "Women Empowerment", "Digital Literacy", "Healthcare"],
        "expertise":           ["Skill Training", "Rural Development", "Youth Programs", "Community Health"],
        "past_projects_count": 12,
    },
}

# Signal weights — must sum to 1.0
WEIGHTS = {
    "cause_alignment":    0.35,
    "geography":          0.25,
    "impact_score":       0.15,
    "expertise_match":    0.15,
    "verification_score": 0.10,
}

_METRO_GROUPS: dict[str, list[str]] = {
    "mumbai":    ["mumbai", "thane", "navi mumbai", "pune", "maharashtra"],
    "delhi":     ["delhi", "new delhi", "noida", "gurgaon", "faridabad", "ghaziabad", "delhi ncr"],
    "bangalore": ["bangalore", "bengaluru", "mysore", "karnataka"],
    "chennai":   ["chennai", "coimbatore", "tamil nadu"],
    "hyderabad": ["hyderabad", "secunderabad", "telangana"],
    "kolkata":   ["kolkata", "howrah", "west bengal"],
}

# Handles known typos in DB state values
_STATE_ALIASES: dict[str, str] = {
    "maharashta":  "maharashtra",
    "maharashtra": "maharashtra",
    "delhi":       "delhi",
    "karnataka":   "karnataka",
}


def _normalise(text: str) -> str:
    return (text or "").strip().lower()


def _geography_score(campaign_region: str, ngo_city: str, ngo_state: str) -> float:
    cr = _normalise(campaign_region)
    nc = _normalise(ngo_city)
    ns = _STATE_ALIASES.get(_normalise(ngo_state), _normalise(ngo_state))

    if not cr:
        return 0.3
    if cr in ("pan india", "all india", "india"):
        return 0.6
    if cr == nc or cr in nc or nc in cr:
        return 1.0
    for group in _METRO_GROUPS.values():
        if any(cr in g or g in cr for g in group) and any(nc in g or g in nc for g in group):
            return 0.8
    if ns and (ns in cr or cr in ns):
        return 0.6
    return 0.1


def _cause_alignment_score(campaign_cause: str, cause_tags: list[str]) -> float:
    if not cause_tags:
        return 0.0
    campaign_words = set(_normalise(campaign_cause).split())
    matched = sum(
        1 for tag in cause_tags
        if any(word in _normalise(tag) for word in campaign_words)
        or any(word in campaign_words for word in _normalise(tag).split())
    )
    return min(matched / len(cause_tags), 1.0)


def _expertise_match_score(campaign: dict, expertise: list[str]) -> float:
    if not expertise:
        return 0.0
    campaign_text = _normalise(" ".join(filter(None, [
        campaign.get("cause", ""),
        campaign.get("schedule_vii", ""),
        campaign.get("title", ""),
    ])))
    matched = sum(
        1 for skill in expertise
        if any(word in campaign_text for word in _normalise(skill).split())
    )
    return min(matched / len(expertise), 1.0)


def _impact_score(past_projects_count: int) -> float:
    # Normalised to 0-1, capped at 20 projects
    return min(past_projects_count / 20.0, 1.0)


def _verification_score(ngo: dict) -> float:
    # verified=0.4, registration_number=0.3, registration_type=0.1, fcra_number=0.2
    score = 0.4
    if ngo.get("registration_number"):
        score += 0.3
    if ngo.get("registration_type"):
        score += 0.1
    if ngo.get("fcra_number"):
        score += 0.2
    return min(score, 1.0)


async def _generate_match_reason(campaign: dict, ngo: dict, signals: dict) -> str:
    prompt = f"""Write one sentence explaining why this NGO matches this CSR campaign.
Be specific. Use only the data given. No invented details.

Campaign:
- Title: {campaign.get('title')}
- Cause: {campaign.get('cause')}
- Region: {campaign.get('region')}
- Schedule VII: {campaign.get('schedule_vii')}

NGO:
- Name: {ngo.get('ngo_name')}
- City: {ngo.get('city')}, {ngo.get('state_province')}
- Registration: {ngo.get('registration_type')}
- FCRA: {'Yes' if ngo.get('fcra_number') else 'No'}

Match signal scores (0 to 1):
- Cause alignment:    {signals['cause_alignment']:.2f}
- Geography:          {signals['geography']:.2f}
- Impact score:       {signals['impact_score']:.2f}
- Expertise match:    {signals['expertise_match']:.2f}
- Verification score: {signals['verification_score']:.2f}

Return ONLY one sentence. No quotes. End with a period."""

    try:
        return (await groq_generate_response(prompt)).strip()
    except Exception:
        top_signal = max(signals, key=signals.get)
        labels = {
            "cause_alignment":    f"strong alignment with {campaign.get('cause')} cause",
            "geography":          f"regional presence in {ngo.get('city')}",
            "impact_score":       "strong past project track record",
            "expertise_match":    "relevant expertise for this campaign type",
            "verification_score": "fully verified with FCRA compliance",
        }
        return (
            f"{ngo.get('ngo_name')} was matched due to "
            f"{labels.get(top_signal, 'strong overall compatibility')} "
            f"with the {campaign.get('title')} campaign."
        )


def _fetch_verified_ngos() -> list[dict]:
    response = (
        supabase
        .from_("ngo_verifications")
        .select(
            "id, user_id, ngo_name, sector, verification_status, "
            "registration_number, registration_type, fcra_number, "
            "users!inner(id, city, state_province, location)"
        )
        .eq("verification_status", "verified")
        .execute()
    )
    ngos = []
    for row in (response.data or []):
        user = row.get("users") or {}
        ngos.append({
            "ngo_id":              row["user_id"],
            "ngo_name":            row.get("ngo_name"),
            "sector":              row.get("sector"),
            "verification_status": row.get("verification_status"),
            "registration_number": row.get("registration_number"),
            "registration_type":   row.get("registration_type"),
            "fcra_number":         row.get("fcra_number"),
            "city":                user.get("city"),
            "state_province":      user.get("state_province"),
            "location":            user.get("location"),
        })
    return ngos


def _apply_dummy_profile(ngo: dict) -> dict:
    # Remove this function when sector/expertise fields are populated in DB
    patch = DUMMY_NGO_PROFILES.get(ngo.get("ngo_name", ""), {})
    ngo["cause_tags"]          = patch.get("cause_tags", [ngo.get("sector")] if ngo.get("sector") else [])
    ngo["expertise"]           = patch.get("expertise", [])
    ngo["past_projects_count"] = patch.get("past_projects_count", 0)
    return ngo


async def match_ngos_to_campaign(campaign: dict, top_n: int = 5) -> list[dict]:
    ngos = _fetch_verified_ngos()

    if not ngos:
        return []

    campaign_cause  = campaign.get("cause", "")
    campaign_region = campaign.get("region", "")
    scored: list[dict] = []

    for ngo in ngos:
        ngo = _apply_dummy_profile(ngo)

        signals = {
            "cause_alignment":    _cause_alignment_score(campaign_cause, ngo.get("cause_tags", [])),
            "geography":          _geography_score(campaign_region, ngo.get("city", ""), ngo.get("state_province", "")),
            "impact_score":       _impact_score(ngo.get("past_projects_count", 0)),
            "expertise_match":    _expertise_match_score(campaign, ngo.get("expertise", [])),
            "verification_score": _verification_score(ngo),
        }

        composite = sum(score * WEIGHTS[signal] for signal, score in signals.items())

        scored.append({
            "_ngo":       ngo,
            "_signals":   signals,
            "_composite": composite,
        })

    scored.sort(key=lambda x: x["_composite"], reverse=True)
    top_candidates = scored[:top_n]

    results: list[dict] = []
    for item in top_candidates:
        ngo     = item["_ngo"]
        signals = item["_signals"]
        match_reason = await _generate_match_reason(campaign, ngo, signals)

        results.append({
            "ngo_id":            ngo["ngo_id"],
            "ngo_name":          ngo["ngo_name"],
            "city":              ngo.get("city"),
            "state_province":    ngo.get("state_province"),
            "cause_tags":        ngo.get("cause_tags", []),
            "expertise":         ngo.get("expertise", []),
            "registration_type": ngo.get("registration_type"),
            "fcra_verified":     bool(ngo.get("fcra_number")),
            "verification_status": ngo.get("verification_status"),
            "composite_score":   round(item["_composite"], 4),
            "signal_breakdown": {
                "cause_alignment":    round(signals["cause_alignment"], 4),
                "geography":          round(signals["geography"], 4),
                "impact_score":       round(signals["impact_score"], 4),
                "expertise_match":    round(signals["expertise_match"], 4),
                "verification_score": round(signals["verification_score"], 4),
            },
            "match_reason": match_reason,
        })

    return results