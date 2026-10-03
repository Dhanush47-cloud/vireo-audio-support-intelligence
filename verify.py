
from analysis import run
import pandas as pd, json
t,a,o,c,p,m,monthly,theme,b=run()
rows=[("tickets",len(t),11750),("agents",len(a),44),("orders",len(o),15500),("customers",len(c),9500),("products",len(p),14),("tier1",int((a.tier==1).sum()),38),("tier2",int((a.tier==2).sum()),6),("blank_csat",int(t.csat_score.isna().sum()),6554),("raw_negative_handle",b["raw_negative_handle"],2309),("negative_handle_after_fix",b["negative_handle_after_fix"],0)]
out=pd.DataFrame(rows,columns=["check","actual","expected"]); out["pass"]=out.actual.eq(out.expected)
print(out.to_string(index=False))
out.to_csv("outputs/verification_checks.csv",index=False); m.to_csv("outputs/agent_metrics_tier1.csv",index=False); monthly.to_csv("outputs/monthly_metrics.csv",index=False); theme.to_csv("outputs/text_themes_tier1.csv",index=False); pd.DataFrame([b]).to_csv("outputs/business_metrics.csv",index=False)
assert out["pass"].all()
