import logging
from lncrawl.templates.novelmtl import NovelMTLTemplate

logger = logging.getLogger(__name__)


class WuxiaUCrawler(NovelMTLTemplate):
    base_url = "https://www.wuxiau.com/"
