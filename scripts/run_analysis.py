"""Execute every SQL analysis statement and retain its reproducible results."""
import sqlite3,json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def run():
    results=[];buffer='';i=0
    with sqlite3.connect(ROOT/'data/processed/retail360.sqlite') as db:
        for line in (ROOT/'sql/business_analysis.sql').read_text().splitlines():
            buffer+=line+'\n'
            if sqlite3.complete_statement(buffer):
                cursor=db.execute(buffer);buffer=''
                if cursor.description:
                    i+=1;columns=[x[0] for x in cursor.description];rows=cursor.fetchall()
                    pd.DataFrame(rows,columns=columns).to_csv(ROOT/f'reports/sql_analysis_{i:02}.csv',index=False)
                    results.append({'query':i,'rows':len(rows),'columns':columns,'passed':True})
    (ROOT/'reports/sql_execution.json').write_text(json.dumps(results,indent=2))
    print(f'Executed {len(results)} analysis queries successfully.')
if __name__=='__main__':run()
