import argparse
import logging
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scraping import settings as settings_local
from scraping.spiders import google_reviews, selenium_spider

logger = logging.getLogger(__name__)


def entrypoint():
    """

    :return:
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--company_name',
        type=str,
        required=True,
    )

    parser.add_argument(
        '--browser',
        default='CHROME',
        choices=['FIREFOX', 'CHROME'],
    )

    options = parser.parse_args(sys.argv[1:])

    try:
        company_crawler = google_reviews.GoogleReviewScraper(options.company_name)
    except KeyError as exc:
        msg = 'Google Reviews Scrape crawler is not found.'
        context = {'spider': 'Google Reviews'}
        logger.error(msg, context, exc_info=exc)

        return

    logger.debug(
        f'Crawling reviews of {options.company_name}.'
    )

    settings = Settings()
    settings.setmodule(settings_local)
    crawler = CrawlerProcess(settings)

    if issubclass(company_crawler, selenium_spider.SeleniumSpider):
        with selenium_spider.driver_context(options.browser) as driver:
            company_crawler.driver = driver
            crawler.crawl(company_crawler)
            crawler.start()
    else:
        crawler.crawl(company_crawler)
        crawler.start()

    logger.info('Done.')
