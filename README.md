Library for grabbing job listings from hacker news.
===================================================
[![Build Status](https://travis-ci.org/joshz/whoishiring.png)](https://travis-ci.org/joshz/whoishiring)

Usage
-----

### whoishiring listing
Get all [user whoishiring](https://news.ycombinator.com/submitted?id=whoishiring)'s submissions
```
In [1]: from whoishiring import whlisting

In [2]: bydate = whlisting.WHListing()
```

`WHListing` is a class that behaves like collections.OrderedDict. It holds all the posts submitted by whoishiring.

You can index an instance of that class by date of the first day of a month
```
In [3]: from datetime import date

In [4]: bydate[date(2013, 7, 1)]
Out[4]:
[HNListingItem(title='Ask HN: Freelancer? Seeking freelancer? (July 2013)', permanent=False, url='item?id=5970190', date=datetime.date(2013, 7, 1)),
 HNListingItem(title='Ask HN: Who is hiring? (July 2013)', permanent=True, url='item?id=5970187', date=datetime.date(2013, 7, 1))]
```
and you'll receive a list of named tuples containing title, url, date and whether it's a perm or freelance listing for that date.

If you're only interested in the latest postings do
```
In [7]: bydate.latest
Out[7]:
[HNListingItem(title='Ask HN: Freelancer? Seeking freelancer? (September 2013)', permanent=False, url='item?id=6310240', date=datetime.date(2013, 9, 1)),
 HNListingItem(title='Ask HN: Who is hiring? (September 2013)', permanent=True, url='item?id=6310234', date=datetime.date(2013, 9, 1))]
```

Or if you're interested only in latest freelance postings
```
In [6]: bydate.latest.freelance
Out[6]: HNListingItem(title='Ask HN: Freelancer? Seeking freelancer? (September 2013)', permanent='freelance', url='item?id=6310240', date=datetime.date(2013, 9, 1))
```

Similarly, you can get permanent postings from January 2013 like this
```
In [8]: d=date(2013, 1, 1)
In [9]: bydate[d].permanent
Out[9]: HNListingItem(title='Ask HN: Who is hiring? (January 2013)', permanent='permanent', url='item?id=4992617', date=datetime.date(2013, 1, 1))

```

### Job listings for particular date
You can ask for jobs from specific date by passing `HNListingItem` from WHListing. Really you need a named tuple that has a date. Job listing is iterable. Each index holds a dictionary with information about the comment:
* html
* text
* url
* author
* date
* permanent <- this is a string, not a boolean like in the HNListingItem
* parent_thread

```
In [10]: from whoishiring import joblisting

In [11]: j = joblisting.JobListing(bydate.latest.permanent)

In [12]: j.date
Out[12]: datetime.date(2013, 9, 1)

In [13]: for v in j:
   ....:     print v['author']
   ....:
user?id=author1
user?id=author2
user?id=author3
user?id=author4
user?id=author5
...

In [14]: len(j)
Out[14]: 369
```

That's prety much it.
