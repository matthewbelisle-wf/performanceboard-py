from unittest import TestCase

from mock import patch
from mock import Mock

import performanceboard


@patch('performanceboard.requests', Mock())
class MetricTestCase(TestCase):
    def test_post(self):
        """
        Tests that post is called exactly once, even with nested metrics.
        """
        with patch('performanceboard.Metric.post') as post:
            with performanceboard.Metric('foo', api='dummy_api') as metric:
                with performanceboard.Metric('bar', api='dummy_api') as metric2:
                    pass
            self.assertEqual(post.call_count, 1)

    def test_data(self):
        """
        Tests that metrics can be nested.

        https://github.com/mgbelisle/performanceboard#metrics
        """
        key = 'foo'
        key2 = 'bar'
        with performanceboard.Metric(key) as metric:
            with performanceboard.Metric(key2) as metric2:
                data2 = metric2.data
            data = metric.data
        self.assertIn('key', data)
        self.assertIn('start', data)
        self.assertIn('end', data)
        self.assertIn(data2, data['children'])

    def test_api(self):
        """
        Tests that os.environ['PERFORMANCEBOARD_API'] is used as the API.
        """
        api = 'dummy_api'
        with patch.dict('performanceboard.os.environ', {'PERFORMANCEBOARD_API': api}),\
             performanceboard.Metric('foo') as metric:
            api2 = metric.api
        self.assertEqual(api, api2)
