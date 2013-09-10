import nose.tools
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

    def test_extracts_listings_from_page(self):
        l = whlisting.WHListing()
        test_min = 25
        test_max = 31
        exp = len(l.listing) > test_min and len(l.listing) < test_max
        nose.tools.ok_(exp, "Number of items out of acceptable range")