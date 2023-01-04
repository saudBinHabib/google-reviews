import re
from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).parent

init = here / 'src' / 'scraping' / '__init__.py'

with init.open(mode='rt', encoding='utf-8') as fp:
    txt = fp.read()

try:
    pattern = r"^__version__ = '([^']+)'\r?$"
    version = re.findall(pattern, txt, re.M)[0]
except IndexError:
    raise RuntimeError('Unable to determine version.')

requirements = here / 'requirements' / 'dev.txt'

try:
    with requirements.open(mode='rt', encoding='utf-8') as fp:
        install_requires = (
            line.split('#')[0].strip() for line in fp if not
            line.startswith('git+')
        )
        install_requires = list(filter(None, install_requires))
except IndexError:
    raise RuntimeError('requirements/dev.txt is broken')

setup(
    name='scraping',
    version=version,
    install_requires=install_requires,
    include_package_data=True,
    package_data={
        '': ['*.json'],
    },
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'crawl = scraping.entrypoints.crawl:entrypoint',
        ],
    },
)
