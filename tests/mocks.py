import os
from StringIO import StringIO


def get_page(page):
    """Return raw comment page from the data directory"""
    datadir = os.path.normpath(os.path.abspath(__file__)).split(os.sep)
    datadir = os.sep.join(datadir[:-2])
    with open(page % datadir, 'r') as f:
        raw = StringIO(f.read())
    return raw