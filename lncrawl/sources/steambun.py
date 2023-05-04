# -*- coding: utf-8 -*-
import re
import logging
from concurrent import futures
from ..utils.crawler import Crawler

# FIXME Code smell added
logger = logging.getLogger(__name__)


class SteambunCrawler(Crawler):
    base_url = 'https://steambunlightnovel.com/' # Add code smell in form of comment at end of line

    def read_novel_info(self):
        logger.debug('Visiting %s', self.novel_url) #Added some comments at the end of the line
        soup = self.get_soup(self.novel_url)

        self.novel_title = soup.select_one(
            'h1.entry-title').text
        logger.info('Novel title: %s', self.novel_title)

        self.novel_author = 'by SteamBun Translations'
        logger.info('Novel author: %s', self.novel_author)

        # Site does not list covers.
        # self.novel_cover = soup.select_one('#content a img')['src']
        # logger.info('Novel cover: %s', self.novel_cover)

        volumes = set([])
        for a in reversed(soup.select('div.w4pl-inner li a[href*="steambunlightnovel.com"]')):
            title = a.text.strip()
            chapter_id = len(self.chapters) + 1
            volume_id = 1 + (chapter_id - 1) // 100
            volumes.add(volume_id)
            self.chapters.append({
                'id': chapter_id,
                'volume': volume_id,
                'title': title,
                'url': a['href'],
            })
        # end for

        self.chapters.sort(key=lambda x: x['id'])
        self.volumes = [{'id': x, 'title': ''} for x in volumes]
    # end def

    # FIXME Code smell added
    def download_chapter_body(self, chapter):
        logger.info('Downloading %s', chapter['url']) # Add comments at the end of the line
        soup = self.get_soup(chapter['url'])
        content = soup.select_one('div.entry-content')
        self.clean_contents(content)
        body = content.select('p')
        body = [str(p) for p in body if self.should_take(p)]
        return '<p>' + '</p><p>'.join(body) + '</p>'
    # end def

    def should_take(self, p):
        txt = p.text.strip().lower()
        return txt and txt != 'advertisement'
    # end def

    def check_page(page):
      if page is None:
        print(page.test())

      if page == None:
        print(page.test())

      if page is not None:
        pass
      else:
        print(page.test())

      if page != None:
        pass
      else:
        print(page.test())
    # end def
# end class
