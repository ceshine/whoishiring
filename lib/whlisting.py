from random import randint
from pyquery import PyQuery as pq
from lxml.html import parse
from dateutil.parser import parse as date_parse
from datetime import timedelta, datetime
import re
import time
from collections import namedtuple
import logging
import utils
from base import Base
from urlparse import urljoin


logger = logging.getLogger('lib.whlisting')


# A list of those is returned after parsing the listing page for whoishiring account
Item = namedtuple('HNListingItem', ['title', 'permanent', 'url', 'date'], verbose=False)


class Error(Exception):
    pass


class ListingError(Error):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


class WHListing(Base):
    _date_rx = r'.*\((.+)\).*'
    datere = re.compile(_date_rx)

    def __init__(self):
        self.listing = []
        #TODO: I don't know about this
        self.__call__()

    def __iter__(self):
        return iter(self.listing)

    def __call__(self):
        """Get listing from HN user whoishiring

        Returns:
         List of named tuples containing title, url, date, is_freelance[T/F] indicator for each listing
        """
        items = []
        try:
            nextpage = Base.SUBMISSION_URL
            while True:
                listing_page, nextpage = self._prepare_listing_page(urljoin(Base.HN_BASE_URL, nextpage))
                items.extend(listing_page)

                # if nextpage == None then that means
                if not nextpage:
                    self.listing = items
                    return items
                logging.info("Grabbing next page: %s", nextpage)
        except:
            logger.error("Error getting all submissions")
            return None


    def _prepare_listing_page(self, url=Base.SUBMISSION_URL):
        """Get single page with url

        Args:
         url: url of page to download listings from

        Returns:
         List of Item elements
        """
        items = []

        rawpage = utils.get_raw_page(url)

        try:
            page = pq(rawpage.read())
        except TypeError:
            logger.error("Error parsing raw page")
            raise

        listing = page.find('.title a')
        for i in listing:
            url = pq(i).attr('href')
            perm = 'freelance' not in i.text.lower()
            title = i.text.strip()

            # skip item if it has no date, like (January 2012) in title, probably not a job listing
            try:
                items.append(Item(title=title,
                                  permanent=perm,
                                  url=url,
                                  date=date_parse(self.datere.match(title).group(1)).date()
                ))
            except AttributeError:
                logger.info('SKIPPING: %s', title)

        try:
            if listing[-1].text == 'More':
                return items, url
            else:
                return items, None
        except IndexError:
            logging.error("Can't prepare submission, you may be rate limited.")
            raise