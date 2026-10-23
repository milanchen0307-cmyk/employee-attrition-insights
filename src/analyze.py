"""Aggregate exploration of a simulated coursework dataset; not an HR decision tool."""
from pathlib import Path
import argparse,json
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def wilson(k,n):
    z=1.96;p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [float(c-h),float(c+h)]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);a=ap.parse_args()
    df=pd.read_csv(a.data);df['left']=df.Attrition.eq('Yes').astype(int)
    rows=[]
    for (dept,ot,wlb),g in df.groupby(['Department','Overtime','Work_Life_Balance']):rows.append(dict(department=dept,overtime=ot,work_life_balance=int(wlb),n=len(g),left=int(g.left.sum())))
    summary=[]
    for dept,g in df.groupby('Department'):
        k=int(g.left.sum());n=len(g);summary.append(dict(department=dept,n=n,left=k,rate=k/n,ci95=wilson(k,n)))
    out=Path(__file__).resolve().parents[1]/'reports';out.mkdir(exist_ok=True)
    result=dict(dataset='Simulated employee attrition coursework dataset; not verified IBM employee records.',rows=len(df),left=int(df.left.sum()),rate=float(df.left.mean()),groups=rows,departments=summary,limitations='Descriptive associations only. Small groups are unstable. No employee-level predictions, causal claims, or employment decisions.')
    (out/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');pd.DataFrame(summary).to_csv(out/'department_summary.csv',index=False)
    fig,ax=plt.subplots(figsize=(9,4.5));rates=np.array([x['rate'] for x in summary]);bounds=np.array([x['ci95'] for x in summary]);ax.barh([x['department'] for x in summary],rates*100,xerr=np.array([rates-bounds[:,0],bounds[:,1]-rates])*100,color='#197c80',capsize=4);ax.set_xlabel('Observed attrition (%) with 95% Wilson interval');ax.set_title('Department comparison | Simulated coursework data');fig.tight_layout();fig.savefig(out/'department_rates.png',dpi=180);plt.close(fig)
    print('Aggregates exported:',len(df),'rows;',len(rows),'groups')
if __name__=='__main__':main()
