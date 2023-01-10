import pkg_resources
from path import Path

__version__ = '0.0.1'

try:
    pkg_version = pkg_resources.get_distribution('google_reviews').version
except pkg_resources.DistributionNotFound:
    raise RuntimeError('Install project, eg "pip install -e ."')

if pkg_version != __version__:
    raise RuntimeError('Reinstall project, eg "pip install -e ."')

ROOT = Path(__file__).dirname
