import argparse
import logging
import sys

from google_reviews.spiders import GoogleReviewScraper, selenium_spider

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

    options = parser.parse_args(sys.argv[1:])

    logger.debug(
        f'Crawling reviews of {options.company_name}.'
    )

    google_crawler = GoogleReviewScraper(options.company_name)

    with selenium_spider.driver_context() as driver:
        google_crawler.driver = driver
        google_crawler.parse()

    logger.info('Done.')
