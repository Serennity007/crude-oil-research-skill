import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import analyze_curve as tool
import analyze_structure as structure

HEADER = 'contract,delivery_month,price,quote_time,benchmark,currency,unit\n'
def data(prices=(80, 78, 77)):
    return (HEADER + ''.join(f'DEMO{i},2024-0{i+3},{price},2024-01-09T00:00:00Z,WTI,USD,currency_per_barrel\n' for i, price in enumerate(prices))).encode()

class CurveTests(unittest.TestCase):
    def run_curve(self, raw):
        return tool.analyze(raw, '2024-01-09T00:00:00Z', 'synthetic')

    def test_curve_shape_and_signed_spread_arithmetic(self):
        for prices, shape in [((80,78,77),'backwardation'), ((77,78,80),'contango'), ((80,80,80),'flat'), ((80,78,81),'mixed')]:
            with self.subTest(prices=prices):
                result = self.run_curve(data(prices))
                self.assertEqual(result['curve_shape'], shape)
                self.assertEqual(result['near_minus_far'], prices[0]-prices[-1])
        self.assertAlmostEqual(self.run_curve(data())['near_minus_far_over_near'], .0375)

    def test_delivery_sorting_does_not_use_file_order(self):
        lines = data().decode().splitlines()
        result = self.run_curve(('\n'.join([lines[0], *reversed(lines[1:])])+'\n').encode())
        self.assertEqual(result['near_minus_far'], 3)

    def test_negative_prices_preserve_spread_and_omit_percentage(self):
        result = self.run_curve(data((-10,0,5)))
        self.assertEqual(result['near_minus_far'], -15)
        self.assertIsNone(result['near_minus_far_over_near'])
        self.assertTrue(result['nonpositive_quotes_present'])
        raw = b'close_time,open,high,low,close\n2024-01-01T00:00:00Z,-10,-8,-12,-9\n'
        report = structure.analyze(raw,'OIL_DEMO','H4','2024-01-02T00:00:00Z','synthetic',support=-11,resistance=-7)
        self.assertEqual(report['latest_completed_bar']['close'], -9)

    def test_future_counterfactual_cannot_change_curve(self):
        reports = [self.run_curve(data() + f'FUTURE,2024-06,{v},2024-01-10T00:00:00Z,WTI,USD,currency_per_barrel\n'.encode()) for v in (-999,999)]
        for key in ('curve_shape','near_minus_far','quotes'):
            self.assertEqual(reports[0][key], reports[1][key])
        self.assertEqual(reports[0]['excluded_future_quotes'], 1)

    def test_mixed_units_benchmarks_and_currencies_are_rejected(self):
        for old,new in [('WTI','BRENT'),('USD','CNY'),('currency_per_barrel','USD_per_tonne')]:
            raw = data().decode().replace(old,new,1).encode()
            with self.subTest(new=new), self.assertRaises(ValueError):
                self.run_curve(raw)

    def test_duplicate_month_nonfinite_and_insufficient_data_are_rejected(self):
        bad = [data().decode().replace('2024-04','2024-03'), data().decode().replace(',78,',',NaN,'), HEADER+data().decode().splitlines()[1]+'\n']
        for raw in bad:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.run_curve(raw.encode())

    def test_asynchronous_age_is_visible(self):
        result = self.run_curve(data().replace(b'DEMO0,2024-03,80,2024-01-09T00:00:00Z',b'DEMO0,2024-03,80,2024-01-08T00:00:00Z'))
        self.assertEqual(result['quote_span_seconds'],86400)
        self.assertEqual(result['oldest_quote_age_seconds'],86400)
