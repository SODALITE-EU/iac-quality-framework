import json
import unittest

from ansiblemetrics.metrics_cal import MetricsCal


class TestRoleTaskMetrics(unittest.TestCase):

    def test_file(self):
        metricCal = MetricsCal()
        js = json.loads(metricCal.calculate('testResources/configure.yml', 'atss'))
        self.assertEqual(1, js['bloc']['count'])
        self.assertEqual(1, js['cloc']['count'])
        self.assertEqual(23, js['loc']['count'])
        self.assertEqual(3, js['nun']['count'])


if __name__ == '__main__':
    unittest.main()
