#!/usr/bin/env python

from django.core.management.base import BaseCommand, CommandError

import urllib2
import urlparse
from bs4 import BeautifulSoup
from champions.models import Champion

class LeagueScraper(object):
    def __init__(self):
        pass

    def champions(self, url, details=True):
        opener = urllib2.build_opener()
        url_opener = opener.open(url)
        soup = BeautifulSoup(url_opener)

        soup = soup(attrs='champion_item')

        for champion in soup:
            s_champ = champion(attrs='champion')[0]
            s_description = champion(attrs='description')[0]

            # Build the detail url
            detail_url = s_champ.find('a', recursive=False)['href']
            detail_url = urlparse.urljoin(url, detail_url)

            info = {
                'detail_url': detail_url,
                'icon_url': s_champ.find('img')['src'],
                'name': s_description.find(attrs='highlight').find('a').text,
                'short_description': s_description.find('p').text
            }

            # Get the full detail page
            if details:
                detail_soup = BeautifulSoup(opener.open(detail_url))
                image_url = urlparse.urljoin(detail_url, detail_soup.find(attrs='champion_render').find('img')['src'])
                info.update({
                    'title': detail_soup.find(attrs='champion_title').text,
                    'image_url': image_url,
                    'description': detail_soup.find(attrs='champion_description').text
                })

            yield info


CHAMPION_URL = 'http://na.leagueoflegends.com/champions'


class Command(BaseCommand):
    help = 'Scrape champions and update the database'

    def __init__(self):
        self.scraper = LeagueScraper()

    def handle(self, *args, **options):
        for champion in self.scraper.champions(CHAMPION_URL):
            (obj, created) = Champion.objects.get_or_create(name=champion['name'],
                                defaults={'title': champion['title'],
                                            'detail_url': champion['detail_url'],
                                            'icon_url': champion['icon_url'],
                                            'image_url': champion['image_url'],
                                            'short_description': champion['short_description'],
                                            'description': champion['description']})
            obj.save()
