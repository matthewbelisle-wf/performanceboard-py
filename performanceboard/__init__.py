from collections import defaultdict
from importlib import import_module
from time import time
import logging
import json
import os

import requests


class Metric(object):
    """
    Context manager for a PerformanceBoard metric.  Metrics can be hierarchical.
    """
    def __init__(self, key, api=None):
        self.api = api or os.environ.get('PERFORMANCEBOARD_API')
        self.data = {'key': key}

    def __enter__(self):
        self._stack.append(self)
        self.start_data()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._stack.pop()
        self.end_data()
        if self._stack:
            parent = self._stack[-1]
            parent.data['children'] = parent.data.get('children', [])
            parent.data['children'].append(self.data)
        else:
            self.post()
            logging.info('Posted to {}'.format(self.api))

    # Since nested metrics are all bundled into one post, `_stack` keeps track of the call chain to
    # enable accessing the parent metric.  This limits usage to single threaded apps unfortunately,
    # perhaps there is a way to implement it through inspect.stack()?
    _stack = []

    def start_data(self):
        self.data['start'] = time()

    def end_data(self):
        self.data['end'] = time()

    def post(self):
        requests.post(self.api, data=json.dumps([self.data]))
