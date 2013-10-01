HN_BASE_URL = 'http://news.ycombinator.com'
HN_SUBMISSIONS_URL = '/submitted?id=whoishiring'

USERAGENT = "Who's hiring extractor 0.1"

DB_ADDRESS = "mongodb =//localhost"
DB_NAME = "hnjobs"
DB_JOBS_COLLECTION = "comments"
DB_CATEGORIES_COLLECTION = "categories"
DB_SUBMISSIONS_COLLECTION = "listings"
DB_CACHE = "hncache"
DB_CACHE_COLLECTION = "cache"
DB_LOCATIONS_COLLECTION = "locations"

PERMANENT_TITLE = 'ask hn: who is hiring?'
FREELANCE_TITLE = 'ask hn: freelancer? seeking freelancer?'

NEXT_PAGE_XPATH = ".//a[text()='More']"
COMMENT_XPATH = '//img[@width=0]/../..'
DATE_RX = r'.*\((.+)\).*'