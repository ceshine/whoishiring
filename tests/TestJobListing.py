import nose.tools as nt
from lib import utils
from mock import patch
from spec import Spec
import mocks
from datetime import date
from lib.joblisting import JobListing
from collections import namedtuple


Item = namedtuple('HNListingItem', ['title', 'permanent', 'url', 'date'], verbose=False)


class TestWHListing(Spec):
    def setup(self):
        self.patcher_ep = patch.object(utils,
                                       'get_raw_page',
                                       autospec=True,
                                       return_value=mocks.get_page('%s/tests/data/dec2012.html'))
        self.patcher_ep.start()
        self.d = date(2013, 3, 1)
        self.item = Item('test title', True, 'http://fakeurl.com/stuff', self.d)

    def teardown(self):
        self.patcher_ep.stop()

    def test_listing_has_nonzero_length(self):
        j = JobListing(self.item)
        nt.eq_(len(j), 103, "Incorrect object length")
        print j

    def test_comment_from_correct_date_and_indexing(self):
        j = JobListing(self.item)
        nt.eq_(j[10]['date'], self.d, "Incorrect date")

    def test_prints_human_readable_str(self):
        j = JobListing(self.item)
        nt.ok_('103' in j.__str__(), "Incorrect or unreadable str")

    def test_iterates_over_comments(self):
        j = JobListing(self.item)
        for comment in j:
            nt.ok_('parent_thread' in comment, 'Iterates over comments in JobListing')