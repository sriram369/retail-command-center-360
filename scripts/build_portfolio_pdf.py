"""Offline executive brief with explicitly identified native Power BI captures."""
from pathlib import Path
import json
from html import escape
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape,A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader

ROOT=Path(__file__).resolve().parents[1]
W,H=landscape(A4)
NAVY='#14233B';TEAL='#0F766E';MUTED='#63748A';BG='#F7F9FB';GRID='#E5EAF0';AMBER='#C48B42'
def main():
    k=json.loads((ROOT/'reports/kpi_controls.json').read_text())
    target=ROOT/'Retail360_Portfolio_Brief.pdf'
    c=canvas.Canvas(str(target),pagesize=(W,H));c.setTitle('Retail Command Center 360 | Portfolio brief')
    c.setAuthor('Aster & Co. synthetic portfolio project');c.setSubject('Business systems analysis and native Power BI report evidence')
    def box(x,y,w,h,color='#FFFFFF',stroke=GRID):
        c.setFillColor(HexColor(color));c.setStrokeColor(HexColor(stroke));c.roundRect(x,y,w,h,7,fill=1,stroke=1)
    def text(x,y,value,size=11,color=NAVY,bold=False):
        c.setFillColor(HexColor(color));c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,y,str(value))
    def para(x,y,w,value,size=11,color=NAVY,bold=False):
        p=Paragraph(value,ParagraphStyle('body',fontName='Helvetica-Bold' if bold else 'Helvetica',fontSize=size,leading=size*1.4,textColor=HexColor(color)))
        _,h=p.wrap(w,700);p.drawOn(c,x,y-h);return y-h
    def base(n,title,subtitle):
        c.setFillColor(HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(HexColor(NAVY));c.rect(0,H-5,W,5,fill=1,stroke=0)
        text(36,H-35,'ASTER & CO.  /  RETAIL COMMAND CENTER 360',10,TEAL,True)
        text(36,H-73,title,25,NAVY,True);text(36,H-95,subtitle,10,MUTED)
        text(36,20,'Fictional company | Synthetic data | USD | Reporting cutoff: September 30, 2026',8,MUTED)
        text(W-66,20,f'{n:02} / 05',8,MUTED)
    base(1,'Growth with operational friction.','Enterprise retail intelligence, business systems reliability and operational optimization')
    cards=[('+9.9%','Q3 sales growth vs 2025'),('-2.75 pp','Q3 gross margin change'),('28','Orders missing ERP links')]
    cw=(W-96)/3
    for i,(value,label) in enumerate(cards):
        x=36+i*(cw+12);box(x,H-211,cw,91)
        text(x+16,H-155,value,28,TEAL if i==0 else NAVY,True);text(x+16,H-182,label,10,MUTED)
    y=H-236
    para(36,y,W-72,'<b>The question:</b> Why can an accessories retailer grow sales while margin and service reliability weaken?',13)
    box(36,120,369,194);box(421,120,W-457,194)
    text(52,291,'What the sample indicates',14,NAVY,True)
    yy=272
    for body in [
        'Sales rose from $978k to $1.08m in comparable Q3 periods, while gross margin fell from 59.7% to 56.9%. Gross profit dollars still grew.',
        '$1.91m of stock coexists with six at-risk SKU/location pairs. About 383 days of historical COGS indicates slow overall stock circulation.',
        'Integration failures and absent events leave $4,132.66 of ordered-value exposure. This is not established lost revenue.'
    ]:
        yy=para(52,yy,337,escape(body),10)-12
    text(437,291,'Decisions and ownership',14,NAVY,True)
    yy=272
    for title,body in [
        ('Business Systems + IT','Assign the 28-order queue; repair mapping and confirm reconciliation before closing the business exception.'),
        ('Inventory + Procurement','Validate donor availability, prioritize delayed approvals and avoid indiscriminate purchasing.'),
        ('CFO + Merchandising','Review pouch/travel discounts alongside supplier cost and return trends.')
    ]:
        yy=para(437,yy,W-489,'<b>'+escape(title)+'</b><br/>'+escape(body),10)-12
    text(36,88,'Evidence: 275 dataset checks | 7 control tests | 15 SQL analyses | 20 matching raw-data hashes',10,TEAL,True)
    para(36,66,W-72,'Built in Power BI Service: three saved pages, 51 native DAX measures and 17 dimension relationships. This brief is an offline case summary; following pages are native browser captures.',9,MUTED)
    c.showPage()
    pages=[('Financial performance','01_financial_native.jpg'),('Inventory and fulfillment','02_inventory_native.jpg'),('Business systems health','03_systems_native.jpg')]
    for n,(title,name) in enumerate(pages,2):
        base(n,title,'Native Power BI Service browser capture | All available dates unless a current cutoff measure is shown')
        image=ImageReader(str(ROOT/'visuals/screenshots'/name));iw,ih=image.getSize()
        # Clip surrounding browser chrome in the PDF only. Original screenshots retain context.
        left,top,rw,rh=(253,297,1314,740) if name.startswith('02_') else (0,29,1677,944)
        maxw,maxh=W-60,H-139;scale=min(maxw/rw,maxh/rh);ww,hh=rw*scale,rh*scale
        x,y=(W-ww)/2,36+(maxh-hh)/2
        c.saveState();clip=c.beginPath();clip.rect(x,y,ww,hh);c.clipPath(clip,stroke=0)
        c.drawImage(image,x-left*scale,y-(ih-top-rh)*scale,width=iw*scale,height=ih*scale)
        c.restoreState()
        c.showPage()
    base(5,'A project a reviewer can inspect.','Reproducible sources, explicit definitions and evidence of native report execution')
    text(36,H-130,'Follow the evidence',15,NAVY,True)
    yy=H-151
    for number,title,body in [
        ('01','Read the business story','docs/executive_summary.md explains the findings, proposed actions and owners.'),
        ('02','Inspect the saved report','Open the Power BI report from README.md. Account access is required; public sharing has not been enabled.'),
        ('03','Trace the calculations','SQL, DAX and typed Power Query definitions are supplied. reports/kpi_controls.json is the independent numeric control.'),
        ('04','Reproduce and challenge it','Run python scripts/run_all.py after installing requirements.txt. Tests inject bad references and duplicate ERP identifiers into disposable databases.')
    ]:
        text(36,yy-2,number,15,TEAL,True);text(73,yy,title,12,NAVY,True)
        yy=para(73,yy-12,W-112,escape(body),10)-25
    box(36,58,W-72,130)
    text(52,164,'Scope and honest boundaries',13,NAVY,True)
    para(52,149,W-104,'All source systems and transactions are simulated. Sales is a shipment-date operational proxy, not audited accounting revenue. No production savings, real vendor integration, scheduled refresh or deployed RLS is claimed. Native order/SKU drillthrough and additional detail charts are documented extensions.',10)
    para(52,93,W-104,'The three captured report pages are real native Power BI visuals. This PDF was assembled locally from those browser captures; it is not a retained native Power BI PDF export. Scrollable queues are provided in full as CSV. Review and understand the work before using the supplied resume bullets.',9,MUTED)
    c.save();print(target)

if __name__=='__main__':main()
