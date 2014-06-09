"""
Plugins are python modules with a method `post(data=None, url=None)` in order to facilitate
asynchronous posts.  Potential plugins would be appengine, twisted, celery, and gevent maybe?

Look at [./appengine.py](./appengine.py) for an example.
"""

from importlib import import_module


PLUGINS = ['performanceboard.appengine']


def get_plugin():
    for plugin in PLUGINS:
        try:
            return import_module(plugin)
        except PluginNotAvailable:
            pass


class PluginNotAvailable(Exception):
    """
    Plugin is not available
    """
