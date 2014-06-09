from performanceboard.plugins import PluginNotAvailable
try:
    import dev_appserver
except ImportError:
    raise PluginNotAvailable('Google Appengine')
dev_appserver.fix_sys_path()


from google.appengine.ext.deferred import defer
import requests


def _post(data=None, url=None):
    requests.post(url, data=data)


def post(data=None, url=None):
    defer(_post, data=data, url=url)
