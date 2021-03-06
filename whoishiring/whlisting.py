from pyquery import PyQuery as pq
from dateutil.parser import parse as date_parse
import re
from collections import namedtuple
import logging
import utils
from base import Base
from urlparse import urljoin
from collections import OrderedDict
from datetime import date


logger = logging.getLogger('whoishiring.whlisting')


# A list of those is returned after parsing the listing page for whoishiring account
Item = namedtuple('HNListingItem', ['title', 'permanent', 'url', 'date'], verbose=False)


class Error(Exception):
    pass


class ListingError(Error):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


class PFSubmissions(object):
    def __init__(self):
        self.permanent = None
        self.freelance = None

    def __getitem__(self, item):
        # self.__dict__.values()[item]
        #TODO: I don't know about this
        if item not in (0, 1):
            raise IndexError
        else:
            return self.permanent if item else self.freelance

    def __iter__(self):
        return self.__dict__.itervalues()

    def __unicode__(self):
        return '[{},\n{}]'.format(self.permanent, self.freelance)

    def __str__(self):
        return unicode(self).encode('utf-8')

class WHListing(OrderedDict, Base):
    datere = re.compile(Base.DATE_RX)

    def __init__(self):
        # self.listing = []
        super(WHListing, self).__init__()
        self._get()

    def __unicode__(self):
        return '{{{}}}'.format('\n'.join([item.__str__() for item in self.values()]))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __missing__(self, key):
        if isinstance(key, date):
            self[key] = PFSubmissions()
            return self[key]
        raise KeyError

    def _get(self):
        """Get listing from HN user whoishiring and make available
        """
        try:
            nextpage = Base.SUBMISSION_URL
            while True:
                nextpage = self._prepare_listing_page(urljoin(Base.HN_BASE_URL, nextpage))

                # if nextpage == None then that means
                if not nextpage:
                    return self
                logging.info("Grabbing next page: %s", nextpage)
        except:
            logger.error("Error getting all submissions")
            raise


    def _prepare_listing_page(self, url=Base.SUBMISSION_URL):
        """Get single page with url

        Args:
         url: url of page to download listings from
        """
        def _decide_perm(title):
            if Base.PERMANENT_TITLE in title:
                return 'permanent'
            elif Base.FREELANCE_TITLE in title:
                return 'freelance'
            else:
                raise ValueError

        rawpage = utils.get_raw_page(url)

        try:
            page = pq(rawpage.read())
        except TypeError:
            logger.error("Error parsing raw page")
            raise

        listing = page.find('.title a')
        for i in listing:
            url = pq(i).attr('href')
            title = i.text.strip()

            # skip item if it has no date, like (January 2012) in title, probably not a job listing
            try:
                item_date = date_parse(self.datere.match(title).group(1)).date()
                idate = date(item_date.year, item_date.month, 1)
                position = _decide_perm(title.lower())
                setattr(self[idate], position, Item(title=title,
                                                  permanent=position,
                                                  url=url,
                                                  date=idate
                                               ))
            except (AttributeError, ValueError) as e:
                logger.info('SKIPPING: %s, error: %s', title, e)

        try:
            if listing[-1].text == 'More':
                return url
            else:
                return None
        except IndexError:
            logging.error("Can't prepare submission, you may be rate limited.")
            raise

    @property
    def latest(self):
        """Return the latest submissions, PFSubmissions object
        """
        return self[next(iter(self))]
