# Submission Form — Vireo Audio Task 1

Candidate: Dhanush Bangera

Deliverable: Vireo Audio — Support Intelligence (Advanced)

Business goal: Reduce SLA-credit exposure by 20% as a measurable planning target. Current analyzed Tier-1 exposure is ₹332,850; 20% corresponds to ₹66,570 avoided exposure over the analyzed period if achieved.

Cost: No paid API/model calls. Marginal model/API cost per run = ₹0; monthly model/API cost at ~650 tickets/week = ₹0.

Validation: `python verify.py` checks source row counts, agent/tier populations, blank CSAT handling, raw negative handle times and the corrected post-normalization value. The text-theme layer is keyword-based and transparent.

Client pushback: Tier 2 was not ranked against Tier 1; bottom-ten was treated as a review shortlist rather than an automatic retraining list because of queue-context caveats in the email.

Limitations: Keyword themes can miss synonyms/multi-intent cases; CSAT is not causal; 20% is a planning target; no automatic retraining decision.

AI use: AI/coding assistance for implementation and review; deterministic pandas metrics; transparent local NLP; no paid per-ticket calls.

Three-minute recording: [PASTE PUBLIC RECORDING LINK]

Public Google Drive: [PASTE PUBLIC DRIVE LINK]

Monday handoff: 1) run `python verify.py`; 2) run `streamlit run app.py`; 3) read `README.md` and `submission_memo.md` for methodology and limitations.

Honest hours spent: [ENTER ACTUAL HOURS]

GitHub Repo: [PASTE PUBLIC REPO URL]
