import json
import logging

logger = logging.getLogger(__name__)


class JsonWriterPipeline(object):
    file_path = None

    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        """

        :param spider:
        :return:
        """
        logger.info(f'Writing to file: "{self.file_path}".')
        self.file = open(JsonWriterPipeline.file_path, mode='wt')

    def close_spider(self, spider):
        """

        :param spider:
        :return:
        """
        self.file.close()
        logger.info(f'Finished writing to file "{self.file_path}".')

    def process_item(self, item, spider):
        """

        :param item:
        :param spider:
        :return:
        """
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item