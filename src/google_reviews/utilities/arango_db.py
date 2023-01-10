
import logging
import os

import arango
from arango import ArangoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:

    ARANGO_USERNAME = os.environ.get('ARANGO_USERNAME')
    ARANGO_PASSWORD = os.environ.get('ARANGO_PASSWORD')
    ARANGO_HOST_NAME = os.environ.get('ARANGO_HOST')
    ARANGO_HOST = f'http://{ARANGO_HOST_NAME}:8529'

    def __init__(self):
        self.ARANGO_CLIENT = ArangoClient(hosts=self.ARANGO_HOST)
        self.ARANGO_SYS_DB = self.ARANGO_CLIENT.db(
            '_system',
            username=self.ARANGO_USERNAME,
            password=self.ARANGO_PASSWORD
        )

        if not self.ARANGO_SYS_DB.has_database('google_reviews'):
            self.ARANGO_SYS_DB.create_database('google_reviews')

        self.ARANGO_SOURCE_DB = self.ARANGO_CLIENT.db(
            'google_reviews',
            username=self.ARANGO_USERNAME,
            password=self.ARANGO_PASSWORD
        )

        self.REVIEWS_COLLECTION = self.create_collection('reviews')
        logger.info('Collections Created.')

    def create_collection(self, collection_name: str):
        """

        :param collection_name: this function will take the collection_name and it will be stored.
        :return:
        """
        if self.ARANGO_SOURCE_DB.has_collection(collection_name):
            return self.ARANGO_SOURCE_DB.collection(collection_name)
        else:

            logger.info(f'Created the {collection_name} Collection')
            return self.ARANGO_SOURCE_DB.create_collection(collection_name)

    def insert_data_into_collection(self, collection,  source_data: dict):
        """

        :param collection: pass
        :param source_data:
        :return:
        """
        try:
            self.ARANGO_SOURCE_DB.insert_document(collection.name, source_data)
            logger.info(f'Document inserted in the {collection.name}')
        except arango.exceptions.DocumentInsertError:
            import ipdb; ipdb.set_trace()
            logger.error(f'Document Insertion Error for {collection.name}')
