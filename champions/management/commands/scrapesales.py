#!/usr/bin/env python

import feedparser
import urllib2
import re
from django.core.management.base import BaseCommand
from champions.models import Champion
from bs4 import BeautifulSoup


class SaleFinder(object):
    def __init__(self, skins, champions):
        """Initializes a SaleFinder.
                skins -> List of skin names
                campions -> List of champion names"""
        self.skins = skins
        self.champions = champions
        self.price_regex = re.compile('(\d+)\s+RP', re.MULTILINE)

    def get_articles(self, url):
        """Returns a list of tuples in the form of (published, title, link)
        for all articles in `url`"""
        d = feedparser.parse(url)
        return [(e['published_parsed'], e['title'], e['link']) for e in d['entries']]

    def extract_sales(self, url):
        """Extracts the new price of skins and champions"""
        opener = urllib2.build_opener()
        url_opener = opener.open(url)
        page = url_opener.read()
        soup = BeautifulSoup(page)

        soup = soup(attrs='article_body')[0]
        list_items = [li.text for li in soup.find_all('li')]

        sales = []
        for li in list_items:
            sale = {}

            # look for skin names
            for skin in self.skins:
                if skin in li:
                    sale['item'] = skin
                    sale['type'] = "skin"
                    print "Skin name found: " + skin

            # if no skin name, look for champion names
            if 'item' not in sale:
                for champion in self.champions:
                    if champion in li:
                        sale['item'] = champion
                        sale['type'] = "champion"
                        print "Champion name found: " + champion

            # if eith skin or champion, look for price
            if 'item' in sale:
                price_regex_result = self.price_regex.search(li)
                if price_regex_result.group(1):
                    sale['price'] = price_regex_result.group(1)
                    print "\tPrice found: " + sale['price']
                    sales.append(sale)

        return sales


class Command(BaseCommand):
    help = 'Scrape champions and update the database'

    def handle(self, *args, **options):
        skins = [
            'Veigar Greybeard',
            'Ironscale Shyvana',
            'Gangster Twitch',
            'Blah Skin'
        ]

        champions = [x.name for x in Champion.objects.all()]
        print "Champions:", champions

        s = SaleFinder(skins, champions)
        articles = s.get_articles('http://na.leagueoflegends.com/taxonomy/term/22/all/feed')
        url = articles[1][2]

        sales = s.extract_sales(url)

        print "Sales:", sales
