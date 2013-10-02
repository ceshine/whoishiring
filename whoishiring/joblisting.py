from pyquery import PyQuery as pq
from lxml.html import parse
import time
import logging
import utils
from base import Base
from urlparse import urljoin


logger = logging.getLogger('whoishiring.joblisting')


class JobListing(Base):
    def __init__(self, listing_item, delay=0):
        logger.debug("Processing %s", listing_item)
        self.date = listing_item.date
        self.title = listing_item.title
        self.permanent = listing_item.permanent
        self.url = listing_item.url
        self.comments = []
        self._raw_comments = []

        self._fetch_comments(delay)

    def __iter__(self):
        return iter(self.comments)

    def __len__(self):
        return len(self.comments)

    def __str__(self):
        return '{} comments from thread {}, taken on {} for {} listings'.format(
            len(self.comments),
            self.url,
            self.date,
            self.permanent
        )

    def __getitem__(self, item):
        return self.comments[item]

    def _fetch_comments(self, delay=0):
        """Return a list of comments from an hn post with given link, delay is a fuzzing thing, probably useless

        Args:
         listing_item: string value, like '/item?id=3412900' with article id, from _get_all_submissions
         delay: be nice and wait between requests, or not
        """

        try:
            link = self.url
            # for (comments, link) in iter(partial(self._extract_raw_comments, link), None):
            #     self._process_comments(comments)

            while True:
                logger.info('processing page: %s', link)

                raw = utils.get_raw_page(urljoin(Base.HN_BASE_URL, link))
                logger.debug('Got raw page, parsing...')
                page = parse(raw)
                logger.debug('Extracting comments and next page...')
                # [:-2] the last two are some spacers
                comments = self._extract_raw_comments(page)[:-1]
                link = self._extract_next_url(page)
                logger.debug('Processing comments...')
                self._process_comments(comments)
                if link:
                    logger.info('Waiting %s seconds...', delay)
                    time.sleep(delay)
                else:
                    logger.info("Downloaded all comments under submission %s", self.title)
                    break
        except:
            raise

    def _process_comments(self, comments):
        for comment in comments:
            self._process_comment(comment)

    def _extract_raw_comments(self, page):
        """Extracts comments from raw page

        Args:
         page: ElementTree object with page contents
        Returns:
         List of comments extracted from page in lxml.html.HtmlElement format
        """
        return page.xpath(Base.COMMENT_XPATH)

    def _extract_next_url(self, page):
        """Extract next link from page

        Args:
         page: ElementTree object with page contents
        Returns:
         URL for next page or None
        """
        try:
            nextpage = page.xpath(Base.NEXT_PAGE_XPATH)[0].attrib['href']
        except IndexError:
            nextpage = None

        return nextpage

    def is_tlc(self, comment):
        """Decide if comment is a top level comment, not a response

        Args:
         comment: PyQuery object

        Returns a lower level element with class default if img element's width is 0 else false
        """
        try:
            img = comment.find('img')[0]
        except IndexError:
            return False

        return img.attrib['width'] == '0'

    def _process_comment(self, comment):
        """Arranges comment into a dictionary containing some meta data about the comment

        Args:
         comment: html of the comment
        """
        cpq = pq(comment)

        a = cpq('.comhead').find('a')

        contents = cpq('.comment')

        self.comments.append({
            'html': contents.html().encode('utf-8'),
            'text': contents.text(),
            'url' : a.eq(1).attr.href,
            'author': a.eq(0).attr.href,
            'date': self.date,
            'permanent': self.permanent,
            'parent_thread': self.url
        })
