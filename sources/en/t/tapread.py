# -*- coding: utf-8 -*-
import logging
from urllib.parse import urlparse
from lncrawl.core.crawler import Crawler

logger = logging.getLogger(__name__)

chapter_list_url = "https://www.tapread.com/book/contents?bookId=%s"
chapter_url = "https://www.tapread.com/book/chapter?bookId=%s&chapterId=%s"


class TapreadCrawler(Crawler):
    base_url = "https://www.tapread.com/"

    def read_novel_info(self):
        logger.debug("Visiting %s", self.novel_url)
        soup = self.get_soup(self.novel_url)

        possible_title = soup.select_one(".book-name")
        assert possible_title, "No novel title"
        self.novel_title = possible_title.text.strip()
        logger.info("Novel title: %s", self.novel_title)

        possible_image = soup.select_one("img.bg-img, img.cover-img, .book-img img")
        if possible_image:
            self.novel_cover = self.absolute_url(possible_image["src"])
        logger.info("Novel cover: %s", self.novel_cover)

        try:
            possible_authors = []
            for div in soup.select(".author, .translator"):
                possible_authors.append(
                    ": ".join([x.strip() for x in div.text.split(":")])
                )
            self.novel_author = ", ".join(possible_authors)
        except Exception:
            pass
        logger.info(self.novel_author)

        path = urlparse(self.novel_url).path
        book_id = path.split("/")[3]
        data = self.get_json(chapter_list_url % book_id)

        volumes = set()
        for chap in data["result"]["chapterList"]:
            chap_id = chap["chapterNo"]
            vol_id = (chap_id - 1) // 100 + 1
            volumes.add(vol_id)
            self.chapters.append(
                {
                    "id": chap_id,
                    "volume": vol_id,
                    "title": chap["chapterName"],
                    "url": chapter_url % (chap["bookId"], chap["chapterId"]),
                }
            )

        self.volumes = [{"id": x} for x in volumes]

    def download_chapter_body(self, chapter):
        data = self.get_json(chapter["url"])
        return data["result"]["content"]
