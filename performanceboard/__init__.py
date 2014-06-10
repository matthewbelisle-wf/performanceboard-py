from collections import defaultdict
from importlib import import_module
from time import time
import atexit
import logging
import json
import os

import requests


class Metric(object):
    """
    Context manager for a PerformanceBoard metric.  Metrics can be hierarchical.
    """
    def __init__(self, key, url=None):
        self.key = key
        self.url = url or os.environ.get('PERFORMANCEBOARD_URL')
        self.data = defaultdict(list, [('key', key)])

    def __enter__(self):
        self._stack.append(self)
        self.data['start'] = time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._stack.pop()
        self.data['end'] = time()
        if self._stack:
            parent = self._stack[-1]
            parent.data[self.key].append(self.data)
        else:
            self.post()
            logging.info('Posted to {}'.format(self.url))

    # Since nested metrics are all bundled into one post, `_stack` keeps track of the call chain to
    # enable accessing the parent metric.
    _stack = []

    def post(self):
        atexit.register(requests.post, self.url, data=json.dumps([self.data]))
