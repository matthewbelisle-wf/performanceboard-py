from collections import defaultdict
from importlib import import_module
from time import time
from traceback import extract_stack
import atexit
import inspect
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
        self.metric = defaultdict(list, [('key', key)])

    def __enter__(self):
        self.metric['start'] = time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.metric['end'] = time()
        if self.url:
            # Nested metrics have their metric attached to the parent
            for frame in inspect.stack()[1:]:
                parent = frame[0].f_locals.get('self')
                if isinstance(parent, Metric):
                    parent.metric[self.key].append(self.metric)
                    break
            else:
                self.post()
                logging.info('Posted to {}'.format(self.url))

    def post(self):
        atexit.register(requests.post, self.url, data=json.dumps([self.metric]))
