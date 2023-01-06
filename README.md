# Google Reviews scraping
Scraping scripts for various service related data sources with
dockerized selenium infrastructure

## Setup

Inside the root folder of the application run `$ docker-compose up`.
This will set up selenium grid as well as currently one node for both
Firefox and Chrome.

## Scraping

For automatic usage of selenium scrapy calls are wrapped by the entry-
point `crawl`, used like following:

`$ docker-compose run scraping crawl --company_name=aspira`

