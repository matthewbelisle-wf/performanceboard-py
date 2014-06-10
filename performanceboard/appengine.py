import dev_appserver

from . import Metric


dev_appserver.fix_sys_path()


class AppengineMetric(Metric):
    # TODO: Collect memory metrics
    pass
        
