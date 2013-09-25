import urllib2
import config
import logging
from functools import wraps
from decorators import retries


logger = logging.getLogger('whoishiring.utils')


@retries(10, 1, 2, exceptions=(urllib2.URLError, IOError))
def get_raw_page(url):
    """Download a listing page with the given link

    Args:
     link:  URL of the page with job postings
    Returns:
     File-like object, like urlopen does for urllib2
    """
    request = urllib2.Request(url, None, {'User-Agent': config.USERAGENT})
    try:
        f = urllib2.urlopen(request)
    except urllib2.URLError as e:
        logger.error("Error occured when downloading page: %s", e.message)
        raise
    return f


def cache(func):
    saved = {}
    @wraps(func)
    def newfunc(*args):
        if args in saved:
            return newfunc(*args)
        result = func(*args)
        saved[args] = result
        return result
    return newfunc