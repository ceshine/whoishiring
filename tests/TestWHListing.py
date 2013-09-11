import nose.tools as nt
from lib import whlisting, utils
from mock import patch
from spec import Spec
import mocks


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
        nt.ok_(len(l) > 20 and len(l) < 40)

    def test_extracts_listings_from_page(self):
        l = whlisting.WHListing()
        test_min = 25
        test_max = 31
        exp = len(l.listing) > test_min and len(l.listing) < test_max
        nt.ok_(exp, "Number of items out of acceptable range")

    def test_iterates_over_listing(self):
        l = whlisting.WHListing()
        for item in l:
            nt.ok_(isinstance(item, whlisting.Item), "item not an instance of Item")