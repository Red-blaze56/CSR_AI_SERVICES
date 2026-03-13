STEP_FLOW = {
    "welcome":"budget",
    "budget":"cause",
    "cause":"region",
    "region":"timeline",
    "timeline":"employee_engagement",
    "employee_engagement":"generating_ideas",
}

SUGGESTIONS = {
    "budget": ["₹50,000", "₹1 Lakh", "₹2 Lakh", "₹5 Lakh"],
    "cause": ["Women Empowerment", "Education", "Environment", "Healthcare"],
    "region": ["Delhi NCR", "Mumbai", "Bangalore", "Pan India"],
    "timeline": ["3 months", "6 months", "12 months"],
    "employee_engagement": ["Yes", "No"],
}

PROMPTS = {
    "budget": "What is your CSR budget?",
    "cause": "Which cause would you like to support?",
    "region": "Which region should the campaign focus on?",
    "timeline": "What timeline are you considering for the campaign?",
    "employee_engagement": "Would employees participate in volunteering?"
}