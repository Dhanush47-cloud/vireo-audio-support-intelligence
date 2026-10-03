# Vireo Audio — Support Intelligence (Advanced)

## One-command workflow
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
python verify.py
streamlit run app.py
```

No user data upload or configuration is required. The app reads the included `data/` files automatically.

## What is included
- Business goal with explicit ₹ impact
- Tier-1 comparable bottom-ten review
- CSAT and handle time
- SLA breach economics
- Agent drill-down
- Monthly trends
- Transparent local NLP text-theme analysis
- Data-quality reconciliation
- Known-limitations panel

## Important decisions
Tier 2 is not ranked against Tier 1. Blank CSAT is excluded. Legacy resolution timestamps are normalized UTC→IST. Joins use agent_id. Hardware/warranty context is surfaced as a caveat. The 20% savings target is a planning target, not a causal forecast.

## Cost
The dashboard uses no paid API/model calls. One run has ₹0 marginal model/API cost. Monthly model/API cost at Vireo's stated volume is also ₹0.

## AI disclosure
AI/coding assistance was used for implementation and review. The final KPI calculations are deterministic. The text-theme layer is transparent keyword-based NLP rather than an opaque external API.

## Scope
Included: requested dashboard, bottom-ten review, business impact, text-theme decision aid, trends, drill-down and QA.
Excluded: automated causal attribution, automatic retraining decisions, per-ticket paid LLM inference, and a production database/backend.
