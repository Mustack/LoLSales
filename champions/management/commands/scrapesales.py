#!/usr/bin/env python

import feedparser
import urllib2
from bs4 import BeautifulSoup

class SaleFinder(object):
    def __init__(self, skins, champions):
        """Initializes a SaleFinder.
                skins -> List of skin names
                campions -> List of champion names"""
        self.skins = skins
        self.champions = champions

    def get_articles(self, url):
        """Returns a list of tuples in the form of (published, title, link)
        for all articles in `url`"""
        d = feedparser.parse(url)
        return [(e['published_parsed'], e['title'], e['link']) for e in d['entries']]

    def extract_sale(self, url):
        """Extracts the new price of skins and champions"""
        opener = urllib2.build_opener()
        url_opener = opener.open(url)
        page = url_opener.read()
        soup = BeautifulSoup(page)

        soup = soup(attrs='article')
        print soup

s = SaleFinder([], [])
articles = s.get_articles('http://na.leagueoflegends.com/taxonomy/term/22/all/feed')
url = articles[0][2]
print url

print s.extract_sale(url)
