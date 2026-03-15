# CSR AI Service API

## 1. CSR Conversational Agent

### Endpoint

```
POST /csr-agent/chat
```

### Purpose

Collect CSR campaign preferences step-by-step and extract structured data.

---

### Request

```json
{
  "session_id": "123",
  "message": "around 5 lakhs",
  "context": {
    "current_step": "collect_budget",
    "preferences_collected": {},
    "user_profile": {
      "company_id": 1,
      "company_name": "Example Corp"
    }
  }
}
```

### Response

```json
{
  "response_text": "Which cause would you like to support?",
  "next_step": "collect_cause",
  "action": "collect_cause",
  "extracted_data": {
    "budget": 500000
  }
}
```

### Completion Response

When all preferences are collected:

```json
{
  "action": "complete",
  "next_step": null,
  "extracted_data": {
    "budget": 500000,
    "cause": "Education",
    "region": "Maharashtra",
    "timeline": 6
  }
}
```

---

## 2. Campaign Generation

### Endpoint

```
POST /generate-campaign
```

### Request

```json
{
  "cause": "Women empowerment",
  "budget": 5000000,
  "region": "Maharashtra",
  "timeline": 12,
  "companyId": "uuid"
}
```

### Response

```json
{
  "campaigns": [
    {
      "title": "EmpowerHer",
      "description": "...",
      "budgetBreakdown": {
        "infrastructure": 200000,
        "training": 150000,
        "materials": 100000,
        "monitoring": 50000
      },
      "scheduleVII": "...",
      "sdgAlignment": [5, 8],
      "impactMetrics": {
        "beneficiaries": 500,
        "duration": "12 months"
      },
      "milestones": [
        {
          "title": "Setup & Onboarding",
          "description": "Identify beneficiaries, set up required infrastructure",
          "duration_weeks": 2,
          "budget_allocated": 20000,
          "deliverables": [
            "Beneficiary list finalized",
            "Infrastructure ready"
          ]
        }
      ]
    }
  ]
}
```

> Multiple campaign options may be returned (typically 3 per request).
