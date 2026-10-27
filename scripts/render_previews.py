"""Deterministic report layout previews; these are not native Power BI screenshots."""
from pathlib import Path
import json,math
import pandas as pd
from PIL import Image,ImageDraw,ImageFont
from generate_data import ROOT

NAVY='#14233B';TEAL='#0F766E';SLATE='#325E85';AMBER='#C48B42';MUTED='#63748A';RED='#B54738';BG='#F7F9FB';WHITE='#FFFFFF';GRID='#E5EAF0'
W,H=1600,900;S=2
def font(size,bold=False):
    choices=[Path('/System/Library/Fonts/Supplemental')/('Arial Bold.ttf' if bold else 'Arial.ttf'),
             Path('/usr/share/fonts/truetype/dejavu')/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for p in choices:
        if p.exists():return ImageFont.truetype(str(p),int(size*S))
    return ImageFont.load_default(size=int(size*S))

class Canvas:
    def __init__(self,page,title,subtitle):
        self.im=Image.new('RGB',(W*S,H*S),BG);self.d=ImageDraw.Draw(self.im)
        self.rect(0,0,W,7,NAVY);self.text(48,30,'ASTER & CO.',20,NAVY,True)
        self.text(48,60,'RETAIL COMMAND CENTER 360',10,MUTED,True)
        labels=['01  Financial performance','02  Inventory & fulfillment','03  Systems health']
        for i,label in enumerate(labels):
            x=530+i*340
            self.text(x,36,label,14,TEAL if page==i else MUTED,page==i)
            if page==i:self.rect(x,65,280,3,TEAL)
        self.text(48,102,title,32,NAVY,True);self.text(48,147,subtitle,14,MUTED)
        self.text(1550,108,'SEPTEMBER 30, 2026',11,MUTED,True,'ra')
        self.text(48,866,'Fictional company · Synthetic data · Verified analytical preview, not a native Power BI screenshot',11,MUTED)
        self.text(1550,866,f'{page+1:02} / 03',11,MUTED,False,'ra')
    def rect(self,x,y,w,h,fill,outline=None,r=0):
        xy=[int(x*S),int(y*S),int((x+w)*S),int((y+h)*S)]
        if r:self.d.rounded_rectangle(xy,int(r*S),fill=fill,outline=outline,width=S)
        else:self.d.rectangle(xy,fill=fill,outline=outline,width=S)
    def text(self,x,y,text,size=14,color=NAVY,bold=False,anchor=None):
        self.d.text((int(x*S),int(y*S)),str(text),font=font(size,bold),fill=color,anchor=anchor)
    def line(self,points,fill,width=2):
        self.d.line([(int(x*S),int(y*S)) for x,y in points],fill=fill,width=width*S)
    def panel(self,x,y,w,h,title,note=''):
        self.rect(x,y,w,h,WHITE,GRID,8);self.text(x+24,y+20,title,17,NAVY,True)
        if note:self.text(x+24,y+48,note,11,MUTED)
    def kpi(self,x,label,value,context,color=TEAL):
        self.rect(x,188,358,118,WHITE,GRID,8);self.text(x+22,205,label.upper(),11,MUTED,True)
        self.text(x+22,231,value,34,NAVY,True);self.text(x+22,279,context,12,color)
    def series(self,x,y,w,h,labels,series,percent=False):
        values=[v for _,vals,_ in series for v in vals];lo=0 if not percent else max(0,min(values)-.02)
        hi=max(values)*(1.18 if not percent else 1.03);n=len(labels)
        for step in range(4):
            frac=step/3;yy=y+h*(1-frac);self.line([(x,yy),(x+w,yy)],GRID,1)
            val=lo+(hi-lo)*frac;self.text(x-12,yy,f'{val:.0%}' if percent else f'${val/1000:,.0f}k',10,MUTED,anchor='rm')
        for name,vals,color in series:
            points=[(x+w*i/(n-1),y+h*(1-(v-lo)/(hi-lo))) for i,v in enumerate(vals)]
            self.line(points,color,3)
            for xx,yy in points:self.d.ellipse([int((xx-3)*S),int((yy-3)*S),int((xx+3)*S),int((yy+3)*S)],fill=color)
        for i,label in enumerate(labels):
            if i%3==0 or i==n-1:self.text(x+w*i/(n-1),y+h+18,label,10,MUTED,anchor='mm')
    def bars(self,x,y,w,labels,values,colors=None,formatvalue=None,row=38):
        maxv=max(values) if max(values)>0 else 1
        for i,(label,v) in enumerate(zip(labels,values)):
            yy=y+i*row;self.text(x,yy,label,12,NAVY)
            self.rect(x+150,yy+1,w-235,15,BG,r=3)
            self.rect(x+150,yy+1,(w-235)*max(v,0)/maxv,15,colors[i] if colors else TEAL,r=3)
            self.text(x+w,yy,formatvalue(v) if formatvalue else f'{v:,.0f}',12,NAVY,False,'ra')
    def table(self,x,y,widths,headers,rows,row=37):
        self.rect(x,y,sum(widths),34,BG)
        xx=x
        for h,w in zip(headers,widths):self.text(xx+12,y+11,h,10,MUTED,True);xx+=w
        for i,rr in enumerate(rows):
            yy=y+34+i*row;self.line([(x,yy+row),(x+sum(widths),yy+row)],GRID,1);xx=x
            for j,(value,w) in enumerate(zip(rr,widths)):
                self.text(xx+12,yy+12,value,11,TEAL if j==len(rr)-1 else NAVY);xx+=w
    def save(self,name):
        p=ROOT/'visuals/previews'/name;p.parent.mkdir(parents=True,exist_ok=True)
        self.im.resize((W,H),Image.Resampling.LANCZOS).save(p)
        return p

def main():
    k=json.loads((ROOT/'reports/kpi_controls.json').read_text())
    read=lambda n:pd.read_csv(ROOT/'data/processed'/f'{n}.csv')
    fin=read('ReportFinance');monthly=read('ReportMonthly');cat=read('ReportCategory');inv=read('ReportInventory');sys=read('ReportSystems')
    q=fin[fin.MonthStart.between('2026-07-01','2026-09-01')]
    current=k['q3_comparison'][1];old=k['q3_comparison'][0]
    c=Canvas(0,'Sales are growing. Margin needs attention.','Comparable quarter: Q3 2026 vs Q3 2025 · All channels · USD')
    c.kpi(48,'Q3 net sales',f'${current["NetSales"]/1e6:.2f}m',f'+{k["q3_sales_growth"]:.1%} vs prior-year quarter')
    c.kpi(430,'Q3 gross profit',f'${(current["NetSales"]-current["COGS"])/1000:,.0f}k','Sales less weighted-average product cost')
    c.kpi(812,'Q3 gross margin',f'{current["GrossMargin"]:.1%}',f'{k["q3_margin_change_pp"]:.2f} pp vs prior-year quarter',RED)
    c.kpi(1194,'Q3 sales vs budget',f'{q.NetSales.sum()/q.SalesBudget.sum()-1:+.1%}','Independent synthetic sales plan')
    c.panel(48,330,976,280,'Growth is visible; the plan needs recalibration','Monthly net sales and budget · Apr 2025–Sep 2026')
    c.text(820,353,'Actual',11,TEAL,True);c.text(900,353,'Budget',11,AMBER,True)
    labels=pd.to_datetime(monthly.MonthStart).dt.strftime('%b %y').tolist()
    c.series(120,415,865,135,labels,[('Actual',monthly.NetSales.tolist(),TEAL),('Budget',monthly.SalesBudget.tolist(),AMBER)])
    c.panel(1048,330,504,280,'Where Q3 sales come from','Net sales by channel')
    channel=q.groupby('Channel').NetSales.sum().sort_values(ascending=False)
    c.bars(1072,423,455,channel.index.tolist(),channel.tolist(),formatvalue=lambda v:f'${v/1000:,.0f}k',row=53)
    c.panel(48,634,976,202,'Category profitability','Q3 2026 · all channels · rates computed from totals')
    cq=cat[cat.MonthStart.between('2026-07-01','2026-09-01')].groupby('Category')[['NetSales','GrossProfit']].sum().sort_values('NetSales',ascending=False)
    rows=[(n,f'${r.NetSales/1000:,.0f}k',f'{r.GrossProfit/r.NetSales:.1%}') for n,r in cq.head(4).iterrows()]
    c.table(72,700,[320,280,280],['CATEGORY','NET SALES','GROSS MARGIN'],rows,row=23)
    c.panel(1048,634,504,202,'Management action')
    c.text(1072,684,'Review pouch and travel discount depth.',16,NAVY,True)
    c.text(1072,718,'Pair pricing decisions with supplier cost trends.',13,MUTED)
    c.text(1072,783,'OWNER  CFO + Merchandising',11,TEAL,True);c.save('01_financial_preview.png')
    c=Canvas(1,'Put inventory where demand is.','Current stock and exception view · As of September 30, 2026 · USD')
    c.kpi(48,'Inventory carrying value',f'${k["inventory_value"]/1e6:.2f}m','Moving weighted average cost')
    c.kpi(430,'Units on hand',f'{k["units_on_hand"]:,}','Physical stock across eight locations',SLATE)
    c.kpi(812,'SKU / locations at risk',str(k['stockout_risk_sku_locations']),'Recent demand + reserved backlog',RED)
    c.kpi(1194,'Open purchase orders',str(k['pending_purchase_orders']),'Awaiting approval or receipt',AMBER)
    c.panel(48,330,976,280,'High total stock can coexist with local shortages','Stock value by physical location')
    byloc=inv.groupby('LocationName').InventoryValue.sum().sort_values(ascending=False)
    labels=[x.replace('Columbus Distribution','Distribution center').replace('Aster ','') for x in byloc.index]
    c.bars(72,404,925,labels,byloc.tolist(),formatvalue=lambda v:f'${v/1000:,.0f}k',row=23)
    c.panel(1048,330,504,280,'Fulfillment control','Order cohorts through the reporting cutoff')
    c.text(1072,409,f'{k["fulfillment_rate"]:.1%}',46,NAVY,True);c.text(1072,466,'of noncanceled orders fulfilled',14,MUTED)
    c.text(1072,514,f'{k["open_late_orders"]} open orders past their promise',16,RED,True)
    c.text(1072,556,f'{k["average_fulfillment_days"]:.1f} days average for completed fulfillment',12,MUTED)
    c.panel(48,634,976,202,'Replenishment exceptions','Candidate actions require donor availability checks')
    risky=inv[inv.StockoutRisk.eq(1)].sort_values(['BackorderUnits','RecommendedUnits'],ascending=False).head(4)
    rr=[(r.SKU,r.LocationName.replace('Aster ',''),str(int(r.UnitsOnHand)),str(int(r.BackorderUnits)),str(int(r.RecommendedUnits))) for r in risky.itertuples()]
    c.table(72,700,[240,230,130,140,140],['SKU','LOCATION','ON HAND','BACKLOG','CANDIDATE UNITS'],rr,row=23)
    c.panel(1048,634,504,202,'Management action')
    c.text(1072,684,'Validate transfers before buying more.',16,NAVY,True)
    c.text(1072,718,'Expedite affected receipts and approvals.',13,MUTED)
    c.text(1072,783,'OWNER  Inventory + Procurement',11,TEAL,True);c.save('02_inventory_preview.png')
    c=Canvas(2,'Reconcile orders before exceptions spread.','Integration event trend + current reconciliation queue · All data is simulated')
    c.kpi(48,'Integration success',f'{k["integration_success_rate"]:.1%}','Ignored duplicates excluded from attempts')
    c.kpi(430,'Failed attempts',str(k['failed_integration_events']),'Events, not distinct failed orders',RED)
    c.kpi(812,'Orders to reconcile',str(k['unreconciled_orders']),f'${k["unreconciled_order_value"]:,.0f} ordered exposure, not booked loss',RED)
    c.kpi(1194,'Ticket SLA compliance',f'{k["sla_compliance"]:.1%}','Resolved + overdue open ticket population',RED)
    c.panel(48,330,976,280,'Failures rise with the affected assortment','Failed integration attempts by event month')
    vals=sys.FailedEvents.tolist();labels=pd.to_datetime(sys.MonthStart).dt.strftime('%b %y').tolist()
    x0,y0,ww,hh=105,411,870,139;mx=max(vals)*1.15
    for i,vv in enumerate(vals):
        bw=ww/len(vals)*.57;xx=x0+ww/len(vals)*i
        c.rect(xx,y0+hh-hh*vv/mx,bw,hh*vv/mx,RED if i>=15 else SLATE,r=3)
        if i%3==0 or i==len(vals)-1:c.text(xx,y0+hh+18,labels[i],10,MUTED)
    c.text(x0-14,y0+hh,'0',10,MUTED,anchor='rm')
    c.text(x0-14,y0,f'{mx:.0f}',10,MUTED,anchor='rm')
    c.panel(1048,330,504,280,'Reliability controls')
    c.text(1072,412,str(k['missing_event_orders']),42,NAVY,True);c.text(1130,424,'unresolved orders have no event',14,MUTED)
    c.text(1072,478,str(k['deduplicated_events']),42,TEAL,True);c.text(1175,490,'duplicate webhooks ignored',13,MUTED)
    c.text(1072,554,f'{k["mean_resolution_hours"]:.1f} h mean resolution · {k["open_tickets"]} open tickets',13,MUTED)
    c.panel(48,634,976,202,'Unresolved source orders','Source-to-ERP comparison catches missing events as well as failed events')
    recon=read('ReportReconciliation');recon=recon[recon.SyncStatus.eq('Awaiting reconciliation')].sort_values('OrderDate').head(4)
    rr=[(r.OrderNumber,r.OrderDate,r.ExceptionType,f'${r.OrderedAmount:,.0f}') for r in recon.itertuples()]
    c.table(72,700,[260,200,300,120],['SOURCE ORDER','ORDER DATE','EXCEPTION','EXPOSURE'],rr,row=23)
    c.panel(1048,634,504,202,'Management action')
    c.text(1072,684,'Fix mapping, then replay safely.',16,NAVY,True)
    c.text(1072,718,'Assign queue owners and prevent repeat causes.',13,MUTED)
    c.text(1072,783,'OWNER  Business Systems + IT',11,TEAL,True);c.save('03_systems_preview.png')
    html='''<!doctype html><html><meta charset="utf-8"><title>Aster & Co. | Analytical report previews</title><style>body{margin:0;background:#e8edf2;font-family:Segoe UI,Arial;color:#14233B}header{padding:24px 4%;background:#14233B;color:white}h1{margin:0;font-size:24px}p{margin:9px 0;font-size:14px}nav{display:flex;gap:12px;margin:24px 4%}a{padding:12px 18px;background:white;color:#0F766E;border-radius:6px;text-decoration:none}img{display:block;width:92%;max-width:1600px;margin:24px auto;box-shadow:0 8px 30px #14233b15}section{scroll-margin-top:20px}</style><header><h1>Retail Command Center 360</h1><p>Verified layout previews from synthetic data. These images are not the native Power BI report.</p></header><nav><a href="#finance">Financial performance</a><a href="#inventory">Inventory & fulfillment</a><a href="#systems">Systems health</a></nav>'''
    for label,name in [('finance','01_financial_preview.png'),('inventory','02_inventory_preview.png'),('systems','03_systems_preview.png')]:html+=f'<section id="{label}"><img alt="{label} verified analytical preview" src="{name}"></section>'
    (ROOT/'visuals/previews/index.html').write_text(html+'</html>')
    # Native Power BI backgrounds contain only branding, section labels and actions.
    # All values, charts and tables are left blank for real Power BI visuals.
    specs=[('Executive financial performance','April 2025–September 2026 · All channels · USD',
       'Monthly net sales and budget','Channel performance','Category profitability · all channels',
       'Review pouch and travel discount depth.','Pair pricing decisions with supplier cost trends.','CFO + Merchandising'),
      ('Inventory and fulfillment','Current stock · As of September 30, 2026 · USD',
       'Inventory carrying value by location','Open purchase orders by category','Replenishment exceptions',
       'Validate transfers before buying more.','Expedite affected receipts and approvals.','Inventory + Procurement'),
      ('Business systems health','Integration trends + current reconciliation queue · Simulated systems',
       'Failed integration attempts by month','Ticket SLA and resolution','Unresolved source orders',
       'Fix mapping, then replay safely.','Assign queue owners and prevent repeat causes.','Business Systems + IT')]
    target=ROOT/'powerbi/backgrounds';target.mkdir(exist_ok=True)
    for page,(title,sub,left,right,lower,action,explanation,owner) in enumerate(specs):
        b=Canvas(page,title,sub)
        # Replace preview disclosure with correct native-report disclosure.
        b.rect(40,850,1515,40,BG);b.text(48,866,'Aster & Co. is fictional · Synthetic data · Shipment-date sales proxy · USD',11,MUTED)
        b.text(1550,866,f'{page+1:02} / 03',11,MUTED,False,'ra')
        b.panel(48,330,976,280,left);b.panel(1048,330,504,280,right)
        b.panel(48,634,976,202,lower)
        if page==1:
            b.panel(1048,634,504,202,'Fulfillment and inventory cover')
        else:
            b.panel(1048,634,504,202,'Management action')
            b.text(1072,684,action,16,NAVY,True);b.text(1072,718,explanation,13,MUTED)
            b.text(1072,783,'OWNER  '+owner,11,TEAL,True)
        b.im.resize((W,H),Image.Resampling.LANCZOS).save(target/f'0{page+1}_background.png')
    print('Three labeled report previews rendered.')

if __name__=='__main__':main()
