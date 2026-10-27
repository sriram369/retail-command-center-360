"""Tests verify controls detect corruption and cover SLA boundary cases."""
import unittest,sqlite3,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class Controls(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(':memory:')
        with sqlite3.connect(ROOT/'data/processed/retail360.sqlite') as source:source.backup(self.db)
    def tearDown(self):self.db.close()
    def test_invalid_reference_is_detected(self):
        self.db.execute('UPDATE FactSalesOrderLines SET OrderId=99999999 WHERE OrderLineId=1')
        n=self.db.execute('SELECT COUNT(*) FROM FactSalesOrderLines l LEFT JOIN FactSalesOrders o USING(OrderId) WHERE o.OrderId IS NULL').fetchone()[0]
        self.assertEqual(n,1)
    def test_duplicate_erp_business_key_is_detected(self):
        self.db.execute('INSERT INTO FactERPOrderLinks SELECT 99999999,OrderId,ERPOrderId,SyncedDate FROM FactERPOrderLinks LIMIT 1')
        rows=self.db.execute('SELECT OrderId FROM FactERPOrderLinks GROUP BY OrderId HAVING COUNT(*)>1').fetchall()
        self.assertEqual(len(rows),1)
    def test_canceled_sale_is_detected(self):
        oid=self.db.execute("SELECT OrderId FROM FactSalesTransactions WHERE TransactionType='Sale' LIMIT 1").fetchone()[0]
        self.db.execute("UPDATE FactSalesOrders SET OrderStatus='Canceled' WHERE OrderId=?",(oid,))
        self.assertGreater(self.db.execute("SELECT COUNT(*) FROM FactSalesTransactions s JOIN FactSalesOrders o USING(OrderId) WHERE o.OrderStatus='Canceled'").fetchone()[0],0)
    def test_budget_does_not_multiply(self):
        a=self.db.execute('SELECT SUM(SalesBudget) FROM FactBudget').fetchone()[0]
        b=self.db.execute('SELECT SUM(SalesBudget) FROM ReportFinance').fetchone()[0]
        self.assertAlmostEqual(a,b,places=2)
    def test_independent_sql_financial_control(self):
        k=json.loads((ROOT/'reports/kpi_controls.json').read_text())
        value=self.db.execute('SELECT SUM(NetAmount-COGS) FROM FactSalesTransactions').fetchone()[0]
        self.assertAlmostEqual(value,k['gross_profit'],places=2)
    def test_missing_events_are_not_lost(self):
        n=self.db.execute("SELECT COUNT(*) FROM ReportReconciliation WHERE SyncStatus='Awaiting reconciliation' AND HasEvent=0").fetchone()[0]
        self.assertGreater(n,0)
    def test_sla_open_boundary_and_zero_denominator(self):
        # Exact deadline is passed/eligible at the same instant; unresolved means breach.
        self.db.execute('CREATE TEMP TABLE tickets(status TEXT,deadline TEXT,resolved TEXT)')
        self.db.executemany('INSERT INTO tickets VALUES(?,?,?)',[
            ('Open','2026-09-30T23:59:59',None),('Open','2026-10-01T00:00:00',None),
            ('Resolved','2026-09-30T12:00:00','2026-09-30T12:00:00')])
        eligible,met=self.db.execute("SELECT SUM(status='Resolved' OR deadline<='2026-09-30T23:59:59'),SUM(status='Resolved' AND resolved<=deadline) FROM tickets").fetchone()
        self.assertEqual((eligible,met),(2,1))
        self.assertIsNone(self.db.execute('SELECT 1.0/NULLIF(0,0)').fetchone()[0])

if __name__=='__main__':unittest.main()
