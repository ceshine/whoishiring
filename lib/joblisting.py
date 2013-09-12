from pyquery import PyQuery as pq
from lxml.html import parse
import time
import logging
import utils


logger = logging.getLogger('lib.joblisting')


class JobListing(object):
    NEXT_PAGE_XPATH = '/html/body/center/table/tr[3]/td/table/tr[last()]/td/a/@href'
    COMMENT_XPATH = '//td[@class="default"]'

    def __init__(self, listing_item):
        self.date = listing_item.date
        self.title = listing_item.title
        self.permanent = listing_item.permanent
        self.url = listing_item.url
        self.comments = []

        self._fetch_comments()

    def __iter__(self):
        return iter(self.comments)

    def __len__(self):
        return len(self.comments)

    def __str__(self):
        return '{} comments from thread {}, taken on {} for {} listings'.format(
            len(self.comments),
            self.url,
            self.date,
            'permanent' if self.permanent else 'freelance'
        )

    def __getitem__(self, item):
        return self.comments[item]

    def _fetch_comments(self, delay=0):
        """Return a list of comments from an hn post with given link, delay is a fuzzing thing, probably useless

        Args:
         listing_item - string value, like '/item?id=3412900' with article id, from _get_all_submissions
         delay - be nice and wait between requests, or not
        """

        try:
            link = self.url
            while True:
                logger.info('page: %s', link)

                raw = utils.get_raw_page(link)
                comments, link = self._extract_raw_comments(raw)

                logger.info('\tfetched %s comments', len(comments))

                self._process_comments(comments)

                if link:
                    #TODO: don't run this?
                    time.sleep(delay)
                else:
                    break
        except:
            raise("Error occured when fetching comments for %s", self.title)

    def _process_comments(self, comments):
        for comment in comments:
            self._process_comment(comment)

    def _extract_raw_comments(self, raw):
        """Extracts comments from raw page, puts them in the list

        Args:
         File-like object, result of get_raw_page or file name, whatever lxml parse would expect
        Returns:
         List of comments extracted from page in lxml.html.HtmlElement format
        """
        page = parse(raw)
        comments = page.xpath(self.COMMENT_XPATH)
        try:
            nextpage = page.xpath(self.NEXT_PAGE_XPATH)[0]
        except IndexError:
            nextpage = None

        return comments, nextpage

    def _process_comment(self, comment):
        """Arranges comment into a dictionary containing some meta data about the comment

        Args:
         comment: html of the comment
         parent: parent thread (not parent comment) of the comment
         date: date of the posting of parent thread
         permanent: Boolean of whether the comment came from freelance or regular posting

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
