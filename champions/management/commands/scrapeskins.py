
from django.core.management.base import BaseCommand, CommandError

import urllib2
import urlparse
from bs4 import BeautifulSoup
from bs4.element import Tag
from champions.models import Champion, Skin
import re


# This scraper uses the league of legends wika, so it may not be constantly up to date

class SkinScraper(object):
    RE_SKIN = re.compile('Skin Name')

    def skins(self, url):
        opener = urllib2.build_opener()
        url_opener = opener.open(url)
        soup = BeautifulSoup(url_opener)

        # Find table header cells that fit skin tables
        table_headers = soup('th', text=self.RE_SKIN)

        # Find the tables that hold the header cells
        skin_tables = [x.find_parent('table') for x in table_headers]

        for skin_table in skin_tables:
            for skin_row in skin_table('tr'):
                data = [x for x in skin_row.contents if isinstance(x, Tag)]

                if len(data) < 1:
                    continue

                c_name = data[0].find('b')

                if not c_name:
                    continue

                c_name = c_name.find('a')

                if not c_name:
                    continue

                if c_name:
                    champion = c_name['title'].split('/', 1)[0]
                    yield champion, c_name.text

SKIN_URL = 'http://leagueoflegends.wikia.com/wiki/Champion_skin'

class Command(BaseCommand):
    help = 'Scrape skins and update the database'

    def __init__(self):
        self.scraper = SkinScraper()
        self.champions = dict((x.name, x) for x in Champion.objects.all())

    def handle(self, *args, **options):
        for c_name, s_name in self.scraper.skins(SKIN_URL):
            skin = Skin()
            skin.name = s_name


            s_name = s_name.lower()
            c_name = c_name.lower()

            for name, champion in self.champions.iteritems():
                if name.lower() in c_name or name.lower() in s_name:
                    skin.champion = champion
                    break

            try:
                _ = skin.champion
            except Champion.DoesNotExist:
                print s_name
                exit()

            skin.save()
