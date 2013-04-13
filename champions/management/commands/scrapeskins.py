
from django.core.management.base import BaseCommand, CommandError

import urllib2
import urlparse
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from champions.models import Champion, Skin
import re


# This scraper uses the league of legends wika, so it may not be constantly up to date

class SkinScraper(object):
    def skins(self, url):
        opener = urllib2.build_opener()
        url_opener = opener.open(url)
        soup = BeautifulSoup(url_opener)

        # Find root element for every skin
        skins = soup.findAll('div', {'class' : 'thumbinner'})


        for skin in skins:
            if skin.div.b.a: #checks for the Riot Points logo because then we know the skin is actually in the store
                skin_name = skin.div.b.i.contents[0]
                skin_url = BASE_URL + skin.find('img', {'class' : 'thumbimage'})['src']

                #Some skins have this random space that throws off the index of the proper string in contents
                #cost_string = skin.div.b.contents[1] if type(skin.div.b.contents[1]) == NavigableString else skin.div.b.contents[2]
                #skin_cost = int(cost_string.replace('-','').replace(',','').strip())

                skin_cost = int(skin.div.b.text.split(' - ')[1].replace('-','').replace(',','').strip())

                yield skin_name, skin_url, skin_cost

BASE_URL = 'http://leaguepedia.com'

class Command(BaseCommand):
    help = 'Scrape skins and update the database'

    def __init__(self):
        self.scraper = SkinScraper()

    def handle(self, *args, **options):
        for champion in Champion.objects.all():
            name = champion.name.replace(' ', '_')
            URL = BASE_URL + '/wiki/' + name

            print "Scraping Skins For:   "+ champion.name

            #Special cases
            if champion.name == 'Dr. Mundo':
                URL = 'http://leaguepedia.com/wiki/Dr._Mundo_-_The_Madman_of_Zaun'
            elif champion.name == 'Master Yi':
                URL = 'http://leaguepedia.com/wiki/Master_Yi_-_The_Wuju_Bladesman'

            for skin_name, skin_url, skin_cost in self.scraper.skins(URL):
                skin = Skin()

                skin.champion = champion
                skin.name = skin_name
                skin.icon_url = skin_url
                skin.cost = skin_cost

                skin.save()

