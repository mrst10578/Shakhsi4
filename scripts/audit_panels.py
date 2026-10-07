"""Inspect two confidential source Excel panels without publishing row-level data.
pip install artifact-tool numpy
python scripts/audit_panels.py --ai "data/AI_Balanced_Panel (1).xlsx" --digital "data/Balanced_Panel_Data.xlsx"
"""
import argparse
import json
from collections import Counter
from pathlib import Path
import numpy as np
from artifact_tool import Blob, SpreadsheetFile

SPECS = {
 "ai":["AI_Investment","AI_Patents","GDP_Growth"],
 "digital":["Internet","Broadband","ICT_Exports","Unemployment","Inflation","RnD"]
}

def read_excel(path):
 wb=SpreadsheetFile.import_xlsx(Blob.load(str(path)))
 ws=wb.worksheets.get_item_at(0)
 head=ws.get_range("A1:Z1").values[0]
 columns=[str(c) for c in head if c is not None and str(c).strip()]
 cells=ws.get_range_by_indexes(1,0,1200,len(columns)).values
 return columns,[dict(zip(columns,r)) for r in cells if r[0] is not None and r[0]!=""]

def vifs(matrix, columns):
 x=np.asarray(matrix,dtype=float)
 out={}
 for col in range(x.shape[1]):
  dependent=x[:,col]
  others=np.column_stack([np.ones(len(x)),np.delete(x,col,axis=1)])
  beta=np.linalg.lstsq(others,dependent,rcond=None)[0]
  var=np.sum((dependent-np.mean(dependent))**2)
  unexplained=np.sum((dependent-others@beta)**2)
  score=(var/unexplained) if var>0 and unexplained/var>1e-10 else None
  out[columns[col]]=round(float(score),4) if score is not None else "undefined or infinite"
 return out

def inspect(name,path):
 cols,rows=read_excel(path)
 countries=sorted({r["ISO3"] for r in rows})
 years=sorted({int(r["Year"]) for r in rows})
 ids=[(r["ISO3"],int(r["Year"])) for r in rows]
 counts=Counter(r["ISO3"] for r in rows)
 numeric=[c for c in cols if c not in ("ISO3","Country","Year")]
 missing={k:sum(r[k] is None or r[k]=="" for r in rows) for k in cols}
 distributions={}
 for key in numeric:
  a=np.asarray([float(r[key]) for r in rows if isinstance(r[key],(int,float))])
  distributions[key]={"min":round(float(a.min()),4),"median":round(float(np.median(a)),4),
    "p99":round(float(np.quantile(a,.99)),4),"max":round(float(a.max()),4),
    "zero_n":int(np.sum(a==0)),"negative_n":int(np.sum(a<0))}
 pred=SPECS[name]
 clean=[r for r in rows if all(isinstance(r[p],(int,float)) for p in pred)]
 x=np.asarray([[float(r[p]) for p in pred] for r in clean])
 demean=[]
 for code in countries:
  subset=np.asarray([[float(r[p]) for p in pred] for r in clean if r["ISO3"]==code])
  demean.extend((subset-subset.mean(axis=0)).tolist())
 cor=np.corrcoef(x,rowvar=False)
 high=[{"a":pred[i],"b":pred[j],"correlation":round(float(cor[i,j]),4)}
  for i in range(len(pred)) for j in range(i+1,len(pred)) if abs(cor[i,j])>=.8]
 flags=[]
 if "AI_Patents" in cols:
  for code in countries:
   subset=sorted((r for r in rows if r["ISO3"]==code),key=lambda r:r["Year"])
   if subset[-1]["Year"]==2024 and subset[-2]["AI_Patents"]>0:
    ratio=subset[-1]["AI_Patents"]/subset[-2]["AI_Patents"]
    if ratio<.2: flags.append({"ISO3":code,"year":2024,"field":"AI_Patents","ratio_vs_2023":round(ratio,3)})
 return {
  "track":name,"source_filename":Path(path).name,"n_obs":len(rows),"n_countries":len(countries),
  "year_min":years[0],"year_max":years[-1],"year_count":len(years),
  "countries":countries,"Iran_present":"IRN" in countries,"duplicates":len(ids)-len(set(ids)),
  "balanced":len(rows)==len(countries)*len(years) and all(v==len(years) for v in counts.values()),
  "missing_by_field":missing,"distribution":distributions,
  "pooled_vif":vifs(x,pred),"within_country_vif":vifs(demean,pred),
  "strong_correlations_abs_ge_0_8":high,"unverified_anomaly_flags":flags,
  "not_executed":["formal IPS/LLC/Fisher unit roots","Stata xtabond2 system GMM","Hansen/AR diagnostics"]
 }

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--ai",required=True)
 p.add_argument("--digital",required=True)
 p.add_argument("--out",default="results/audit.json")
 args=p.parse_args()
 report={"ai":inspect("ai",args.ai),"digital":inspect("digital",args.digital)}
 out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 for name,s in report.items():
  print(name,s["n_obs"],s["n_countries"],s["year_min"],s["year_max"],
    "duplicates",s["duplicates"],"pooled_VIF",s["pooled_vif"])
if __name__=="__main__":
 main()
