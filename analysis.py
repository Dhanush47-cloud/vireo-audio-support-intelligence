
from pathlib import Path
import pandas as pd, numpy as np, re
from collections import Counter
ROOT=Path(__file__).resolve().parent; DATA=ROOT/"data"
SLA={"chat":15/60,"email":8,"voice":2,"social":4}
STOP=set("""the and for with this that have from your are was were has had but not you our can will into on in to of a is it my me we i an be or as at by do did if so very they them their please just this""".split())
THEME_RULES={
"Delivery / logistics": ["delivery","deliver","shipping","shipment","courier","late","delay","delayed","tracking","arrive"],
"Replacement / return": ["replace","replacement","return","refund","exchange","damaged","damage"],
"Battery / charging": ["battery","charge","charging","drain","power"],
"Bluetooth / pairing": ["bluetooth","pair","pairing","connect","connection"],
"Audio quality": ["sound","audio","noise","volume","mic","microphone","static"],
"App / firmware": ["app","firmware","update","software","sync","watch","notification"],
"Warranty / hardware": ["warranty","defect","hardware","fault","broken","repair"],
"Account / order": ["order","account","invoice","payment","cancel","address"],
}
def load():
    return tuple(pd.read_csv(DATA/f) for f in ["tickets.csv","agents.csv","orders.csv","customers.csv","products.csv"])
def prepare(t):
    t=t.copy()
    for c in ["created_at","first_response_at","resolved_at"]: t[c]=pd.to_datetime(t[c],errors="coerce")
    raw=t["resolved_at"].copy()
    legacy=t.source_system.eq("legacy_fd") & t.resolved_at.notna()
    t.loc[legacy,"resolved_at"] += pd.Timedelta(hours=5,minutes=30)
    t["handle_time_hours"]=(t.resolved_at-t.first_response_at).dt.total_seconds()/3600
    t.loc[t.handle_time_hours<0,"handle_time_hours"]=np.nan
    t["response_time_hours"]=(t.first_response_at-t.created_at).dt.total_seconds()/3600
    t["sla_target_hours"]=t.channel.map(SLA); t["sla_breach"]=t.response_time_hours>t.sla_target_hours
    t["csat_score"]=pd.to_numeric(t.csat_score,errors="coerce")
    t["refund_amount_inr"]=pd.to_numeric(t.refund_amount_inr,errors="coerce").fillna(0)
    t["replacement_issued"]=t.replacement_issued.fillna("N").astype(str).str.upper()
    t["theme"]=t["customer_message"].fillna("").astype(str).str.lower().apply(classify_theme)
    return t,raw
def classify_theme(text):
    for theme, words in THEME_RULES.items():
        if any(re.search(r"\b"+re.escape(w)+r"\b",text) for w in words): return theme
    return "Other / mixed"
def run():
    t,a,o,c,p=load()
    raw_res=pd.to_datetime(t.resolved_at,errors="coerce"); raw_fr=pd.to_datetime(t.first_response_at,errors="coerce")
    raw_negative=int(((raw_res-raw_fr).dt.total_seconds()<0).sum())
    t,_=prepare(t)
    a1=a[a.tier.eq(1)].drop_duplicates("agent_id")
    g=t.groupby("agent_id")
    m=g.agg(tickets=("ticket_id","count"),csat_responses=("csat_score","count"),csat=("csat_score","mean"),
            avg_handle_hours=("handle_time_hours","mean"),median_handle_hours=("handle_time_hours","median"),
            sla_breaches=("sla_breach","sum"),replacements=("replacement_issued",lambda s:(s=="Y").sum()),
            refund_total_inr=("refund_amount_inr","sum")).reset_index()
    m=a1.merge(m,on="agent_id",how="left")
    m["sla_breach_rate"]=m.sla_breaches/m.tickets; m["replacement_rate"]=m.replacements/m.tickets
    m["eligible"]=m.csat.notna(); m["csat_rank"]=m.loc[m.eligible,"csat"].rank(method="min")
    m["bottom10"]=m.eligible&(m.csat_rank<=10)
    m["context_flag"]=np.where((m.team=="Escalations & Warranty")|m.agent_id.isin(["A3004","A3005","A3006","A3007"]),"Hardware / warranty context","")
    t["month"]=t.created_at.dt.to_period("M").astype(str)
    monthly=t.groupby("month").agg(tickets=("ticket_id","count"),csat=("csat_score","mean"),avg_handle_hours=("handle_time_hours","mean"),sla_breaches=("sla_breach","sum"),replacements=("replacement_issued",lambda s:(s=="Y").sum())).reset_index()
    tier1=t[t.agent_id.isin(set(a1.agent_id))]
    repl=t[t.replacement_issued.eq("Y")].merge(p[["sku","unit_cost_inr"]],left_on="product_sku",right_on="sku",how="left")
    theme= tier1.groupby("theme").agg(tickets=("ticket_id","count"),csat=("csat_score","mean"),avg_handle_hours=("handle_time_hours","mean"),sla_breaches=("sla_breach","sum")).reset_index()
    theme["share"]=theme.tickets/theme.tickets.sum()
    b={"tickets_total":len(t),"tier1_tickets":len(tier1),"tier1_csat":float(tier1.csat_score.mean()),
       "sla_breaches_tier1":int(tier1.sla_breach.sum()),"sla_credit_exposure_inr":int(tier1.sla_breach.sum()*350),
       "replacement_count":len(repl),"replacement_cost_inr":float((repl.unit_cost_inr.fillna(0)+340).sum()),
       "raw_negative_handle":raw_negative,"negative_handle_after_fix":int((t.handle_time_hours<0).sum())}
    # Goal: 20% reduction in SLA-credit exposure, a measurable planning target rather than a causal claim.
    b["goal_reduction_pct"]=20
    b["goal_savings_inr"]=round(b["sla_credit_exposure_inr"]*0.20,2)
    return t,a,o,c,p,m,monthly,theme,b
