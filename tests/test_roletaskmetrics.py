import json
import pytest

from ansiblemetrics.metrics_cal import MetricsCal


class TestRoleTaskMetrics:

    def test_(self):
        metricCal = MetricsCal()
        js = json.loads(metricCal.calculate('testResources/configure.yml', 'atss'))
        assert 1 == js['bloc']['count']
        assert 1 == js['cloc']['count']
        assert  23 == js['loc']['count']
        assert 3 == js['nun']['count']