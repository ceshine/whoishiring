import os
from StringIO import StringIO


def get_page(page):
    """Return raw comment page from the data directory"""
    datadir = os.path.normpath(os.path.abspath(__file__)).split(os.sep)
    datadir = os.sep.join(datadir[:-2])
    with open(page % datadir, 'r') as f:
        raw = StringIO(f.read())
    return raw

def hook():
    print("Exception caught, retrying")

def retry_mock(max_tries, delay=1, backoff=2, exceptions=(Exception,), hook=None):
    print 'mock retry called'
    def dec(func):
        def f2(*args, **kwargs):
            try:
               return func(*args, **kwargs)
            except exceptions as e:
                hook()
