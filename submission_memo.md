# Vireo Audio — Support Performance Review
**To:** Priya Raman, Head of Customer Experience

## Executive summary
The supplied pack contains 11,750 tickets from January 2025 through June 2026. The dashboard uses Tier 1 as the comparable population for the requested bottom-ten review and keeps Tier 2 separate. Blank CSAT values are treated as non-responses.

The bottom ten are presented as a **review shortlist**, not an automatic retraining list. The email thread states that the hardware-triage/warranty queue receives harder customers by design, so the dashboard surfaces that context alongside CSAT, response count, handle time and SLA rate.

## Business outcome
A measurable planning target is to reduce SLA-credit exposure by 20%. The analyzed Tier-1 exposure is ₹332,850, so a 20% reduction corresponds to about **₹66,570** of avoided store-credit exposure over the analyzed period. This is a target, not a causal forecast.

## Cost
The tool makes **no paid API/model calls**. The marginal model/API cost per run is ₹0, so the model/API monthly cost at roughly 650 tickets/week is also ₹0.

## Validation
The included verification script reconciles row counts, agent/tier populations, blank CSAT handling and the legacy timestamp correction. Raw negative handle times are detected and disappear after UTC→IST normalization. The text-theme layer is keyword-based and therefore intentionally transparent.

## Limitations
The tool is descriptive, not causal. Keyword themes can miss synonyms and multi-intent cases. CSAT can reflect queue mix, product issues and customer expectations. The 20% savings figure is a planning target.

## Scope
The dashboard focuses on the requested decision: who should be reviewed for training. It deliberately does not automate retraining decisions or make per-ticket paid LLM calls.
