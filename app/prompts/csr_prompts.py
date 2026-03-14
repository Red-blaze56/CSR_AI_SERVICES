SCHEDULE_VII = """
Schedule VII Categories (Companies Act 2013):
i   - Hunger, poverty, malnutrition, health, sanitation
ii  - Education, vocational skills, livelihood
iii - Gender equality, women empowerment
iv  - Environment, ecology, conservation
v   - National heritage, art, culture
vi  - Armed forces veterans
vii - Rural/Olympic/Paralympic sports
viii- Technology incubators
ix  - Rural development
x   - Slum development
xi  - Disaster management
xii - Other (PM Relief Fund)
"""
 
# ── Prompt 1: Extract data from user message ──────────────────────────────────
# Gemini reads what the user typed and pulls out the actual value
 
def extract_prompt(current_step: str, message: str) -> str:
    return f"""The user is filling out a CSR campaign form step by step.
Current step: {current_step}
User just said: "{message}"
 
Extract the relevant value from the user's message for this step.
 
{SCHEDULE_VII if current_step == "cause" else ""}
 
Return ONLY this JSON:
{{
  "extracted_value": <the extracted value, correct type>,
  "is_valid": <true if you could extract a clear value, false if unclear>,
  "clarification_needed": "<if is_valid is false, what to ask the user>"
}}
 
Examples:
- step=collect_budget, message="around 2 lakhs" → {{"extracted_value": 200000, "is_valid": true}}
- step=collect_cause, message="women empowerment" → {{"extracted_value": "Women Empowerment", "is_valid": true, "schedule_vii": "iii"}}
- step=collect_region, message="delhi" → {{"extracted_value": "Delhi NCR", "is_valid": true}}
- step=collect_timeline, message="6 months" → {{"extracted_value": 6, "is_valid": true}}     
- step=collect_employee, message="yes" → {{"extracted_value": true, "is_valid": true}}
- step=collect_budget, message="I don't know" → {{"extracted_value": null, "is_valid": false, "clarification_needed": "Please enter a budget amount in INR (minimum ₹10,000)"}}

Additional instructions:
- For budget, extract a number in INR. If user gives a range, take the upper limit.
- For cause, match to one of the Schedule VII categories. If user gives a specific cause (e.g. education for underprivileged kids), map it to the closest category (e.g. Education).
- For region, match to one of the suggested regions. If user gives a city, map it to the corresponding region (e.g. Delhi → Delhi NCR).
- For timeline, convert number in months if in years.
- For employee involvement, interpret yes/true as true, no/false as false.
- If you can't extract a clear value, return is_valid=false and provide a clarification_needed message to ask the user for the specific information you need.
"""
 
 
# ── Prompt 2: Generate 3-4 campaign concepts ──────────────────────────────────
 
def generate_campaigns_prompt(preferences: dict) -> str:
  # handle both possible key names
  budget   = preferences.get('budget')
  cause    = preferences.get('cause')
  region   = preferences.get('region')
  timeline = preferences.get('timeline')
  employee = preferences.get('employee_engagement')
  print(f"Generating campaigns with preferences: {budget=}, {cause=}, {region=}, {timeline=}, {employee=}")
  return f"""You are an expert CSR strategist helping Indian companies design impactful CSR campaigns aligned with Schedule VII of the Companies Act 2013.

{SCHEDULE_VII}

Company Preferences:
- Budget:              ₹{budget} INR
- Cause:               {cause}
- Region:              {region}
- Timeline:            {timeline} months
- Employee Engagement:{employee}

Generate exactly 3 distinct CSR campaign concepts based on these preferences.

STRICT RULES:
- Each campaign MUST be aligned with a Schedule VII category
- estimated_budget MUST be ≤ ₹{budget}
- budget_breakdown values MUST sum exactly to estimated_budget
- All 3 campaigns MUST be meaningfully different from each other
- expected_beneficiaries MUST be an integer only — no text, no units
- Return ONLY valid JSON — no markdown, no extra text

Return ONLY this JSON:
{{
  "campaigns": [
    {{
      "title": "string",
      "description": "2-3 sentences about the approach and goal of this campaign",
      "budgetBreakdown": {{
        "infrastructure": 50000,
        "training": 40000,
        "materials": 35000,
        "monitoring": 15000,
        "contingency": 10000
      }},
      "scheduleVII": "e.g. Education",
      "sdgAlignment": [4, 8],
      "impactMetrics": {{
        "beneficiaries": 100,
        "duration": "{timeline} months"
      }},
      "milestones": [
        {{
          "title": "Setup & Onboarding",
          "description": "Identify beneficiaries, set up required infrastructure",
          "duration_weeks": 2,
          "budget_allocated": 20000,
          "deliverables": [
            "Beneficiary list finalized",
            "Infrastructure ready"
          ]
        }},
        {{
          "title": "Phase 1 - Implementation",
          "description": "Begin core program activities with first batch",
          "duration_weeks": 8,
          "budget_allocated": 80000,
          "deliverables": [
            "First batch completed",
            "Progress report submitted"
          ]
        }},
        {{
          "title": "Phase 2 - Completion",
          "description": "Complete remaining activities and document impact",
          "duration_weeks": 14,
          "budget_allocated": 50000,
          "deliverables": [
            "All beneficiaries covered",
            "Final impact report ready"
          ]
        }}
      ]
    }}
  ]
}}"""