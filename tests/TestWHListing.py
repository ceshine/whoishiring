import nose.tools as nt
from lib import whlisting, utils
from mock import patch
from spec import Spec
import mocks
from datetime import date
from random import randint
from itertools import izip


class TestWHListing(Spec):
    def setup(self):
        self.patcher_ep = patch.object(utils,
                                       'get_raw_page',
                                       autospec=True,
                                       return_value=mocks.get_page('%s/tests/data/whoishiring.html'))
        self.patcher_ep.start()
        self.idate = date(2012, 12, 1)

    def teardown(self):
        self.patcher_ep.stop()

    def test_listing_has_non_zero_length(self):
        l = whlisting.WHListing()
        nt.ok_(len(l) == 14, "Not a correct number of items in listing")

    def test_indexing_listing(self):
        l = whlisting.WHListing()
        nt.ok_("December 2012" in l[self.idate][randint(0, 1)].title, "Item doesn't contain correct string")

    def test_out_of_index_raises_IndexError(self):
        l = whlisting.WHListing()
        with nt.assert_raises(IndexError):
            l[self.idate][3]

    def test_iterating_over_submissions(self):
        l = whlisting.WHListing()
        for item in l[self.idate]:
            nt.eq_(item.date, self.idate, "Item doesn't have a correct date")

    def test_access_by_attribute(self):
        l = whlisting.WHListing()
        idate = date(2012, 12, 1)
        nt.ok_("December 2012" in l[idate].permanent.title, "Item doesn't contain correct string")
        nt.ok_("December 2012" in l[idate].freelance.title, "Item doesn't contain correct string")

    def test_iterates_in_order_over_listing(self):
        l = whlisting.WHListing()
        dates = [(2013, 3, 1),
                (2013, 2, 1),
                (2013, 1, 1),
                (2012, 12, 1),
                (2012, 11, 1),
                (2012, 10, 1),
                (2012, 9, 1),
                (2012, 8, 1),
                (2012, 7, 1),
                (2012, 6, 1),
                (2012, 5, 01),
                (2012, 4, 1),
                (2012, 3, 1),
                (2012, 2, 1)]

        for (k, v), d in izip(l.iteritems(), dates):
            nt.ok_(isinstance(v[randint(0, 1)], whlisting.Item), "Item not an instance of Item")
            nt.eq_(date(*d), k, "Iterating not in order")

    def test_returns_correct_latest(self):
        l = whlisting.WHListing()
        nt.eq_(l.keys()[0], date(2013, 3, 1), "Bad date for the latest item")
        nt.eq_(l.latest[0].date, date(2013, 3, 1), "Bad date for the latest item")