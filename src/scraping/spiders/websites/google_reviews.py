
import csv
import logging
import os
import requests

from dataclasses import asdict
from time import sleep

from scraping.spiders.selenium_spider import SeleniumSpider
from scraping.utilities.data_cleaning import process_data, process_reviews

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleReviewScraper(SeleniumSpider):
    name = 'google'
    start_urls = ['https://www.google.com/maps/@50.386969,8.1018231,14z']
    DIR_PATH = os.getcwd()
    TIMEOUT = 10
    MAX_TRIES = 5

    def __init__(self, company_name: str):
        """
        :param company_name:
        """
        self.company_name = company_name
        company_name = company_name.replace(' ', '_')
        self.output_file = os.path.join(self.DIR_PATH, f'{company_name}.csv')

    def click_on_reviews(self, path: str):
        """

        :param path:
        :return:
        """
        num_of_tries = 0
        while True:
            try:
                sleep(1)
                self.driver.find_element(
                    By.XPATH,
                    value=path
                ).click()
                return True
            except TimeoutException as exc:
                num_of_tries += 1
                if num_of_tries > self.MAX_TRIES:
                    return False

    def click_first_organization(self, path):
        """

        :param path:
        :return:
        """

        num_of_tries = 0
        while True:
            try:
                sleep(1)
                self.driver.find_element(
                    By.XPATH,
                    value=path
                ).click()
                return True
            except TimeoutException as exc:
                num_of_tries += 1
                if num_of_tries > self.MAX_TRIES:
                    return False

    def scroll_into_review_pannel(self, path: str):
        """

        :param path:
        :return:
        """
        num_of_tries = 0
        while True:
            try:
                sleep(1)
                review_panel = self.driver.find_element(
                    By.XPATH,
                value=path)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", review_panel)
                return True
            except TimeoutException as exc:
                num_of_tries += 1
                if num_of_tries > self.MAX_TRIES:
                    return False

    def get_all_reviews_requests(self)-> list:
        """

        :return:
        """
        review_requests = self.driver.requests
        return [
            request for request in review_requests if
            request.method == 'GET' and 'https://www.google.com/maps/preview/review/listentitiesreviews' in request.url
        ]

    def write_data_in_csv(self, reviews: list):
        try:
            with open(self.output_file, 'a', newline='') as f:
                fieldnames = ['reviewer_name', 'review_time', 'review', 'rating', 'reply', 'reply_text', 'review_link']
                csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
                csv_writer.writeheader()
                for review in reviews:
                    csv_writer.writerow(asdict(review))
        except Exception as exc:
            msg = 'Got the error while saving CSV.'
            context = {'spider': 'Google Reviews'}
            logger.error(msg, context, exc_info=exc)

    def parse(self, response):
        """

        :param response:
        :return:
        """

        self.driver.get(self.start_urls[0])
        try:
            element_present = EC.presence_of_element_located((
                By.XPATH,
                 '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span'
            ))
            WebDriverWait(self.driver, self.TIMEOUT).until(element_present)

            self.driver.find_element(
                By.XPATH,
                value='//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span'    # noqa
            ).click()
        except TimeoutException as exc:
            msg = 'Cookies can not be accepted properly.'
            context = {'spider': 'Google Reviews'}
            logger.error(msg, context, exc_info=exc)
            return

        try:
            element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="searchboxinput"]'))
            WebDriverWait(self.driver, self.TIMEOUT).until(element_present)
            search_box = self.driver.find_element(By.XPATH, value='//*[@id="searchboxinput"]')
            search_box.send_keys(self.company_name)
            search_box.send_keys(Keys.ENTER)
        except TimeoutException as exc:
            msg = 'Search box could not be found.'
            context = {'spider': 'Google Reviews'}
            logger.error(msg, context, exc_info=exc)
            return

        click_next_item = self.click_on_reviews(
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]'    # noqa
        )

        if click_next_item:
            scrolled = self.scroll_into_review_pannel(
                '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[11]'
            )
            if not scrolled:
                msg = 'Not able to scroll into review panel.'
                context = {'spider': 'Google Reviews'}
                logger.error(msg, context)
                return
        else:
            get_reviews = self.click_first_organization(
                '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div'
            )
            if get_reviews:
                self.click_on_reviews(
                    '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span'    # noqa
                )
            else:
                msg = 'No Review Button Found.'
                context = {'spider': 'Google Reviews'}
                logger.error(msg, context)
                return

        reviews_requests = self.get_all_reviews_requests()
        if not reviews_requests:
            msg = 'No Review requests have found.'
            context = {'spider': 'Google Reviews'}
            logger.error(msg, context)
            return
        for request in reviews_requests:
            text = requests.get(request.url).text
            text = text.strip(")]}\'\n")
            data = process_data(text)
            reviews_list = [process_reviews(reviewer) for reviewer in data]
            self.write_data_in_csv(reviews_list)

        msg = 'Data has been process.'
        context = {'spider': 'Google Reviews'}
        logger.info(msg, context)

