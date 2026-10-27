import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const operations=process.argv.includes('--operations');
const data=JSON.parse(await fs.readFile(path.join(root,operations?'reports/operations_payload.json':'reports/workbook_payload.json'),'utf8'));
const wb=Workbook.create();
const col=n=>{let s='';for(n++;n>0;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
for(const [name,p] of Object.entries(data)){
  const sh=wb.worksheets.add(name);sh.showGridLines=false;
  const end=col(p.columns.length-1),rows=p.rows.length+1;
  // Power BI consumes explicit Excel tables, so headers start in row 1.
  sh.getRange(`A1:${end}${rows}`).values=[p.columns,...p.rows];
  sh.getRange(`A1:${end}${rows}`).format.font.name='Aptos';
  sh.getRange(`A1:${end}${rows}`).format.font.size=10;
  sh.getRange(`A1:${end}${rows}`).format.columnWidth=19;
  sh.getRange(`A1:${end}1`).format.fill='#14233B';
  sh.getRange(`A1:${end}1`).format.font.color='#FFFFFF';
  sh.getRange(`A1:${end}1`).format.font.bold=true;
  sh.getRange(`A1:${end}1`).format.rowHeight=38;
  sh.getRange(`A1:${end}1`).format.wrapText=true;
  sh.getRange(`A2:${end}${rows}`).format.rowHeight=19;
  sh.freezePanes.freezeRows(1);
  sh.tables.add(`A1:${end}${rows}`,true,name);
  p.columns.forEach((c,i)=>{
    const r=sh.getRange(`${col(i)}2:${col(i)}${rows}`);
    if(/(Sales|COGS|Profit|Value|Amount|Budget|Cost|Price)/.test(c))r.setNumberFormat('#,##0.00');
    else if(/(Units|Count|Events|Orders|Tickets|SLAEligible|SLAMet|Id|Risk|LowStock)/.test(c))r.setNumberFormat('#,##0');
    if(/(Name|Action|ProductName|LocationName)/.test(c))sh.getRange(`${col(i)}1:${col(i)}${rows}`).format.columnWidth=28;
  });
  if(name==='ReportInventory'){
    const idx=p.columns.indexOf('StockoutRisk');
    sh.getRange(`${col(idx)}2:${col(idx)}${rows}`).conditionalFormats.add('cellIs',{
      operator:'equal',formula:1,format:{fill:'#FDE9E4',font:{color:'#A33B2B',bold:true}}});
  }
}
wb.recalculate();
console.log((await wb.inspect({kind:'region',sheetId:Object.keys(data)[0],range:'A1:G5',maxChars:1800,tableMaxRows:5,tableMaxCols:7})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},maxChars:1000})).ndjson);
await fs.mkdir(path.join(root,'reports/workbook_previews'),{recursive:true});
for(const name of Object.keys(data)){
  const blob=await wb.render({sheetName:name,range:'A1:F6',scale:1.4,format:'png'});
  await fs.writeFile(path.join(root,'reports/workbook_previews',name+'.png'),new Uint8Array(await blob.arrayBuffer()));
}
const outputName=operations?'retail360_operations.xlsx':'retail360_powerbi.xlsx';
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(root,'data',outputName));
console.log('Workbook exported: '+path.join(root,'data',outputName));
