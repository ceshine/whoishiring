import nose.tools as nt
from lib import whlisting, utils
from mock import patch
from spec import Spec
import mocks
from datetime import date
from random import randint


class TestWHListing(Spec):
    def setup(self):
        self.patcher_ep = patch.object(utils,
                                       'get_raw_page',
                                       autospec=True,
                                       return_value=mocks.get_page('%s/tests/data/whoishiring.html'))
        self.patcher_ep.start()

    def teardown(self):
        self.patcher_ep.stop()

    def test_listing_has_non_zero_length(self):
        l = whlisting.WHListing()
        nt.ok_(len(l) == 14, "Not a correct number of items in listing")

    def test_indexing_listing(self):
        l = whlisting.WHListing()
        idate = date(2012, 12, 1)
        nt.ok_("December 2012" in l[idate][1].title, "Item doesn't contain correct string")

    def test_iterates_over_listing(self):
        l = whlisting.WHListing()
        for k, v in l.iteritems():
            nt.ok_(isinstance(v[randint(0, 1)], whlisting.Item), "Item not an instance of Item")