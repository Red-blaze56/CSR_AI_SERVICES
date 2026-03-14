from app.api.csr.schemas import CSRAgentRequest, CSRAgentResponse, Action
from app.api.csr.csr_service import extract_preferences
from app.api.campaigns.campaigns_service import generate_campaigns
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
    
    # this stores all the extracted data w.r.t the steps in the preferences dictionary
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
    if next_step == "complete":
        return CSRAgentResponse(
            response_text="Great! I have collected all your CSR preferences.",
            next_step="complete",
            action=Action.complete,
            extracted_data=preferences,
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