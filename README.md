# Google Reviews scraping
Scraping scripts for various service related data sources with
dockerized selenium infrastructure

## Setup

Inside the root folder of the application run `$ docker-compose up -d`.
This will set up selenium grid as well as currently one node for both
Firefox and Chrome.

## Scraping

For automatic usage of selenium scrapy calls are wrapped by the entry-
point `crawl`, used like following:

`$ docker-compose run google-reviews crawl --company_name="aspria berlin ku'damm"`

or

`$ docker-compose run google-reviews crawl --company_name="Granvalora Limburg"`

Note: The limitation of this script is that, It's currently scrolling only into the 
first page of reviews, I need to improve the code for scrolling further.

But one feature, which I has implemented, is that if there are multiple companies
with the same name, it will automatically take the first company and get it's reviews.

you can see the scraped reviews, in `ArangoDB`. you can access it on 

`http://localhost:8529/`

username and password can be found in `env` file inside `compose` directory.
and the database is `google-reviews`.


------------------------------------

# Testing ETL Google Reviews.

for the sake of testing purpose, I had loaded the selenium driver, and open the reviews of `"aspria berlin ku'damm"`, 
and manually scrolled down to load multiple reviews requests, and get all the content of those requests, and stored it
in files, which you can see in `file` directory, and then inside `input` folder.


You can perform the ETL task, by `Extracting` raw review content.
`Transform` transforming the review's raw content in review's data classes.
`Loading` loading the transformed data as CSV in the `files` `output` folder.

you can just simply use the following command.

`python -m virtualenv  .venv`

`source .venv\bin\activate`

`pip install notebook`

`cd notebooks`

`jupyter notebook`

it will load the jupyter notebook, you can test the ETL pipeline there.
