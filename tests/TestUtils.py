import nose.tools as nt
from lib import utils
from mock import patch
from spec import Spec
import urllib2

class TestWHListing(Spec):
    def setup(self):
        pass
    def teardown(self):
        pass

    @patch("urllib2.urlopen")
    def test_get_raw_page(self, urlopen_mock):
        with open('data/whoishiring.html', 'r') as f:
            urlopen_mock.return_value = f
            nt.ok_('http://ycombinator.com' in utils.get_raw_page('fake_page').read(),
                   "It doesn't appear the the correct file was read")

    @patch("urllib2.urlopen")
    def test_get_raw_page_network_error(self, urlopen_mock):
        with nt.assert_raises(urllib2.URLError):
            e = urllib2.URLError("not a real error")
            urlopen_mock.side_effect = e
            utils.get_raw_page('fake_somepage')