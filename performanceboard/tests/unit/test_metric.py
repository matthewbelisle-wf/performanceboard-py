from unittest import TestCase

from mock import patch

import performanceboard


class MetricTestCase(TestCase):
    def test_data(self):
        url = 'dummy_url'
        key = 'dummy_key'
        with patch('performanceboard.PLUGIN') as mock_plugin,\
             patch.dict('performanceboard.os.environ', {'PERFORMANCEBOARD_URL': url}):
            with performanceboard.Metric(key) as metric:
                data = metric.data
            mock_plugin.post.assert_called_once_with(data=data, url=url)
        self.assertIn('key', data)
        self.assertIn('start', data)
        self.assertIn('end', data)

    def test_url(self):
        url = 'dummy_url'
        with patch('performanceboard.PLUGIN') as mock_plugin:
            with performanceboard.Metric('dummy_key', url=url) as metric:
                data = metric.data
            mock_plugin.post.assert_called_once_with(data=data, url=url)
