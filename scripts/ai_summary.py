"""Optional grounded narrative. Default demonstration needs no credentials or network."""
import os,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROMPT='''You are an operations analyst. Use only the supplied validated metrics.
Return JSON with qualitative_summary (no digits), claims (array of metric_key values), and recommendations (array of qualitative strings, no digits).
Do not invent figures, calculations, financial savings or real company claims. Claims must reference exact supplied scalar metric keys.
Separate observations from recommendations. Unreconciled order value is exposure, not lost revenue.
'''
def main():
    metrics=json.loads((ROOT/'reports/kpi_controls.json').read_text())
    scalar={k:v for k,v in metrics.items() if isinstance(v,(int,float))}
    if not os.getenv('ANTHROPIC_API_KEY'):
        result={'mode':'Deterministic demonstration; no AI API called',
            'qualitative_summary':'Comparable-quarter sales increased while gross margin declined. Resolve missing ERP orders and review stock allocation.',
            'claims':['q3_sales_growth','q3_margin_change_pp','unreconciled_orders','stockout_risk_sku_locations'],
            'recommendations':['Assign order reconciliation ownership.','Review discounts alongside product cost changes.','Validate warehouse stock before replenishment transfers.']}
    else:
        model=os.getenv('ANTHROPIC_MODEL')
        if not model:raise SystemExit('Set ANTHROPIC_MODEL to a model available in your account. No request sent.')
        body={'model':model,'max_tokens':1200,'system':PROMPT,'messages':[{'role':'user','content':json.dumps(scalar)}]}
        request=urllib.request.Request('https://api.anthropic.com/v1/messages',data=json.dumps(body).encode(),
            headers={'content-type':'application/json','anthropic-version':'2023-06-01','x-api-key':os.environ['ANTHROPIC_API_KEY']})
        with urllib.request.urlopen(request,timeout=60) as response:payload=json.load(response)
        text=''.join(x['text'] for x in payload['content'] if x['type']=='text').strip()
        result=json.loads(text);result['mode']='AI-generated qualitative narrative, grounded claims rendered deterministically'
    for key in result['claims']:
        if key not in scalar:raise ValueError('Unsupported metric reference: '+key)
    for text in [result['qualitative_summary'],*result['recommendations']]:
        if any(ch.isdigit() for ch in text):raise ValueError('Numeric statements must be rendered from supplied metric references.')
    result['verified_claim_values']={key:scalar[key] for key in result['claims']}
    (ROOT/'reports/ai_summary_demo.json').write_text(json.dumps(result,indent=2))
    print(result['mode'])
if __name__=='__main__':main()
