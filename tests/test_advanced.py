from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import compare_curves as tool

HEADER='contract,delivery_month,price,quote_time,benchmark,currency,unit\n'
def curve(day,months,prices):
    return (HEADER+''.join(f'DEMO_{month},2024-{month:02d},{price},2024-01-{day:02d}T00:00:00Z,WTI,USD,currency_per_barrel\n' for month,price in zip(months,prices))).encode()

class AdvancedTests(unittest.TestCase):
    def check(self,before,after):
        return tool.analyze(before,after,'2024-01-08T00:00:00Z','2024-01-09T00:00:00Z','synthetic')

    def test_fixed_pair_avoids_rollover_comparison(self):
        result=self.check(curve(8,[2,3,4],[90,80,78]),curve(9,[3,4,5],[82,79,70]))
        self.assertEqual(result['comparison_pair'],['DEMO_3','DEMO_4'])
        self.assertEqual(result['previous_matched_spread'],2)
        self.assertEqual(result['current_matched_spread'],3)
        self.assertEqual(result['matched_spread_change'],1)
        self.assertEqual(result['dropped_contracts'],['DEMO_2'])
        self.assertEqual(result['added_contracts'],['DEMO_5'])

    def test_signed_prices_preserve_raw_spread_change(self):
        result=self.check(curve(8,[3,4],[-10,-5]),curve(9,[3,4],[-7,-4]))
        self.assertEqual(result['matched_spread_change'],2)
        self.assertNotIn('return',result)

    def test_changed_contract_month_and_reused_quotes_are_rejected(self):
        before=curve(8,[3,4],[80,78])
        after=curve(9,[3,4],[82,79])
        for raw in [after.replace(b'2024-03',b'2024-05'),after.replace(b'2024-01-09',b'2024-01-08')]:
            with self.subTest(raw=raw),self.assertRaises(ValueError):
                self.check(before,raw)

    def test_insufficient_overlap_and_currency_mismatch_are_rejected(self):
        before=curve(8,[3,4],[80,78])
        for after in [curve(9,[4,5],[79,77]),curve(9,[3,4],[82,79]).replace(b'USD',b'CNY')]:
            with self.subTest(after=after),self.assertRaises(ValueError):
                self.check(before,after)
