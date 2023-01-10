
import csv
import logging
import os
import requests

from dataclasses import asdict
from time import sleep

from google_reviews.spiders.selenium_spider import SeleniumSpider
from google_reviews.utilities.data_cleaning import process_data, process_reviews
from google_reviews.utilities.arango_db import Database

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleReviewScraper(SeleniumSpider):
    name = 'google'
    company_name = None
    start_urls = ['https://www.google.com/maps/@50.386969,8.1018231,14z']
    DIR_PATH = os.getcwd()
    TIMEOUT = 10
    MAX_TRIES = 10
    database = Database()

    def __init__(self, company_name):
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
            except Exception as exc:
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
            except Exception as exc:
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
            except Exception as exc:
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

    def parse(self):
        """

        :param response:
        :return:
        """

        # getting the google_maps website.
        self.driver.get(self.start_urls[0])
        self.driver.get('https://www.google.com/maps/')

        # accepting the cookies, to load the website.

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

        # finding the search box, and putting the company name and hiting enter for searching the company.

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

        """ try to click the reviews link, for loading the reviews, if the company is not founded correctly, it will get 
        the first company on the shown items and click it.
        """

        click_next_item = self.click_on_reviews(
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]'    # noqa
        )

        if click_next_item:
            # if it's able to click on the review links, then it will go inside the review panel and try to perfor
            # scrolling.
            # Important: Until now, I am just able to scroll once, in future I can try to implement the unlimited scroll
            scrolled = self.scroll_into_review_pannel(
                '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[11]'
            )
            if not scrolled:
                msg = 'Not able to scroll into review panel.'
                context = {'spider': 'Google Reviews'}
                logger.error(msg, context)
                return
        else:
            # clicking on the first organization, if we found multiple companies with same name.
            get_reviews = self.click_first_organization(
                '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div'
            )
            # click on the reviews link, to load the reviews requests.
            if get_reviews:
                self.click_on_reviews(
                    '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span'    # noqa
                )
            else:
                msg = 'No Review Button Found.'
                context = {'spider': 'Google Reviews'}
                logger.error(msg, context)
                return

        # get all the requests done by the google maps and fetch only review related requests.
        for _ in range(self.MAX_TRIES):
            sleep(1)
            reviews_requests = self.get_all_reviews_requests()
            if reviews_requests:
                break

        if not reviews_requests:
            msg = 'No Review requests have found.'
            context = {'spider': 'Google Reviews'}
            logger.error(msg, context)
            return

        # after getting all reviews related requests, iterate through each of the requests, and fetch the content of
        #those request, So we can get the reviews.

        for request in reviews_requests:
            text = requests.get(request.url).text
            text = text.strip(")]}\'\n")
            data = process_data(text)
            reviews_list = [process_reviews(reviewer, self.company_name) for reviewer in data]
            # for writing the reviews in the list.
            for review in reviews_list:
                    self.database.insert_data_into_collection(
                        self.database.REVIEWS_COLLECTION,
                        asdict(review)
                    )

            # if you want to write csv, you can comment the underline line.
            # self.write_data_in_csv(reviews_list)

        msg = 'Data has been process.'
        context = {'spider': 'Google Reviews'}
        logger.info(msg, context)

