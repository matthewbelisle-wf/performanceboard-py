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
            with performanceboard.Metric('foo', url='dummy_url') as metric:
                with performanceboard.Metric('bar', url='dummy_url') as metric2:
                    pass
            self.assertEqual(post.call_count, 1)

    def test_data(self):
        """
        Tests that metrics can be nested.

        {
          'key': 'foo',
          'start': 1402378113.505838,
          'end': 1402378113.505866,
          'bar': [
            {
              'key': 'bar',
              'start': 1402378113.50585,
              'end': 1402378113.505854
            }
          ]
        }
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
        self.assertIn(data2, data[key2])

    def test_url(self):
        """
        Tests that os.environ['PERFORMANCEBOARD_URL'] is used as the URL.
        """
        url = 'dummy_url'
        with patch.dict('performanceboard.os.environ', {'PERFORMANCEBOARD_URL': url}),\
             performanceboard.Metric('foo') as metric:
            url2 = metric.url
        self.assertEqual(url, url2)
