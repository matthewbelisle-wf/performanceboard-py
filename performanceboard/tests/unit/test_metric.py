from unittest import TestCase
import json

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
            with performanceboard.Metric('foo'):
                with performanceboard.Metric('bar'):
                    pass
            self.assertEqual(post.call_count, 1)

    def test_nesting(self):
        """
        Tests that metrics can be nested.

        https://github.com/mgbelisle/performanceboard#metrics
        """
        namespace = 'foo'
        namespace2 = 'bar'
        with patch('performanceboard.requests.post') as post:
            with performanceboard.Metric(namespace):
                with performanceboard.Metric(namespace2):
                    pass
                pass
            posted = json.loads(post.call_args[1]['data'])
        self.assertIn(namespace2, [m['namespace'] for m in posted['children']])

    def test_api(self):
        """
        Tests that os.environ['PERFORMANCEBOARD_API'] is used as the API.
        """
        api = 'dummy_api'
        with patch.dict('performanceboard.os.environ', {'PERFORMANCEBOARD_API': api}),\
             patch('performanceboard.requests.post') as post:
            with performanceboard.Metric('foo'):
                pass
            api2 = post.call_args[0][0]
        self.assertEqual(api, api2)
