import os
from contextlib import contextmanager

from scrapy import Spider
from seleniumwire import webdriver


class SeleniumSpider(Spider):
    driver = None

    def parse(self, response):
        """

        :param response:
        :return:
        """
        raise NotImplementedError()


@contextmanager
def driver_context(browser: str):
    """

    :param browser:
    :return:
    """
    browser = os.getenv(browser)
    host, port = os.getenv('SELENIUM_HOST'), os.getenv('SELENIUM_PORT')
    command_executor = f'http://{host}:{port}/wd/hub'
    capabilities = {'browserName': browser}

    driver = webdriver.Remote(
        command_executor=command_executor,
        desired_capabilities=capabilities,
    )

    try:
        yield driver
    finally:
        driver.quit()


command_executor = f'http://localhost:4444/wd/hub'
capabilities = {'browserName': 'CHROME'}

driver = webdriver.Remote(
    command_executor=command_executor,
    desired_capabilities=capabilities,
)