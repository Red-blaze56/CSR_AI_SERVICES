from app.api.csr.schemas import CSRAgentRequest, CSRAgentResponse, Action
from app.ai.service import generate_campaigns, extract_preferences
from app.agents.csr_agent.converstaion_flow import STEP_FLOW, PROMPTS, SUGGESTIONS

STEP_TO_ACTION = {
    "budget": Action.budget,
    "cause": Action.cause,
    "region": Action.region,
    "timeline": Action.timeline,
    "employee_engagement": Action.employee_engagement,
}


async def process_csr_chat(request: CSRAgentRequest) -> CSRAgentResponse:

    message = request.message
    context = request.context

    current_step = context.current_step
    preferences = dict(context.preferences_collected or {})

    # Welcome
    if current_step == "welcome":
        return CSRAgentResponse(
            response_text=PROMPTS["budget"],
            next_step="budget",
            action=Action.budget,
            suggestions=SUGGESTIONS.get("budget", []),
            confidence=1.0
        )

    # Extract structured data
    extracted = await extract_preferences(message, current_step)

    if not extracted:
        return CSRAgentResponse(
            response_text=f"I couldn't understand your {current_step}. Could you clarify?",
            next_step=current_step,
            action=STEP_TO_ACTION.get(current_step),
            suggestions=SUGGESTIONS.get(current_step, []),
            confidence=0.6
        )

    if extracted.get("extracted_value") is None or extracted.get("is_valid") is False:
        return CSRAgentResponse(
            response_text=extracted.get("clarification_needed", f"I couldn't understand your {current_step}. Could you clarify?"),
            next_step=current_step,
            action=STEP_TO_ACTION.get(current_step),
            suggestions=SUGGESTIONS.get(current_step, []),
            confidence=0.6
        )
    
    preferences.update({current_step: extracted.get("extracted_value")})

    # Determine next step
    next_step = STEP_FLOW.get(current_step)

    if not next_step:
        return CSRAgentResponse(
            response_text="Something went wrong. Let's restart.",
            next_step="welcome",
            action=STEP_TO_ACTION.get(current_step),
            suggestions=SUGGESTIONS.get(current_step, []),
            confidence=0.3
        )

    # Generate campaigns
    if next_step == "generating_ideas":

        campaigns = await generate_campaigns(preferences)

        return CSRAgentResponse(
            response_text="Here are 3 CSR campaign ideas based on your preferences.",
            next_step="project_selection",
            action=Action.generate_ideas,
            extracted_data={"campaigns": campaigns},
            confidence=1.0
        )

    # Continue flow
    action = STEP_TO_ACTION.get(next_step)

    return CSRAgentResponse(
        response_text=PROMPTS.get(next_step, "Please continue."),
        next_step=next_step,
        action=action,
        extracted_data=preferences,
        suggestions=SUGGESTIONS.get(next_step, []),
        confidence=0.9
    )