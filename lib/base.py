from urlparse import urljoin
import config
import logging


logger = logging.getLogger("lib.base")


class MetaBase(type):
    def __getattr__(cls, item):
        if item == "SUBMISSION_URL":
            return urljoin(config.HN_BASE_URL, config.HN_SUBMISSIONS_URL)
        if hasattr(config, item):
            return getattr(config, item)
        else:
            raise AttributeError(item)

class Base(object):
    __metaclass__ = MetaBase

    def __init__(self):
        super(Base, self).__init__()