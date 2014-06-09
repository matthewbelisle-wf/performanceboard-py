from importlib import import_module
from time import time
from traceback import extract_stack
import os

from performanceboard.plugins import get_plugin


PLUGIN = get_plugin()


class Metric(object):
    """
    Context manager for a PerformanceBoard metric.  Metrics can be hierarchical.
    """
    def __init__(self, key, url=None):
        self.data = {'key': key}
        self.url = url or os.environ.get('PERFORMANCEBOARD_URL')

    def __enter__(self):
        self.data['start'] = time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.data['end'] = time()
        if PLUGIN and self.url:
            PLUGIN.post(data=self.data, url=self.url)
