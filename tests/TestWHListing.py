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

    def test_indexing_listing(self):
        l = whlisting.WHListing()
        nt.ok_("December 2012" in l[7].title, "Item is from correct date")

    def test_iterates_over_listing(self):
        l = whlisting.WHListing()
        for item in l:
            nt.ok_(isinstance(item, whlisting.Item), "item not an instance of Item")