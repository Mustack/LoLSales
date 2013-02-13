#!/usr/bin/env python

import feedparser
import urllib2
import re
from django.core.management.base import BaseCommand
from champions.models import Champion, Skin
from bs4 import BeautifulSoup
import parsedatetime as pdt
from datetime import datetime, timedelta

# http://stackoverflow.com/a/5903760
def to_datetime( result, what ):
    dt = None

    # what was returned (see http://code-bear.com/code/parsedatetime/docs/)
    # 0 = failed to parse
    # 1 = date (with current time, as a struct_time)
    # 2 = time (with current date, as a struct_time)
    # 3 = datetime
    if what in (1,2):
        # result is struct_time
        dt = datetime( *result[:6] )
    elif what == 3:
        # result is a datetime
        dt = result

    if dt is None:
        # Failed to parse
        raise ValueError, ("Don't understand date")

    return dt

class SaleFinder(object):
    def __init__(self, skins, champions):
        """Initializes a SaleFinder.
                skins -> List of skin names
                campions -> List of champion names"""
        self.skins = skins
        self.champions = champions
        self.price_regex = re.compile('(\d+)\s+RP', re.MULTILINE)
        self.date_regex = re.compile(r'^[ \t]*[a-zA-Z]+( )+([1-9][0-9]?)[ \t]*$')

    def get_articles(self, url):
        """Returns a list of tuples in the form of (published, title, link)
        for all articles in `url`"""
        d = feedparser.parse(url)
        return [(e['published_parsed'], e['title'], e['link']) for e in d['entries']]

    def _extract_date(self, detail, body):
        posted_date = datetime.strptime(detail.find('span', attrs='date').text, '%a, %Y-%m-%d %H:%M')
        constants = pdt.Constants()
        constants.Year = posted_date.year

        # Wrap the year around if the date is past december
        if posted_date.month == 12:
            constants.Year = (posted_date + timedelta(years=1)).year

        constants.YearParseStyle = 0
        calendar = pdt.Calendar(constants)

        comment_link = body.find(text='Click here to comment')

        dates = []
        for x in comment_link.find_parent('p').find_all_previous('b', text=self.date_regex, limit=2):
            x = calendar.parse(x.text)
            x = to_datetime(*x)
            x = x.date()
            dates.append(x)
        dates.sort()
        return dates

    def extract_sales(self, url):
        """Extracts the new price of skins and champions"""
        if 'champion-skin-sale' not in url:
            return ([], [])
        opener = urllib2.build_opener()
        url_opener = opener.open(url)
        page = url_opener.read()
        s = BeautifulSoup(page)

        soup = s(attrs='article_body')[0]
        detail = s(attrs='article_detail')[0]
        dates = self._extract_date(detail, soup)
        list_items = [li.text for li in soup.find_all('li')]

        sales = []
        for li in list_items:
            sale = {}

            # look for champion names
            for champion in self.champions:
                if champion in li:
                    # see if it's a skin sale, not a champion sale.
                    for skin in self.skins:
                        if skin.replace(champion, '').strip() in li:
                            sale['item'] = skin
                            sale['type'] = "skin"
                    # if no skin name was found, it is a champion sale
                    if 'item' not in sale:
                        sale['item'] = champion
                        sale['type'] = "champion"

            # if either skin or champion, look for price
            if 'item' in sale:
                price_regex_result = self.price_regex.search(li)
                if price_regex_result.group(1):
                    sale['price'] = price_regex_result.group(1)
                    sale['url'] = url
                    sales.append(sale)

        return (dates, sales)


class Command(BaseCommand):
    help = 'Scrape sales and update the database.'

    def handle(self, *args, **options):
        skins = [x.name for x in Skin.objects.all()]
        print len(skins), 'known skins'

        champions = [x.name for x in Champion.objects.all()]
        print len(champions), 'known champions'

        s = SaleFinder(skins, champions)
        articles = s.get_articles('http://na.leagueoflegends.com/taxonomy/term/22/all/feed')

        urls = [articles[i][2] for i in range(len(articles))]
        print "URLs:\n" + "\n".join(urls)

        sales = []
        for url in urls:
            sales.append(s.extract_sales(url))

        print "Sales:"
        for dates, items in sales:
            for item in items:
                    print "{:>9}: {:<30} for {:>4} RP ({} - {}) \t {}".format(item['type'], item['item'], item['price'], dates[0], dates[1], item['url'])
