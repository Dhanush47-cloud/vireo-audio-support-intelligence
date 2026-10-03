
import streamlit as st, pandas as pd, numpy as np
from analysis import run
st.set_page_config(page_title="Vireo Audio | Support Intelligence",page_icon="🎧",layout="wide",initial_sidebar_state="expanded")
st.markdown("""<style>
.block-container{max-width:1450px;padding-top:1.2rem}
.hero{padding:26px 30px;border-radius:20px;background:linear-gradient(135deg,#111a31,#172947);border:1px solid #2d4169;margin-bottom:16px}
.hero h1{color:#fff;margin:0;font-size:34px}.hero p{color:#aebdd8;margin:7px 0 0}
.k{padding:15px 16px;border:1px solid #2b3b5d;border-radius:14px;background:#10182a;min-height:103px}
.l{font-size:11px;color:#8fa0bd;text-transform:uppercase;letter-spacing:.07em}.v{font-size:25px;font-weight:750;color:#fff}.n{font-size:11px;color:#8291ad;margin-top:3px}
.insight{padding:16px 18px;border-radius:14px;background:#121d33;border:1px solid #33476e;color:#d8e1f3}
.small{font-size:12px;color:#91a1bd}
</style>""",unsafe_allow_html=True)
t,a,o,c,p,m,monthly,theme,b=run()
def card(col,l,v,n=""): col.markdown(f'<div class="k"><div class="l">{l}</div><div class="v">{v}</div><div class="n">{n}</div></div>',unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🎧 Vireo Audio — Support Intelligence</h1><p>Evidence-led agent review • CSAT • handle time • SLA economics • text themes • reproducible QA</p></div>',unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Decision context")
    st.write("**Comparable population:** Tier 1")
    st.write("**CSAT:** blank surveys excluded")
    st.write("**Handle time:** first response → resolution")
    st.write("**Legacy:** UTC → IST normalization")
    st.write("**Join key:** agent_id")
    st.divider()
    st.caption("No data upload or configuration is required to open the dashboard.")

# Business goal first.
st.subheader("Business goal")
st.markdown(f'<div class="insight"><b>Planning target:</b> reduce SLA-credit exposure by <b>{b["goal_reduction_pct"]}%</b> from ₹{b["sla_credit_exposure_inr"]:,.0f} to approximately ₹{b["sla_credit_exposure_inr"]*(1-b["goal_reduction_pct"]/100):,.0f}. That is about <b>₹{b["goal_savings_inr"]:,.0f}</b> in avoided store-credit exposure over the analyzed period if the reduction is achieved.<br><span class="small">This is a measurable planning target, not a claim that the dashboard proves causality.</span></div>',unsafe_allow_html=True)

cs=st.columns(6)
card(cs[0],"Tickets",f"{b['tickets_total']:,}","Jan 2025–Jun 2026")
card(cs[1],"Tier 1 CSAT",f"{b['tier1_csat']:.2f}/5","No-response surveys excluded")
card(cs[2],"SLA breaches",f"{b['sla_breaches_tier1']:,}","Tier 1")
card(cs[3],"SLA exposure",f"₹{b['sla_credit_exposure_inr']:,.0f}","₹350 per breach")
card(cs[4],"Replacements",f"{b['replacement_count']:,}","Policy: unit cost + ₹340")
card(cs[5],"Goal savings",f"₹{b['goal_savings_inr']:,.0f}","20% exposure reduction target")

st.divider()
tab1,tab2,tab3,tab4=st.tabs(["Agent review","AI-assisted text insights","Trends & economics","QA & methodology"])

with tab1:
    st.subheader("Bottom 10 — review shortlist")
    x=m[m.bottom10].copy(); x["Agent"]=x.name+" ("+x.agent_id+")"; x["CSAT"]=x.csat.round(2); x["Handle (h)"]=x.avg_handle_hours.round(2); x["SLA %"]=(x.sla_breach_rate*100).round(1); x["Context"]=x.context_flag.replace("","Standard")
    st.dataframe(x[["Agent","team","tickets","csat_responses","CSAT","Handle (h)","SLA %","Context"]].rename(columns={"team":"Team","tickets":"Tickets","csat_responses":"CSAT responses"}),use_container_width=True,hide_index=True)
    st.info("Interpretation guardrail: the bottom ten are a review signal, not proof that an agent caused low CSAT. Hardware/warranty context is explicitly surfaced because the client email says that queue receives harder customers by design.")
    st.subheader("CSAT vs handle time")
    st.scatter_chart(m[m.csat.notna()].set_index("agent_id")[["csat","avg_handle_hours"]],x="avg_handle_hours",y="csat")
    st.subheader("Agent drill-down")
    sel=st.selectbox("Select an agent to inspect",m.agent_id.tolist(),format_func=lambda x:f"{x} — {m.loc[m.agent_id.eq(x),'name'].iloc[0]}")
    r=m[m.agent_id.eq(sel)].iloc[0]
    d=st.columns(4); card(d[0],"CSAT",f"{r.csat:.2f}/5" if pd.notna(r.csat) else "—",f"{int(r.csat_responses)} responses"); card(d[1],"Avg handle",f"{r.avg_handle_hours:.2f} h",f"Median {r.median_handle_hours:.2f} h"); card(d[2],"SLA breach",f"{r.sla_breach_rate*100:.1f}%",f"{int(r.sla_breaches)} tickets"); card(d[3],"Replacements",f"{int(r.replacements)}",f"{r.replacement_rate*100:.1f}%")
    st.write(f"**Team:** {r['team']} · **Site:** {r['site']} · **Shift:** {r['shift']} · **Tier:** {r['tier']}")
    if r.context_flag: st.info("Context flag: "+r.context_flag+". Compare within queue before assigning training.")

with tab2:
    st.subheader("AI-assisted ticket-text themes")
    st.caption("Transparent local NLP: keyword-based theme extraction from customer opening messages. No paid API calls. Themes are a decision-support aid, not a sentiment or causality model.")
    tt=theme.copy(); tt["Share %"]=(tt.share*100).round(1); tt["CSAT"]=tt.csat.round(2); tt["Handle (h)"]=tt.avg_handle_hours.round(2); tt["SLA %"]=(tt.sla_breaches/tt.tickets*100).round(1)
    st.dataframe(tt[["theme","tickets","Share %","CSAT","Handle (h)","SLA %"]].rename(columns={"theme":"Theme","tickets":"Tickets"}).sort_values("Tickets",ascending=False),use_container_width=True,hide_index=True)
    st.bar_chart(tt.sort_values("tickets").set_index("theme")[["tickets"]])
    # deterministic insight
    top=tt.sort_values("tickets",ascending=False).iloc[0]
    low=tt.dropna(subset=["csat"]).sort_values("csat").iloc[0]
    st.markdown(f'<div class="insight"><b>Model-generated decision aid:</b> “{top["theme"]}” is the largest classified theme ({int(top["tickets"]):,} Tier-1 tickets, {top["Share %"]:.1f}% of Tier-1 volume). The lowest-CSAT classified theme is “{low["theme"]}” at {low["CSAT"]:.2f}/5. Treat these as prioritization signals; validate samples manually before changing training policy.</div>',unsafe_allow_html=True)

with tab3:
    z=monthly.copy(); z.month=pd.to_datetime(z.month)
    st.subheader("Monthly trend")
    q1,q2,q3=st.tabs(["CSAT","Handle time","SLA breaches"])
    with q1: st.line_chart(z.set_index("month")[["csat"]])
    with q2: st.line_chart(z.set_index("month")[["avg_handle_hours"]])
    with q3: st.line_chart(z.set_index("month")[["sla_breaches"]])
    st.subheader("Replacement economics")
    st.metric("Policy-based replacement cost",f"₹{b['replacement_cost_inr']:,.0f}",help="Replacement cost = product unit cost + ₹340 logistics, per policy.")

with tab4:
    st.subheader("Validation & data quality")
    qa=pd.DataFrame({
      "Check":["Ticket rows","Agents","Tier 1 agents","Tier 2 agents","Blank CSAT","Raw negative handle times","Negative handle after legacy fix"],
      "Actual":[len(t),len(a),int((a.tier==1).sum()),int((a.tier==2).sum()),int(t.csat_score.isna().sum()),b["raw_negative_handle"],b["negative_handle_after_fix"]],
      "Expected":[11750,44,38,6,6554,2309,0]})
    qa["Pass"]=qa.Actual.eq(qa.Expected); st.dataframe(qa,use_container_width=True,hide_index=True)
    st.success("All core reconciliation checks pass." if qa.Pass.all() else "One or more checks need review.")
    st.markdown("""
**Methodology**
- Tier 1 only for comparable bottom-ten ranking; Tier 2 remains separate.
- Blank CSAT is excluded from CSAT averages.
- Handle time = first human response → resolution.
- Legacy resolution timestamps are normalized from event-log UTC to the helpdesk's IST clock.
- Agent joins use `agent_id`, avoiding duplicate-name errors.
- Hardware/warranty context is shown as a caveat, not an excuse.
- Core KPIs are deterministic; the text-theme layer is transparent local NLP.
""")
    st.subheader("Known limitations")
    st.markdown("- Text themes are keyword-based and can miss synonyms or multi-intent tickets.\n- CSAT is observational and can reflect queue mix/product issues; the dashboard does not infer causality.\n- The 20% savings target is a planning target, not a forecast.\n- No automatic retraining decision is made from the ranking alone.")

st.divider()
st.caption("Vireo Audio Task 1 • Reproducible local analysis • No paid per-ticket model calls")
