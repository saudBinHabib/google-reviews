import logging

from google_reviews import __version__


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def entrypoint():
    msg = 'google_reviews package version is %(version)s'
    context = {'version': __version__}
    logger.info(msg, context)
