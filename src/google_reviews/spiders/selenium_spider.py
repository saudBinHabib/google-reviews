import os
from contextlib import contextmanager

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumSpider():
    driver = None

    def parse(self):
        """

        :param response:
        :return:
        """
        raise NotImplementedError()


@contextmanager
def driver_context():

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')


    # windows webdriver capabilities.
    # capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    # capabilities["loggingPrefs"] = {"performance": "ALL"}  # newer: goog:loggingPrefs
    # capabilities['platform'] = "WINDOWS"
    # capabilities['version'] = "10"

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    # creating driver using  windows driver.
    # driver = webdriver.Chrome(
    #     executable_path='geckodriver.exe',
    #    desired_capabilities=capabilities,
    #     options=options
    # )

    try:
        yield driver
    finally:
        driver.quit()
